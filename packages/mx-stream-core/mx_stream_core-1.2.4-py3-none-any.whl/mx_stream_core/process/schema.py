from pyspark.sql.types import StructType, StructField, TimestampType, StringType, IntegerType

output_schema = StructType([
    StructField("window_start", TimestampType()),
    StructField("window_end", TimestampType()),
    StructField("topic", StringType()),
    StructField("events", StringType()),
    StructField("event_count", StringType())  # Ly do ?
])

state_schema = StructType([
    StructField("events", StringType()),
    StructField("event_count", IntegerType())
])
