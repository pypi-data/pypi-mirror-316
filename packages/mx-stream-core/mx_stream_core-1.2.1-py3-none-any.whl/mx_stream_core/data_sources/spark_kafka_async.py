import json
import logging

import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql.functions import window, col
from pyspark.sql.streaming.state import GroupState, GroupStateTimeout
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, \
    TimestampType

from mx_stream_core.data_sources.base import BaseDataSource


def update_state(key, pdf_iterator, state: GroupState):
    """
    Hàm xử lý trạng thái của nhóm với `applyInPandasWithState`.
    :param key: Key của nhóm (ví dụ: (window, topic))
    :param pdf_iterator: Iterator chứa các pandas DataFrame.
    :param state: Trạng thái của nhóm.
    :return: pandas DataFrame kết quả.
    """
    # Hợp nhất tất cả các DataFrame trong iterator
    events_df = pd.concat(list(pdf_iterator))
    # print('[Debug] events_df:', events_df)
    # Trạng thái hiện tại (nếu có)
    if state.exists:
        state_value = state.get
        current_state = {"events": json.loads(state_value[0]), "event_count": state_value[1]}
    else:
        current_state = {"events": [], "event_count": 0}

    # print(f"[Debug] 28 current_state: {current_state}")
    # Tổng hợp các sự kiện mới
    new_events = events_df.to_dict("records")
    # print(f"[Debug] 31 new_events: {new_events}")
    events = [event.get('data') for event in new_events]
    current_state["events"].extend(events)
    current_state["event_count"] += len(new_events)
    # print(f"Has timeout {state.hasTimedOut}")
    # Kiểm tra timeout
    if state.hasTimedOut:
        # Xử lý logic khi timeout
        result = pd.DataFrame([{
            "window_start": key[0].get('start'),
            "window_end": key[0].get('end'),
            "topic": key[1],
            "events": json.dumps(current_state["events"]),
            "event_count": str(current_state["event_count"]),
        }])
        state.remove()  # Xóa trạng thái
        return [result]  # Trả về một danh sách chứa DataFrame

    # Cập nhật trạng thái mới
    state.update((current_state["events"], current_state["event_count"]))
    current_processing_time = state.getCurrentProcessingTimeMs()  # Lay thoi gian hien tai cua processing
    window_end_ms = key[0].get('end').timestamp() * 1000  # Lay thoi gian ket thuc cua window
    # print(f"[Debug] 49 current_processing_time: {current_processing_time} window_end_ms: {window_end_ms}")
    timeout_at = window_end_ms - current_processing_time  # Tinh thoi gian timeout
    if timeout_at < 0:
        timeout_at = 30000  # 30s
    else:
        timeout_at = timeout_at + 30000  # 30s
    # print(f"[Debug] 54 timeout_at: {timeout_at}")
    state.setTimeoutDuration(timeout_at)

    return []


class SparkKafkaAsynchronousDataSource:
    def __init__(self,
                 async_source: BaseDataSource,
                 checkpoint_location=None,
                 watermark_delay_threshold="5 minutes",
                 window_duration="2 minutes",
                 idle_processing_timeout=30000,
                 ):
        if not async_source:
            raise ValueError("Async data source must be provided")
        self.query = None
        self.async_source = async_source
        self.checkpoint_location = checkpoint_location
        self.watermark_delay_threshold = watermark_delay_threshold
        self.window_duration = window_duration
        self.idle_processing_timeout = idle_processing_timeout
        self.windowed_df = None

    def foreach(self, func):
        df = self.async_source.get().withWatermark("timestamp", self.watermark_delay_threshold) \
            .select(
            window(col("timestamp"), self.window_duration).alias("window"),
            col("topic"),
            col("data"),
        )
        windowed_df = df.groupBy(
            col("window"),
            col("topic")
        ).applyInPandasWithState(
            outputMode="update",
            func=update_state,
            outputStructType=StructType([
                StructField("window_start", TimestampType()),
                StructField("window_end", TimestampType()),
                StructField("topic", StringType()),
                StructField("events", StringType()),  # Nếu bạn cần lưu các sự kiện dạng JSON string
                StructField("event_count", StringType())
            ]),
            stateStructType=StructType([
                StructField("events", StringType()),
                StructField("event_count", IntegerType())
            ]),
            timeoutConf=GroupStateTimeout.ProcessingTimeTimeout
        )
        self.windowed_df = windowed_df.select(
            col("window_start"),
            col("window_end"),
            col("events"),
            col("topic"),
            col("event_count"),
        )
        self.query = self.windowed_df.writeStream.option("checkpointLocation", self.checkpoint_location) \
            .outputMode("update") \
            .option("checkpointLocation", self.checkpoint_location) \
            .trigger(processingTime="5 seconds") \
            .foreachBatch(lambda batch, epoch_id: func(batch, epoch_id)).start()

    def awaitTermination(self):
        if self.query:
            self.query.awaitTermination()
