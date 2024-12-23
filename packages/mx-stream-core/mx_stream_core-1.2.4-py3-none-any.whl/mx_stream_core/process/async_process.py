from pyspark.sql.functions import window, col, lit
from pyspark.sql.streaming.state import GroupStateTimeout

from mx_stream_core.data_sources.base import BaseDataSource
from mx_stream_core.process.base_process import BaseProcess
from mx_stream_core.process.pandas.update_with_state import update_with_state
from mx_stream_core.process.schema import output_schema, state_schema


class AsyncProcess(BaseProcess):
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

    def foreach(self, func, processing_time='5 seconds'):
        df = self.async_source.get().withWatermark("timestamp", self.watermark_delay_threshold) \
            .select(
            window(col("timestamp"), self.window_duration).alias("window"),
            col("topic"),
            col("data"),
        ).withColumn('idle_processing_timeout', lit(self.idle_processing_timeout))
        windowed_df = df.groupBy(
            col("window"),
            col("topic")
        ).applyInPandasWithState(
            outputMode="update",
            func=update_with_state,
            outputStructType=output_schema,
            stateStructType=state_schema,
            timeoutConf=GroupStateTimeout.ProcessingTimeTimeout
        )
        windowed_df.select(
            col("window_start"),
            col("window_end"),
            col("events"),
            col("topic"),
            col("event_count"),
        )
        self.query = windowed_df.writeStream.option("checkpointLocation", self.checkpoint_location) \
            .outputMode("update") \
            .option("checkpointLocation", self.checkpoint_location) \
            .trigger(processingTime=processing_time) \
            .foreachBatch(lambda batch, epoch_id: func(batch, epoch_id)).start()

    def awaitTermination(self):
        if self.query:
            self.query.awaitTermination()
