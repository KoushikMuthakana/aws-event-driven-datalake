# AWS Event-Driven Data Lake

## Overview
This repository contains the code and infrastructure to create a robust, scalable data lake using AWS services. The system is designed to ingest, process, and store events coming from an Amazon Kinesis Data Stream. The architecture ensures high performance, scalability, and efficient querying capabilities, making it ideal for processing both large and small amounts of data.

### Features

- **Processes Data in Real-Time**: Deduplicates and transforms incoming data immediately to ensure accuracy and relevance.
- **Stores Data Efficiently**: Saves raw and processed data in a highly efficient format, optimizing storage space and retrieval speed.
- **Automates Metadata Management**: Automatically discovers and catalogs new data, maintaining up-to-date schemas and metadata.
- **Handles Incremental Loads**: Processes and transforms new data incrementally, ensuring the data store is always current.
- **Supports Advanced Analytics**: Enables both batch and streaming data processing for comprehensive analytics and business intelligence reporting.
- **Ensures Consistency and Repeatability**: Manages the entire architecture with automated, consistent deployment and updates.
- **Monitors System Health**: Continuously monitors the performance and health of the data pipeline, providing metrics and logs for effective management.
- **Facilitates Data Recovery**: Provides capabilities to replay events for data recovery and reprocessing as needed.

## Architecture

<p align="center">

<img src="./images/Event_Driven_architecture.png" alt="Architecture.png" />
</p>


## Architecture Flow

1. **Customers (Desktop and Mobile)**: Users generate events via desktop and mobile devices.
2. **Amazon Kinesis Data Streams**: Captures and streams real-time data from multiple customer events.
3. **Amazon CloudWatch**: Monitors the performance and health of the streaming data pipelines.
4. **AWS Lambda**: Processes incoming data, detects duplicates, and handles data transformation.
5. **Amazon DynamoDB**: Stores unique identifiers for duplicate detection and primary key management.
6. **Amazon Kinesis Firehose**: Delivers raw data to Amazon S3 in compressed raw JSON format, partitioned by event type,event_subtype and (Year/Month/day).
7. **Amazon S3 (Compressed Raw JSON Files)**: Serves as the data lake storage, storing raw JSON files in a compressed format for efficient storage and retrieval.
8. **AWS Glue Crawler**: Scans the raw JSON files in S3 and updates the Glue Data Catalog with table definitions.
9. **AWS Glue Data Catalog**: Central metadata repository for data discovery and search.
10. **AWS Glue Job (Apache Spark)**: Transforms raw JSON data into aggregated, partitioned Parquet files, managing incremental loads.
11. **Amazon S3 (Processed Data Storage)**: Stores the transformed and aggregated Parquet files in partitions.
12. **Databricks with Apache Spark**: Processes both batch and streaming data from Amazon S3 for advanced analytics.
13. **Visualization and ML/AI**: Utilizes the processed data for generating insights through visualization tools and machine learning models.
14. **Events Replay (AWS Lambda)**: Replays events from raw JSON files if needed for data recovery or reprocessing.

--- 

### Why AWS Lambda is Perfect for This Architecture

AWS Lambda is a serverless compute service that runs  code in response to events. It automatically manages the underlying compute resources, making it a great fit for the data-driven architecture shown.

### Key Benefits of AWS Lambda

1. **Event-Driven Processing**:
   - **Real-time Handling**: Lambda can trigger functions as soon as new data arrives, allowing immediate processing of events.
   - **Data Transformation**: It can clean, filter, and format data on the fly before sending it to the next step.

2. **Scalability**:
   - **Automatic Scaling**: Lambda automatically adjusts to handle more events when needed and scales down when demand decreases.
   - **High Capacity**: It can process thousands of events per second, suitable for both small and large data volumes.

3. **Cost Efficiency**:
   - **Pay Only for What You Use**: You only pay for the time  code runs, down to the millisecond, and the number of requests. This is cost-effective for varying workloads.
   - **No Idle Costs**: Because Lambda is serverless, you don't pay for idle compute time, saving money for workloads that are not constant.

4. **Seamless Integration**:
   - **Works Well with Other AWS Services**: Lambda integrates easily with services like Kinesis, S3, and DynamoDB, making it simple to build a complete data pipeline.
   - **Orchestrates Data Flow**: Lambda can trigger and coordinate tasks between different AWS services, ensuring smooth data processing.

5. **Flexibility**:
   - **Multiple Languages**: Lambda supports various programming languages like Python, Node.js, and Java, allowing you to use the tools you are comfortable with.

### Handling Different Data Volumes

#### Low Data Volumes
- **Efficient and Cost-Effective**: For small amounts of data, Lambda's pay-as-you-go model ensures you only pay for the compute time you use, making it very economical.
- **Quick Response**: Lambda can quickly start processing small data batches without delay.

#### High Data Volumes
- **Scales Automatically**: Lambda can handle large amounts of data by automatically scaling to match the incoming data rate.
- **High Performance**: Even with high data volumes, Lambda can process data efficiently, ensuring timely and reliable data handling.

### Why Amazon Kinesis Firehose is a Perfect Fit for This Architecture

Amazon Kinesis Firehose is a fully managed service designed to capture, transform, and load streaming data to various AWS destinations like S3, Redshift, Elasticsearch, and Splunk. Here’s why it’s an excellent fit for  architecture:

#### Key Benefits of Amazon Kinesis Firehose

- **Real-time Data Delivery**:
  - **Immediate Processing**: Firehose captures and processes data streams in real time, ensuring that data is promptly delivered to the designated storage or analytics destinations.
  - **Low Latency**: Designed for low-latency data delivery, making it ideal for real-time analytics and monitoring use cases.

- **Automatic Scaling**:
  - **Handles Variable Data Volumes**: Firehose automatically scales to accommodate data streams of any size, from small trickles of data to large, high-volume streams.
  - **Elastic Scaling**: Automatically adjusts to changes in data volume, ensuring consistent performance without manual intervention.

- **Built-in Data Transformation**:
  - **Data Formatting**: Supports transformation tasks like converting data to JSON, CSV, or Parquet formats, which makes the data ready for analysis or further processing.
  - **Compression**: Can compress data (e.g., using GZIP or Snappy) before delivery, reducing storage costs and improving data transfer efficiency.
  - **Data Enrichment**: Allows for simple data manipulation and enrichment using Lambda functions, ensuring that the data meets  specific requirements before being stored or analyzed.

- **Cost Efficiency**:
  - **Pay-as-You-Go Pricing**: You only pay for the amount of data ingested, transformed, and delivered, making it a cost-effective solution for varying workloads.
  - **No Upfront Costs**: Avoids the need for significant upfront investments in infrastructure, paying only for the resources used.

- **Seamless Integration**:
  - **AWS Ecosystem**: Seamlessly integrates with other AWS services like S3, Redshift, and Elasticsearch, enabling the creation of efficient and cohesive data pipelines.
  - **Simple Setup**: Easy to set up and manage, with minimal configuration required to start delivering data to  chosen destinations.

### Handling Different Data Volumes

#### Low Data Volumes
- **Efficient Processing**: For smaller data streams, Firehose processes and delivers data efficiently, ensuring that even low volumes of data are quickly available for storage or analysis.
- **Cost-effective**: The pay-as-you-go model ensures that costs remain low when dealing with small data volumes, as you only pay for the data processed.

#### High Data Volumes
- **Automatic Scaling**: Firehose can automatically scale to handle large volumes of data streams, ensuring that high data loads are processed and delivered without performance issues.
- **Reliable Delivery**: Ensures that even with high volumes, data is reliably delivered to its destinations, maintaining data integrity and performance.
- **Batch Processing**: Supports buffering and batching data to optimize transfer efficiency and reduce costs, particularly beneficial when dealing with high data throughput.

### Why AWS Glue is the Ideal Choice for This Architecture


AWS Glue is a fully managed ETL (Extract, Transform, Load) service that simplifies the process of preparing and loading data for analytics. It combines the power and flexibility of Apache Spark with the convenience of a managed service, making it an excellent fit for the described architecture.

#### Key Benefits of AWS Glue in This Architecture

1. **Fully Managed Service**:
   - **No Infrastructure Management**: AWS Glue eliminates the need for managing the underlying infrastructure. AWS handles provisioning, configuring, and scaling the resources required for  ETL jobs. This allows you to focus on developing ETL processes without worrying about the operational complexities of cluster management.

2. **Serverless Architecture**:
   - **Auto-scaling**: AWS Glue automatically scales the underlying infrastructure based on the workload, ensuring optimal resource utilization without manual intervention. This is particularly beneficial for handling varying data volumes.
   - **Maintenance-Free**: The serverless nature of Glue means there are no servers to maintain, patch, or upgrade, significantly reducing operational overhead.

3. **Cost Efficiency**:
   - **Pay-as-You-Go Pricing**: Glue operates on a pay-as-you-go pricing model, where you only pay for the resources consumed during  ETL jobs. This is cost-effective for both low and high volumes of data processing.
   - **Cost-effective for Intermittent Jobs**: For ETL jobs that run intermittently, Glue's pricing model is economical compared to the continuous costs associated with managing dedicated infrastructure.

4. **Integrated Data Catalog**:
   - **AWS Glue Data Catalog**: Glue includes an integrated data catalog that automatically discovers and registers metadata from  data sources. This catalog is used to create a unified view of  data across various AWS services, simplifying data discovery and governance.
   - **Schema Management**: Glue manages schema evolution and versioning, ensuring consistency and integrity in  data processing pipelines.

5. **Ease of Use**:
   - **Python and PySpark Support**: Glue supports PySpark, making it easier for data engineers and data scientists familiar with Python to write and maintain ETL jobs.
   - **Built-in Transformations**: Glue provides a variety of built-in transformations and connectors for various data sources, simplifying the development of complex ETL workflows.

6. **Seamless Integration with AWS Ecosystem**:
   - **Integration**: Glue integrates seamlessly with other AWS services such as S3, Redshift, RDS, DynamoDB, and Athena. This makes it easier to build end-to-end data pipelines within the AWS ecosystem.
   - **IAM and Security**: Glue leverages AWS Identity and Access Management (IAM) for fine-grained access control and integrates with AWS Key Management Service (KMS) for data encryption, ensuring robust security.

7. **Scalability and Flexibility**:
   - **Handles Variable Data Volumes**: Glue is designed to handle both low and high volumes of data efficiently. It can scale down to process small data sets cost-effectively and scale up to handle large-scale data processing tasks.
   - **Distributed Computing with Spark**: Leveraging Apache Spark, Glue can process large-scale data efficiently through distributed computing. This makes it suitable for handling high data volumes with complex transformation requirements.

8. **Job Scheduling and Orchestration**:
   - **Built-in Scheduler**: Glue provides a built-in job scheduler that allows you to define and manage job schedules, dependencies, and retries, simplifying the orchestration of complex ETL workflows.
   - **Event-driven ETL**: Glue supports event-driven ETL workflows, enabling you to trigger jobs based on events in other AWS services such as S3 or DynamoDB Streams.

### Handling Data Volumes

#### Low Data Volumes
- **Cost Efficiency**: Glue's serverless, pay-as-you-go pricing model ensures that you only pay for the compute resources you use, making it cost-effective for small data sets.
- **Quick Provisioning**: Glue can quickly provision the necessary resources to process small data sets, reducing latency and ensuring timely data processing.

#### High Data Volumes
- **Auto-Scaling**: Glue automatically scales up the resources required to handle large data volumes, ensuring that the ETL jobs are processed efficiently without manual intervention.
- **Distributed Processing**: By leveraging Apache Spark's distributed processing capabilities, Glue can handle complex transformations and large-scale data processing tasks, making it suitable for big data workloads.
- **Optimized Performance**: Glue can efficiently manage large data volumes by partitioning data and performing parallel processing, optimizing both performance and resource utilization.

### Why Amazon DynamoDB is Perfect for Handling Duplicates

- **Fast Data Access**: Provides quick lookups for unique identifiers, ensuring efficient duplicate detection.
- **Automatic Scaling**: Scales automatically to handle both low and high volumes of data seamlessly.
- **Fully Managed**: No need for server maintenance, simplifying operations and allowing you to focus on  application.
- **High Availability**: Ensures data is always available and safe, thanks to replication across multiple availability zones.
- **Cost-effective**: Pay only for what you use, making it economical for varying data volumes.

### Why Amazon S3 is Perfect for This Architecture

- **Unlimited Storage Capacity**: Provides virtually unlimited storage, making it suitable for both small and large volumes of data.

- **Automatic Scaling**: Seamlessly scales storage resources up or down based on  data needs without manual intervention.

- **High Durability and Availability**: Designed for 99.9999% durability and 99.99% availability, ensuring data is safe and accessible.

- **Multi-AZ Replication**: Data is automatically replicated across multiple availability zones for high availability and fault tolerance.

- **Cost-effective**: Pay-as-you-go pricing ensures you only pay for the storage you use, making it economical for varying data volumes.

- **Flexible Storage Classes**: Offers multiple storage classes (Standard, Infrequent Access, Glacier) to optimize costs based on data access patterns.

- **Advanced Data Management**: Supports lifecycle policies for automated data transition and deletion, versioning for data management, and encryption for security.

- **Seamless AWS Integration**: Easily integrates with other AWS services like Lambda, Glue, and Redshift, and supports event notifications to trigger workflows and data processing pipelines.


### Why AWS Glue Crawler and AWS Glue Data Catalog are Perfect for This Architecture

- **Automated Metadata Discovery**:
  - **Automatic Schema Detection**: AWS Glue Crawler automatically discovers new data and infers schemas, saving time and reducing manual effort.
  - **Continuous Updates**: Keeps the Data Catalog up-to-date with the latest data changes, ensuring accurate metadata for querying and processing.

- **Centralized Metadata Repository**:
  - **Unified View**: AWS Glue Data Catalog provides a centralized repository for storing and managing metadata, offering a unified view of  data across the entire data lake.
  - **Easy Data Search**: Enables easy discovery and search of data assets using the catalog, improving data accessibility.

- **Integration with AWS Services**:
  - **Seamless Integration**: Integrates well with other AWS services like Athena, Redshift, and S3, facilitating streamlined data workflows and analytics.
  - **Direct Access for ETL Jobs**: ETL jobs can directly access the Data Catalog, simplifying data transformation processes.

- **Data Governance and Security**:
  - **Fine-grained Access Control**: Supports fine-grained access control and audit capabilities, ensuring that only authorized users can access sensitive data.
  - **Data Lineage**: Provides data lineage tracking, helping in maintaining data quality and compliance.

- **Scalability**:
  - **Handles Any Data Volume**: Efficiently handles metadata for both small and large datasets, automatically scaling to accommodate growing data volumes.
  - **Optimized Performance**: Designed to handle the complexities of large-scale data lakes, ensuring quick and efficient metadata operations.

- **Cost Efficiency**:
  - **Pay-as-you-go**: Costs are based on the resources used by the crawlers and the number of objects in the Data Catalog, making it cost-effective for different data volumes.
  - **No Infrastructure Management**: Being a managed service, there’s no need for infrastructure maintenance, reducing operational costs.

### Handling Different Data Volumes

- **Low Data Volumes**:
  - **Cost-effective**: Low costs for managing metadata of smaller datasets due to the pay-as-you-go pricing model.
  - **Quick Setup**: Rapid deployment and setup for small-scale data environments.

- **High Data Volumes**:
  - **Scalable Metadata Management**: Efficiently handles large datasets, automatically scaling to manage extensive metadata.
  - **High Performance**: Maintains performance and reliability even with large volumes of data, ensuring quick metadata discovery and updates.

### Why Databricks with Apache Spark is Perfect for This Architecture

- **Unified Analytics Platform**:
  - **Integrated Workspace**: Databricks provides a collaborative environment for data scientists, engineers, and analysts, integrating data processing, analytics, and machine learning.
  - **End-to-End Data Pipeline**: Supports the entire data lifecycle, from ingestion and processing to analysis and visualization.

- **Scalability and Performance**:
  - **Scalable Compute**: Automatically scales compute resources based on workload, ensuring efficient processing of both small and large data volumes.
  - **Distributed Computing**: Leverages Apache Spark’s distributed computing capabilities to process large datasets quickly and efficiently.

- **Advanced Analytics and Machine Learning**:
  - **Built-in ML Libraries**: Databricks includes built-in libraries for machine learning, enabling advanced analytics directly within the platform.
  - **Real-time and Batch Processing**: Supports both real-time streaming and batch data processing, providing flexibility for different use cases.

- **Cost Efficiency**:
  - **Pay-as-You-Go**: Databricks offers a pay-as-you-go pricing model, ensuring you only pay for the compute resources used, making it cost-effective for varying data volumes.
  - **Optimized Resource Usage**: Automatically optimizes resource usage, reducing costs associated with idle compute power.

- **Collaboration and Productivity**:
  - **Shared Notebooks**: Facilitates collaboration through shared notebooks, allowing team members to work together in real-time.
  - **Version Control**: Integrated version control helps manage and track changes to code and data workflows, improving productivity and reducing errors.

- **Seamless Integration**:
  - **Works with AWS Services**: Integrates smoothly with AWS services like S3, Redshift, and Glue, making it easy to build comprehensive data pipelines.
  - **Data Source Connectivity**: Connects to a wide variety of data sources, enhancing data ingestion and processing capabilities.

### Handling Different Data Volumes

- **Low Data Volumes**:
  - **Efficient Processing**: Databricks can efficiently handle small datasets, scaling down compute resources to save costs while maintaining performance.
  - **Cost-effective**: Pay-as-you-go pricing ensures minimal costs when dealing with low data volumes, as you only pay for what you use.

- **High Data Volumes**:
  - **High Performance**: Databricks can process large datasets quickly due to Spark’s distributed computing power, ensuring timely and reliable data processing.
  - **Elastic Scaling**: Automatically scales up compute resources to handle large volumes of data, ensuring consistent performance without manual intervention.
  - **Advanced Features**: Capabilities like caching, optimized execution plans, and in-memory processing make it highly efficient for large-scale data operations.

---


## Design Questions

**1. How would you handle duplicate events?**

- To manage duplicates efficiently and process streaming data in real-time, I use AWS Kinesis Data Stream, AWS Lambda, and DynamoDB. 
- The Kinesis stream captures incoming data, and the Lambda function processes each record, checking for duplicates using DynamoDB.
- This approach ensures only unique data is stored in S3, with DynamoDB acting as a cache to filter duplicates.

**For detailed code logic, refer to the [Detailed Implementation README.md](./scripts/README.md)**

---

**2. How would you partition the data to ensure good querying performance and scalability?**
I have used the same Partitioning (event_type, sub_event_type, event_date (year,month,day)) on both raw and processed file on two reasons
1. Raw layer - Easy to replicate specific events on specific days if needed or replay entire state.
2. Processed layer - Assuming the downstream tasks mostly relay on event types, sub event types and aggregated data (lowest frequency is day).

#### Detailed Partitioning Strategy

#### Amazon S3 Partitioning
Amazon S3 serves as the primary storage layer in  data lake. Proper partitioning of data stored in S3 can significantly enhance query performance and scalability.

##### Partitioning Structure
- **Event Type:** Top-level directory that segregates data based on the type of event. This is useful for quickly narrowing down searches to specific event categories.
- **Event Subtype:** Sub-directory within each event type that further categorizes events. This adds an additional layer of granularity, making it easier to query specific subsets of event types.
- **Year/Month/Day:** Temporal partitioning based on the date the event occurred. This structure supports efficient time-based queries and ensures that data can be easily managed and archived.

##### Example Directory Structure
```
s3://your-bucket-name/event_type/event_subtype/year/month/day/
```

#### Example Breakdown
- **event_type:** Type of the event (e.g., "account", "lesson", "payment").
- **event_subtype:** Further categorization within each event type (e.g., "created", "started", "order").
- **year/month/day:** Temporal partitions to organize data chronologically.

#### Benefits of This Partitioning Strategy
1. **Improved Query Performance:**
   - By organizing data into partitions, queries can be directed to specific directories, reducing the amount of data scanned.
   - Temporal partitioning allows efficient time-range queries, which are common in analytical workloads.

2. **Scalability:**
   - This hierarchical partitioning scheme allows the data lake to grow efficiently without compromising performance.
   - New partitions can be added dynamically as new event types or dates are encountered, supporting continuous data ingestion.

3. **Data Management:**
   - Facilitates easier data management tasks such as data lifecycle policies, backups, and archival.
   - Data can be easily purged or archived based on time-based partitions.

### Glue Data Catalog Partitioning
AWS Glue Crawler will automatically recognize these partitions and add them to the Glue Data Catalog. This metadata catalog will be used to optimize query performance further.

#### Glue Crawler Configuration
- **Schedule:** Set the Glue Crawler to run periodically (e.g., hourly, daily) to keep the metadata up to date with the latest partitions.
- **Classifier:** Use classifiers to correctly interpret the schema of  partitioned data.

### Key Points for Partitioning Strategy
1. **Event Type and Subtype Partitioning:**
   - Allows quick filtering of relevant events.
   - Enhances query performance by reducing the amount of data scanned.

2. **Temporal Partitioning:**
   - Supports efficient time-based queries and data management.
   - Facilitates easier data archiving and lifecycle management.

3. **Glue and Databricks Integration:**
   - Glue Crawler and Catalog ensure that partitions are recognized and optimized for query performance.
   - Databricks utilizes these partitions for advanced analytics, ensuring efficient data processing.

**For detailed code logic, refer to the [Detailed Implementation README.md](./scripts/README.md)**

---

**3. What format would you use to store the data?**

I have used two formats, Json with compression and parquet format (Both are partitioned for better query performance )
- **Raw Data Format**:
     Raw data is stored in JSON format and compressed to save storage space and preserve the original state of the data.
    - **Purpose**: This format is ideal for preserving the original data for replication or reprocessing from scratch if needed. Compression helps in reducing storage costs while maintaining the integrity of the raw data.
    - **Partitioning**: Data is partitioned by event type, subtype, and date (year, month, day) to facilitate easy access and management.

- **Processed Data Format**: Processed data is stored in Parquet format, which is a columnar storage file format optimized for performance and storage efficiency.
    - **Purpose**: Parquet is compatible with Apache Spark, making it ideal for analytics and data processing tasks. It allows efficient querying and data retrieval.
    - **Partitioning**: Similar to the raw data, the processed data is also partitioned by event type, subtype, and date (year, month, day) to optimize query performance and scalability. 

### Benefits of Using These Formats

- **JSON with Compression**:
  - **Preservation**: Maintains the original data state, essential for accurate replication or reprocessing.
  - **Efficiency**: Compression reduces storage costs and speeds up data transfer.

- **Parquet with Partitions**:
  - **Compatibility**: Works seamlessly with Spark, enhancing data processing capabilities.
  - **Performance**: Columnar storage format improves query performance, especially for analytical workloads.
  - **Scalability**: Partitioning by event type, subtype, and date ensures efficient data management and scalability.
---

**4. How would you test the different components of your proposed architecture?**
    
I will test individual component by mocking data and validating results individually and at the same time, running E2E flow and validate final results.This kind of testing helps to test the **functionality** and **connectivity**.        

- **Data Ingestion (Kinesis Data Streams)**: Simulate various event types and volumes to test ingestion and ensure data flows correctly from sources.
- **Real-time Processing (AWS Lambda)**: Test Lambda functions for deduplication and transformation using mock events, and validate integration with DynamoDB.
- **Data Storage (Amazon S3)**: Test compression and partitioning of raw JSON files, and verify correct storage and partitioning of processed Parquet files.
- **Metadata Management (AWS Glue Crawler and Data Catalog)**: Run Glue Crawlers to validate schema detection and ensure accurate metadata in the Data Catalog.
- **Data Processing (AWS Glue Jobs)**: Test ETL scripts for data transformation, run complete Glue Jobs on test datasets, and verify processed data storage.
- **Advanced Analytics (Databricks with Apache Spark)**: Test Spark jobs for data processing and analytics, validate batch and streaming outputs, and ensure data flow to Databricks.
- **Monitoring and Logging (Amazon CloudWatch)**: Test creation of metrics and logs, validate alert configurations, and ensure logs and metrics are correctly sent to CloudWatch.
- **Event Replay (AWS Lambda)**: Test Lambda functions for event replay, validate retrieval and reprocessing of historical data from S3, and ensure the end-to-end replay process works.

**5. How would you ensure the architecture deployed can be replicable across environments?**

---

**6. Would your proposed solution still be the same if the amount of events is 1000 times smaller or bigger?**

Yes, the proposed solution would still be effective if the amount of events is 1000 times smaller or bigger. This is because

- **Pay-as-You-Use Services**: The architecture leverages AWS services that charge based on usage, ensuring cost-efficiency and scalability.
- **Automatic Scaling**: Services like Kinesis, Lambda, and S3 automatically scale up or down based on the volume of data, maintaining performance without manual intervention.
- **Cost Efficiency**: By using services that only charge for the compute and storage resources used, the solution remains economical regardless of data volume.
- **Flexibility**: The architecture is designed to handle varying data volumes efficiently, ensuring robust performance whether dealing with smaller or larger amounts of events.

---

**7. Would your proposed solution still be the same if adding fields / transforming the data is no longer
needed?**

Yes, the proposed solution would still be effective even if adding fields or transforming the data is no longer needed. Here’s why

- **Modular Design**: The architecture is modular, each component (ingestion, storage, processing) can function independently. If transformation is not needed, the relevant Lambda functions and Glue Jobs can be bypassed or simplified without affecting the rest of the system.
- **Direct Storage**: Data can be ingested directly into Amazon S3 via Kinesis Firehose without intermediate transformation steps, ensuring efficient data capture and storage.
- **Scalable Storage**: Amazon S3 will continue to provide scalable, cost-effective storage for raw data.
- **Efficient Querying**: The partitioning strategy and use of Parquet format for processed data can be maintained for efficient querying, even if no transformation is applied.
- **Pay-as-You-Use**: The pay-as-you-use model for AWS services ensures that you only pay for the resources you actually use, keeping costs low if certain processing steps are skipped.

### Adjusted Data Flow Without Transformation
1. **Direct Storage**: Data is stored directly in Amazon S3 (raw JSON files, compressed if needed).
2. **Metadata Management**: Glue Crawler updates the Data Catalog with schema information from the raw data.
3. **Advanced Analytics**: Databricks or other analytics tools can directly query and analyze the raw data stored in S3.

Though It required some code changes/config changes in downstream if upstream schema changes or transformations changes but overall architecture design remains same and works efficiently


---