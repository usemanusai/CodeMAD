# Create ETL Pipeline Task

## Purpose

To design and implement robust, scalable ETL (Extract, Transform, Load) pipelines that efficiently process data from various sources to target destinations while ensuring data quality and reliability.

## Inputs

- Data Architecture Document
- Source System Specifications
- Target System Requirements
- Data Transformation Rules
- Performance and SLA Requirements

## Key Activities & Instructions

### 1. Confirm Interaction Mode

Ask the user: "How would you like to proceed with creating the ETL pipeline? We can work:
A. **Incrementally (Default & Recommended):** We'll design each pipeline component step-by-step.
B. **"YOLO" Mode:** I can design a complete ETL pipeline for you to review."

### 2. Pipeline Requirements Analysis

- **Source Analysis:** Analyze source systems, data formats, and extraction methods
- **Target Requirements:** Define target system requirements and data formats
- **Transformation Logic:** Document all data transformation and business rules
- **Performance Requirements:** Define throughput, latency, and SLA requirements
- **Error Handling:** Specify error handling and data quality requirements
- **Scheduling Requirements:** Define batch schedules and real-time processing needs

### 3. Pipeline Architecture Design

- **Pipeline Pattern:** Choose appropriate pattern (batch, streaming, micro-batch, lambda)
- **Tool Selection:** Select ETL tools and frameworks based on requirements
- **Infrastructure Design:** Plan compute, storage, and network infrastructure
- **Scalability Design:** Design for horizontal and vertical scaling
- **Monitoring Architecture:** Plan pipeline monitoring and observability
- **Security Architecture:** Design data security and access controls

### 4. Data Extraction Design

- **Source Connectors:** Design connectors for various source systems
- **Incremental Extraction:** Implement change data capture and incremental loading
- **Full vs Incremental:** Define strategies for full and incremental data loads
- **Data Validation:** Implement source data validation and quality checks
- **Error Recovery:** Design extraction error handling and retry mechanisms
- **Rate Limiting:** Implement rate limiting to avoid overwhelming source systems

### 5. Data Transformation Implementation

- **Data Cleansing:** Implement data cleaning and standardization logic
- **Data Enrichment:** Design data enrichment from reference data sources
- **Business Rules:** Implement complex business logic and calculations
- **Data Aggregation:** Design aggregation and summarization processes
- **Data Validation:** Implement transformation validation and quality checks
- **Schema Evolution:** Handle schema changes and data format evolution

### 6. Data Loading Strategy

- **Loading Patterns:** Implement appropriate loading patterns (insert, upsert, merge)
- **Batch vs Streaming:** Design batch and streaming loading mechanisms
- **Partitioning Strategy:** Implement data partitioning for performance
- **Indexing Strategy:** Design indexing for optimal query performance
- **Conflict Resolution:** Handle data conflicts and duplicate resolution
- **Transaction Management:** Ensure data consistency and transaction integrity

### 7. Pipeline Operations and Monitoring

- **Orchestration:** Implement workflow orchestration and dependency management
- **Monitoring and Alerting:** Set up comprehensive pipeline monitoring
- **Performance Optimization:** Implement performance tuning and optimization
- **Error Handling:** Design comprehensive error handling and notification
- **Data Quality Monitoring:** Implement ongoing data quality monitoring
- **Maintenance Procedures:** Document pipeline maintenance and troubleshooting

## Output Deliverables

- **ETL Pipeline Implementation** (complete pipeline code and configuration)
- **Pipeline Documentation** (`docs/etl-pipeline-{name}.md`)
- **Monitoring Dashboard** (pipeline health and performance monitoring)
- **Operational Runbooks** (troubleshooting and maintenance procedures)

## Key Resources

- **Template:** `templates#data-pipeline-tmpl`
- **Validation:** `checklists#data-pipeline-checklist`
- **User Preferences:** `data#technical-preferences`
