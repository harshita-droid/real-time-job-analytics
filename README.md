
# Real-Time Job Analytics Pipeline

## 📌 Overview

This project demonstrates a **real-time data analytics pipeline** that ingests live events from a public API, streams them through AWS services, and prepares the data for large-scale analytics processing.

The goal of this project is to simulate **real-world data engineering use cases**, such as:

- Real-time ingestion  
- Event-driven architecture  
- Scalable streaming pipelines  
- Cloud-native design  

This project is designed to be **resume-ready and interview-ready**.

---

## 🏗️ System Architecture

```
GitHub Events API
        |
        | (Continuous Polling)
        v
Python Producer (Microservice)
        |
        | (Streaming Events)
        v
AWS Kinesis Data Stream
        |
        | (Next Phase)
        v
Firehose → AWS S3 (Raw / Bronze)
        |
        v
Azure Databricks (Structured Streaming)
```

---

## 🚀 Key Features

- Near real-time data ingestion  
- REST API → Streaming conversion  
- Event-driven pipeline using AWS Kinesis  
- Fault-tolerant and scalable design  
- Secure IAM-based access  
- Production-grade logging  
- Defensive schema handling  

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Language | Python |
| API Source | GitHub Events API |
| Streaming | AWS Kinesis Data Streams |
| Cloud | AWS |
| Security | AWS IAM |
| Logging | Python logging |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```
real-time-job-analytics/
│
├── data-producer/
│   └── github_events_producer.py
│
├── README.md
```

---

## 🔑 Prerequisites

Before running this project, ensure you have:

- Python 3.8+  
- AWS account  
- AWS CLI installed  
- Git installed  
- IAM user with required permissions  
- Active AWS Kinesis Data Stream  

---

## 🔐 IAM Permissions

The Python producer uses a **least-privilege IAM policy**.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:PutRecord",
        "kinesis:PutRecords",
        "kinesis:DescribeStream",
        "kinesis:DescribeStreamSummary"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## ⚙️ AWS Setup

### 1️⃣ Create Kinesis Data Stream

- Stream Name: `job-analytics-stream`
- Region: `ap-south-1`
- Capacity Mode: On-demand

### 2️⃣ Configure AWS Credentials Locally

```bash
aws configure
```

Verify configuration:

```bash
aws sts get-caller-identity
```

---

## 🐍 Python Environment Setup

Install required dependencies:

```bash
pip install boto3 requests
```

---

## ▶️ Running the Application

Navigate to the producer directory:

```bash
cd data-producer
python github_events_producer.py
```

### Sample Output

```
INFO GitHub Events Producer started
INFO Sent 30 events to Kinesis
INFO Sent 30 events to Kinesis
```

---

## 📊 Data Validation in Kinesis

To verify ingestion:

1. Open AWS Console  
2. Navigate to **Kinesis Data Streams**  
3. Select `job-analytics-stream`  
4. Open **Monitoring** tab  
5. Check:
   - IncomingRecords  
   - IncomingBytes  

Optional:
- Use **Data Viewer**
- Shard → `ShardId-000000000000`
- Start Position → `Latest`

---

## 🧠 Design Decisions

### 🔹 API to Streaming Conversion
The GitHub Events API is request-based.  
A continuously running Python service converts API responses into streaming events.

### 🔹 Partition Key Strategy

```python
PartitionKey = event.get("event_type", "UNKNOWN")
```

- Maintains ordering per event type  
- Prevents pipeline failure on missing fields  
- Enables scalable shard distribution  

### 🔹 Defensive Data Handling

- Uses `.get()` for schema tolerance  
- Prevents pipeline crashes  
- Captures malformed records for analysis  

### 🔹 Timezone-Aware Timestamps

All timestamps are stored in **UTC** using timezone-aware datetime objects.

---

## 🪵 Logging Strategy

The application uses Python’s `logging` module instead of `print()`:

- Structured logs  
- Severity levels  
- Better observability  

Example:

```
2025-01-05 11:10:25 INFO Sent 30 events to Kinesis
```

---

## 🔮 Future Enhancements

- Kinesis Firehose → S3 (Raw / Bronze layer)  
- Databricks Structured Streaming  
- Delta Lake tables  
- Data quality checks  
- Alerting & monitoring  
- Dashboarding  

---

## 🎯 Interview Relevance

This project demonstrates:

- Real-time data ingestion  
- Streaming architecture  
- Cloud-native data engineering  
- IAM security best practices  
- Production-ready Python coding  

---

## ✅ Conclusion

This project simulates a **real-world real-time analytics pipeline** and serves as a strong foundation for advanced big data processing using **Databricks** and **Delta Lake**.
