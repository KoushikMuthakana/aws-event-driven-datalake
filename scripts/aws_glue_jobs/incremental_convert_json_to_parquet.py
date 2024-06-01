import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DateType

from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# Initialize GlueContext and SparkSession
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'DATABASE_NAME', 'TABLE_NAME', 'OUTPUT_PATH'])
spark = SparkSession.builder.appName("GlueJob").getOrCreate()
glueContext = GlueContext(spark.sparkContext)
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Parameters
database_name = args['DATABASE_NAME']
table_name = args['TABLE_NAME']
output_path = args['OUTPUT_PATH']

# Read from Glue Catalog
raw_dyf = glueContext.create_dynamic_frame.from_catalog(
    database=database_name,
    table_name=table_name,
    transformation_ctx="raw_dyf"
)

# Define the schema for the Parquet file
schema = StructType([
    StructField("event_type", StringType(), True),
    StructField("event_subtype", StringType(), True),
    StructField("event_uuid", StringType(), True),
    StructField("created_at", DateType(), True),
    StructField("event_name", StringType(), True),
    # Add other fields as necessary
])

raw_df = raw_dyf.toDF()

# Apply the schema to the DataFrame
raw_df = spark.createDataFrame(raw_df.rdd, schema)

# Convert back to DynamicFrame
raw_dyf = DynamicFrame.fromDF(raw_df, glueContext, "raw_dyf")

# Write the data to Parquet format, partitioned by event_type, event_subtype, year, month, and day
glueContext.write_dynamic_frame.from_options(
    frame=raw_dyf,
    connection_type="s3",
    connection_options={
        "path": output_path,
        "partitionKeys": ["event_type", "event_subtype", "year", "month", "day"]
    },
    format="parquet",
    transformation_ctx="datasink4"
)

job.commit()
