
# ☁️ WEEK - 4 — Azure Cloud Fundamentals & Data Pipeline Implementation

![Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![ADF](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Blob Storage](https://img.shields.io/badge/Azure_Blob_Storage-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Status](https://img.shields.io/badge/Pipeline-Succeeded%20✅-brightgreen?style=for-the-badge)

---

## 🎯 Objective

To build a scalable data integration solution by deploying Azure cloud infrastructure and orchestrating an automated data movement pipeline using **Azure Data Factory (ADF)**.

---

## 🛠️ Tech Stack & Services Used

| Service | Purpose |
|--------|---------|
| Microsoft Azure Portal | Cloud console for provisioning all resources |
| Azure Resource Groups | Logical container for managing all project assets |
| Azure Blob Storage | Data Lake storage layer for source and destination CSV files |
| Azure Data Factory (ADF) | Data Orchestration, ETL/ELT pipeline execution |
| Azure IAM (RBAC) | Role-Based Access Control for secure access management |

---

## 🏗️ Project Architecture & Workflow

```
[Sample - Superstore.csv]
        |
        ▼
[Blob Container: source-data]
        |
        ▼
[ADF Linked Service: ls_AzureBlobStorage]
        |
        ▼
[Dataset: ds_SourceCSV]
        |
        ▼
[Get Metadata Activity] ──► itemName, size, columnCount, lastModified
        |
        ▼ (on success)
[Copy Data Activity]
        |
        ▼
[Dataset: ds_DestinationCSV]
        |
        ▼
[Blob Container: destination-data/output_superstore.csv] ✅
```

---

## 📸 Implementation Steps & Evidence

### 1. 🗂️ Resource Group Configuration
A dedicated Resource Group `rg-adf-assignment` was created in **Central India** under the **Azure for Students** subscription to logically group all pipeline resources, ensuring clean cost tracking and deployment lifecycle management.

> **Screenshot:** Resource Group overview showing name, location, and subscription.

---

### 2. 💾 Azure Storage Setup
Provisioned an Azure Storage Account `stgadfnidhi2024` (Standard LRS) and created two designated Blob containers:
- `source-data` — holds the raw input CSV file
- `destination-data` — receives the processed output file

Uploaded **Sample - Superstore.csv** (2.18 MiB) as the data origin.

> **Screenshot:** `source-data` container with uploaded CSV file visible.

---

### 3. 🔗 Azure Data Factory — Linked Services & Datasets
- Created ADF instance `adf-pipeline-nidhi` (V2) in Central India
- Configured Linked Service `ls_AzureBlobStorage` to securely authenticate with Blob Storage using Account Key
- Created two datasets:
  - `ds_SourceCSV` → points to `source-data/Sample - Superstore.csv`
  - `ds_DestinationCSV` → points to `destination-data/output_superstore.csv`

> **Screenshot:** Linked Service showing "Connection successful" status.  
> **Screenshot:** Both datasets listed in ADF Author panel.

---

### 4. 🔍 Pipeline Development & Metadata Validation
Designed pipeline `pl_CopySuperstoreData` with two chained activities:

**Get Metadata Activity**
- Dataset: `ds_SourceCSV`
- Field list retrieved: `itemName`, `size`, `columnCount`, `lastModified`
- Dynamically validates file properties before initiating data transfer

**Copy Data Activity** (triggered on Get Metadata success)
- Source: `ds_SourceCSV`
- Sink: `ds_DestinationCSV`
- Fault tolerance: Skip incompatible rows
- Result: **5,009 rows copied successfully**

> **Screenshot:** Pipeline canvas showing Get Metadata → Copy Data connected.

---

### 5. ▶️ Pipeline Execution Results

| Activity | Status | Duration |
|----------|--------|----------|
| Get Metadata1 | ✅ Succeeded | 13s |
| Copy data1 | ✅ Succeeded | 17s |

Output file `output_superstore.csv` (2.5 MiB) confirmed in `destination-data` container.

> **Screenshot:** Debug output showing both activities Succeeded.  
> **Screenshot:** `destination-data` container with `output_superstore.csv`.

---

### 6. 🔐 IAM Role Assignments (RBAC)

Roles assigned at Resource Group `rg-adf-assignment` scope:

| Role | Assigned To | Type |
|------|------------|------|
| Owner | Nidhi Bansal | User |
| Contributor | Nidhi Bansal | User |
| Reader | Nidhi Bansal | User |
| Storage Blob Data Contributor | adf-pipeline-nidhi | Managed Identity |

> **Screenshot:** IAM Role Assignments page showing all four roles.

---

## 💡 Key Learnings & Business Impact

- **Cloud Infrastructure Management** — Gained practical experience in provisioning, managing, and connecting enterprise-grade Azure resources end-to-end.
- **Metadata-Driven Pipelines** — Learned how to build dynamic, error-resistant pipelines by validating dataset properties before initiating heavy data transfers.
- **Security Best Practices** — Applied the **Principle of Least Privilege (PoLP)** by managing IAM Reader and Contributor roles for secure, scoped access to storage layers.
- **ADF Core Concepts** — Understood the relationship between Linked Services, Datasets, Activities, and Pipelines as building blocks of enterprise ETL workflows.
- **Managed Identity Authentication** — Configured passwordless, secure service-to-service authentication between ADF and Azure Blob Storage.

---

## 📁 Repository Structure

```
WEEK-4-azure-adf-pipeline/
│
├── README.md
├── screenshot/
│   ├── 1-Resource Group.png
│   ├── 2-Storage Setup.png
│   ├── 2- csv uploaded.png
│   ├── 3- linked.png
│   ├── 3-source.png
│   ├── 3-destination.png
│   ├── 3-metadata.png
│   ├── 4-pipeline design.png
│   ├── 5-pipeline execution.png
│   ├── 6-Roles.png
│   └── output.png
└── Datasets/
    └── Sample - Superstore.csv
```

---

## 👩‍💻 Author

**Nidhi Bansal**  
Celebal Technologies — Data Engineering Intern  

---

⭐ **Star this repo if you found it helpful!**
