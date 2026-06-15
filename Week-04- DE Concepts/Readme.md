# ☁️WEEK - 4 Azure Cloud Fundamentals & Data Pipeline Implementation

### 🎯 Objective
To build a scalable data integration solution by deploying Azure cloud infrastructure and orchestrating an automated data movement pipeline using Azure Data Factory (ADF). 

### 🛠️ Tech Stack & Services Used
* **Microsoft Azure Cloud** (Portal, Resource Groups, IAM)
* **Azure Blob Storage** (Data Lake storage layer)
* **Azure Data Factory (ADF)** (Data Orchestration, ETL/ELT)

---

## 🏗️ Project Architecture & Workflow
1. **Infrastructure Provisioning:** Created a centralized Resource Group to manage all Azure assets securely.
2. **Data Ingestion (Source):** Configured a Storage Account and Blob Container to house the raw CSV data files.
3. **Integration Setup:** Established secure Linked Services connecting ADF to the Blob Storage.
4. **Data Orchestration:** Designed an ADF pipeline utilizing **Get Metadata** and **Copy Data** activities to validate and migrate data to a new destination.
5. **Security & Governance:** Implemented Role-Based Access Control (RBAC) assigning specific operational roles.

---

## 📸 Implementation Steps & Evidence

### 1. Resource Group Configuration
A dedicated Resource Group was created to logically group the pipeline's resources, ensuring clean cost tracking and deployment life cycle management.

### 2. Azure Storage Setup
Provisioned an Azure Storage Account and created designated Blob containers. Uploaded the raw source CSV file to act as the data origin.

### 3. Azure Data Factory (Linked Services & Datasets)
Configured ADF by establishing a Linked Service to securely authenticate with Blob Storage. Created distinct datasets to accurately define the schema for both the Source and Destination.

### 4. Pipeline Development & Metadata Validation
Designed the core orchestration pipeline. Integrated a **Get Metadata** activity to dynamically validate file properties prior to execution, followed by a **Copy Data** activity to securely process the data payload.

---

## 💡 Key Learnings & Business Impact
* **Cloud Infrastructure Management:** Gained practical experience in provisioning, managing, and connecting enterprise-grade Azure resources.
* **Metadata-Driven Pipelines:** Learned how to build dynamic, error-resistant pipelines by checking dataset properties before initiating heavy data transfers.
* **Security Best Practices:** Applied the Principle of Least Privilege (PoLP) by managing IAM Reader and Contributor roles for secure access to the storage layers.

  ## 👩‍💻 Author
Nidhi Bansal Celebal Technologies — Data Engineering Intern

⭐ Star this repo if you found it helpful!
