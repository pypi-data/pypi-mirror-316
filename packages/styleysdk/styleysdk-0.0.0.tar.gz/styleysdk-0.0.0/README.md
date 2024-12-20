# Styley Python SDK

## 📚 **Table of Contents**
1. [Introduction](#introduction)
2. [Install Python](#install-python)
3. [Verify Installation](#verify-installation)
4. [Install SDK](#install-sdk)
5. [Environment Variables](#environment-variables)
6. [Usage](#usage)
    - [Deployments](#deployments)
    - [Models](#models)
7. [Class & Method Reference](#class--method-reference)

---

## **Introduction**
The **Styley Python SDK** provides a simple and intuitive interface to interact with Styley’s deployment and model services. With this SDK, you can easily create and manage deployments, query models, and retrieve job statuses programmatically.

---

## *Install Python*

Install Using Official Installer (Recommended)

1. **Download Python**
    - Visit [Python official download page](https://www.python.org/downloads/).
    - Download the installer for your operating system:
      - **Windows**: Download the `.exe` file.
      - **MacOS**: Download the `.pkg` file.
      - **Linux**: Use the system's package manager (e.g., `apt`, `yum`).

2. **Run the installer**
    - Check **Add Python to PATH** (important).
    - Select **Install Now**.

3. **Restart your terminal** after the installation.

---

## **Verify Installation**

Ensure Python and pip are installed correctly.

```bash
python --version
pip --version
```

Expected output:

```bash
Python 3.10.0  # Example version
pip 23.1.2     # Example pip version
```

If you see "command not found", double-check if Python is installed and in your PATH.

---

## **Install SDK**

Install the Python SDK via pip:

```bash
pip install styleysdk
```

This installs the Styley SDK and its dependencies.

---

## **Environment Variables**

To authenticate API requests, set the following environment variable:

```bash
export X_STYLEY_KEY=***************************
```

---

# **Usage**

This section covers available methods for interacting with deployments and models.

---

##  **Deployments**

### 📤 **Create Deployment**

The **Create Deployment** method allows you to create a new deployment using a `model name` and `arguments`. It returns an output with a `job_id` that you can use to fetch the final results.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
deployment = styley.deployments.create(
    deployment=CreateDeployment(
        name="Translate Pro",
        model="e77a0be0-dedb-4f9d-acf6-9878df149d33",
        args={
            "Target_Language": "SL",
            "Text": "what is how",
        }
    )
)
print(deployment)
```

---

### 📄 **Get Deployment By ID**

Fetch details of a specific deployment using its deployment ID.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
deployment_details = styley.deployments.get_by_id(deployment_id)
print(deployment_details)
```

---

### 📜 **List Deployments**

Retrieve a list of all deployments.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
deployments_list = styley.deployments.list()
print(deployments_list)
```

---

### 🚀 **Get Deployment Job**

Get the status of a deployment job using its job ID.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
job_status = styley.deployments.get_job(job_id)
print(job_status)
```

---

# **Models**

### 📜 **List Models**

Retrieve a list of all models available for deployments.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
models_list = styley.models.list()
print(models_list)
```

---

### 🔍 **Get Model By ID**

Fetch a specific model’s details using its model ID.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
model_details = styley.models.get_by_id(model_id)
print(model_details)
```

---

### 🔍 **Get Model By Name**

Fetch a specific model’s details using its model name.

**Example:**

```python
from styleysdk import Styley
from styleysdk.deployments.model import CreateDeployment
from styleysdk.deployments.model import Job

styley = Styley()
model_details = styley.models.get_by_name(model_name)
print(model_details)
```

---

# **Class & Method Reference**

| **Class**       | **Method**       | **Description**                            |
|-----------------|-----------------|------------------------------------------|
| **Deployments** | `create(payload)`| Create a new deployment.                  |
| **Deployments** | `get_by_id(id)`  | Get deployment details by deployment ID.  |
| **Deployments** | `list()`         | List all deployments.                     |
| **Deployments** | `get_job(job_id)`| Get the status of a deployment job.       |
| **Models**      | `list()`         | List all available models.                |
| **Models**      | `get_by_id(id)`  | Get model details by model ID.            |
| **Models**      | `get_by_name(name)`| Get model details by model name.         |

---


