### AWS Glue PySpark Script for Incremental Load


### PySpark Script [incremental_convert_json_to_parquet.py](incremental_convert_json_to_parquet.py)

### Setting Up the AWS Glue Job

1. **Upload the Script**: Upload your script (`incremental_convert_json_to_parquet.py`) to an S3 bucket.
2. **Create a Glue Job**:
   - Go to the AWS Glue console.
   - Click on "Jobs" and then "Add job".
   - Name your job (e.g., `incremental-convert-json-to-parquet`).
   - Choose an IAM role with appropriate permissions.
   - For "Type", select "Spark".
   - For "This job runs", select "A new script to be authored by you".
   - In the script section, specify the S3 path to your uploaded script.
   - Set "Temporary directory" for job bookmarks to manage incremental loads.

### Glue Crawler Setup

1. **Create a Glue Crawler**:
   - Go to the AWS Glue console.
   - Click on "Crawlers" and then "Add crawler".
   - Name your crawler (e.g., `json-data-crawler`).
   - Set the data store to your S3 path (e.g., `s3://your-bucket-name/raw-data/`).
   - Set the crawler to run on a schedule that matches your data ingestion frequency (e.g., daily).

### Scheduling the AWS Glue Job

1. **Create a Schedule**:
   - Go to the AWS Glue console.
   - Click on "Triggers" and then "Add trigger".
   - Name your trigger (e.g., `daily-midnight-trigger`).
   - Set the trigger type to "Scheduled".
   - Set the schedule to run daily at midnight (e.g., `cron(0 0 * * ? *)`).
   - Attach the trigger to the Glue job you created earlier.

### Using Job Bookmarks

Enable job bookmarks in your Glue job settings to ensure that the job processes only new data added since the last run.

1. **Enable Job Bookmarks**:
   - Go to the AWS Glue console.
   - Navigate to your job (e.g., `incremental-convert-json-to-parquet`).
   - Under the "Job details" section, enable the "Job bookmark" setting.

### Or using AWS Step Functions to Trigger AWS Glue Jobs with Parameters

AWS Step Functions can be used to orchestrate the execution of AWS Glue jobs, including passing parameters to the jobs.

1. **Create the Step Function**

Define your Step Function to start the AWS Glue job with parameters. Here’s an example definition: [step_function_definition.json](../aws_step_functions/trigger_glue_incremental_load_job.json)

2. **Deploy the Step Function**

Deploy the Step Function using the AWS Management Console or using the AWS CLI. Here’s an example using the AWS CLI:

```sh
aws stepfunctions create-state-machine \
    --name "TriggerGlueJobStateMachine" \
    --definition file://step_function_definition.json \
    --role-arn arn:aws:iam::account-id:role/your-step-functions-role
```

5. **Trigger the Step Function**

Start the Step Function execution and pass the required parameters using the AWS Management Console or the AWS CLI. Here’s an example using the AWS CLI:

```sh
aws stepfunctions start-execution \
    --state-machine-arn arn:aws:states:region:account-id:stateMachine:TriggerGlueJobStateMachine \
    --input '{"database_name": "your_database", "table_name": "your_table", "output_path": "s3://your-bucket-name/processed-data/"}'
```

