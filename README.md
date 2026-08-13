# 🛡️ Project VIGIL

**Autonomous AI Data Quality & Observability Platform**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://vigildataengine.streamlit.app)
[![Backend API](https://img.shields.io/badge/Backend_API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://vigil-api-rb4z.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 📊 The Problem We Solve

Data teams spend **60-80% of their time** manually debugging data pipelines—fixing null values, duplicates, outliers, and corrupted relationships. Companies lose **millions annually** to bad data, yet existing solutions are:
- ❌ **Reactive**: They alert you *after* the damage is done.
- ❌ **Black-box**: They don't explain *why* the data broke.
- ❌ **Manual**: They force engineers to write repetitive SQL fixes.

---

## 🎯 The Solution: Project VIGIL

Project VIGIL is an **autonomous, self-healing AI system** that continuously monitors data quality, detects hidden anomalies, and automatically generates fixes using a **Generative AI agent**—all while providing a single **Data Trust Score (0-100%)** for executive visibility.

### ✨ Key Highlights

- 📊 **Unified Data Trust Score:** Combines GX validation (20%) + ML anomaly detection (4.36% anomalies) into a single executive-friendly metric.
- 🧠 **ML & Deep Learning:** Built an **Isolation Forest** model and a **PyTorch Autoencoder** to detect 436 structural outliers across 10,000 customer records.
- 🤖 **GenAI Auto-Healing:** Engineered a **LangChain + Google Gemini** agent that autonomously generates corrective SQL, reducing manual debugging time by an estimated **70%**.
- 🔒 **Safety Layer:** Implemented a **safety critic agent** that reviews and blocks dangerous SQL commands (`DELETE`, `DROP`, `TRUNCATE`).
- ☁️ **Production Deployment:** Containerized with **Docker** and deployed on **Render** (FastAPI backend) + **Streamlit Cloud** (dashboard), with **CI/CD** and **24/7 uptime** via cron-job.org pings.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[Live Data Ingestion<br>Open-Meteo Weather API] --> B[(Neon PostgreSQL<br>Customers Table)]
    B --> C[Great Expectations<br>5 Automated Validation Rules]
    C --> D[Anomaly Detection<br>Isolation Forest + PyTorch Autoencoder]
    D --> E[Statistical Drift<br>KS-Test + Chi-Squared]
    E --> F[LangChain + Gemini<br>Auto-Healing Agent]
    F --> G[Critic Agent<br>SQL Safety Checker]
    G --> H[(Validation Reports DB<br>Data Trust Score History)]
    H --> I[FastAPI Backend<br>/trust-score, /drift, /run-validation]
    I --> J[Streamlit Dashboard<br>Live Data Trust Score 0-100%]
```

---

## 🚀 Features

### 1. Automated Data Validation
- **Great Expectations** runs **5+ automated validation rules**:
  - `expect_column_values_to_be_unique` (CustomerID)
  - `expect_column_values_to_be_between` (Age 18-100)
  - `expect_column_values_to_not_be_null` (Email)
  - `expect_column_values_to_match_regex` (Email format `.*@.*`)
  - `expect_column_values_to_be_between` (Purchase >= 0)
- **Result:** The data quality pipeline runs automatically on every new data batch.

### 2. Machine Learning & Deep Learning Anomaly Detection
- **Isolation Forest (Statistical ML):** Detects rare combinations (e.g., very old age + extremely high spending).
- **PyTorch Autoencoder (Deep Learning):** Learns "normal" data patterns and flags structural corruptions (broken relationships between columns).
- **Result:** **436 anomalies detected** (4.36% of the dataset) that Great Expectations rules could never catch.

### 3. Statistical Drift Detection
- **Kolmogorov-Smirnov (KS) Test:** Detects distribution shifts in numeric columns (`Age`, `purchase_amount`).
- **Chi-Squared Test:** Detects shifts in categorical columns (`Country`, `Gender`).
- **Result:** Early warning alerts for pipeline failures before they impact downstream applications.

### 4. GenAI Auto-Healing Agent
- **Healer Agent (LangChain + Google Gemini):** Reads the failed Great Expectations rules and generates a **corrective SQL script**.
- **Critic Agent:** Reviews the generated SQL for safety—blocks `DELETE`, `DROP`, and `TRUNCATE` statements.
- **Result:** Autonomous healing reduces manual debugging by an estimated **70%**.

### 5. Real-Time Data Ingestion
- Fetches live weather data from the **Open-Meteo API** (London) every time the user clicks the dashboard button.
- Transforms the weather JSON into a customer-like row and inserts it into the Neon database.

### 6. Unified Data Trust Score (0-100%)
| Layer | Weight | Current Score |
| :--- | :--- | :--- |
| Great Expectations (Rule Pass Rate) | 30% | 20.0% |
| Isolation Forest (Anomaly Rate Penalty) | 20% | 10% anomalies |
| PyTorch Autoencoder (Anomaly Rate Penalty) | 20% | 4.36% anomalies |
| **Final Data Trust Score** | 100% | **20.00%** |

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Language** | Python 3.13 |
| **Database** | Neon (PostgreSQL), SQLAlchemy, psycopg2-binary |
| **Data Validation** | Great Expectations |
| **ML/DL** | PyOD (Isolation Forest), PyTorch (Autoencoder), Scikit-learn, SciPy |
| **Generative AI** | LangChain, Google Gemini API |
| **Backend** | FastAPI, Pydantic, Uvicorn |
| **Frontend** | Streamlit |
| **DevOps** | Docker, Render, Streamlit Cloud, CI/CD (GitHub Actions), cron-job.org |
| **Security** | python-dotenv, .env files |

---

## 📂 Repository Structure

```
vigil/
├── data/
│   ├── messy_customer_data.csv          # Raw data (10,000 rows)
│   └── cleaned_customers.csv            # ML-ready data
├── notebooks/
│   ├── 03_preprocessing_feature_engineering.ipynb
│   ├── 03_2_isolation_forest.ipynb
│   └── 03_3_autoencoder.ipynb
├── src/
│   ├── __init__.py
│   ├── api.py                           # FastAPI backend (/trust-score, /drift, /run-validation)
│   ├── validator.py                     # Great Expectations validation
│   ├── reporter.py                      # Data Trust Score reporting
│   ├── agent.py                         # GenAI auto-healing agent
│   ├── critic.py                        # SQL safety critic agent
│   ├── drift_detector.py                # KS-Test & Chi-Squared drift detection
│   ├── data_ingestor.py                 # Live weather data ingestion
│   ├── database.py                      # Neon connection
│   ├── logger.py                        # JSON structured logging
│   └── utils.py                         # Utility functions
├── tests/
│   ├── test_utils.py                    # 9 unit tests (100% coverage)
│   └── __init__.py
├── app.py                                # Streamlit dashboard
├── Dockerfile.api                        # Backend container
├── Dockerfile.ui                         # Frontend container
├── docker-compose.yml                    # Multi-container orchestration
├── requirements.txt                      # Python dependencies
├── .env                                  # Secrets (ignored by Git)
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Poetry (for dependency management)
- Neon PostgreSQL account (free tier)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/GaddeBhanu9/vigil.git
cd vigil

# 2. Install dependencies with Poetry
poetry install

# 3. Activate the virtual environment
poetry shell

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your DATABASE_URL and GEMINI_API_KEY

# 5. Run the FastAPI backend
poetry run uvicorn src.api:app --reload

# 6. Run the Streamlit dashboard (in a new terminal)
poetry run streamlit run app.py
```

### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL="postgresql://username:password@hostname/database_name?sslmode=require"
GEMINI_API_KEY="your_google_gemini_api_key"
API_URL="https://vigil-api-rb4z.onrender.com"  # For production
```

### Running with Docker

```bash
# Build and run both services
docker-compose up -d --build

# Check running containers
docker ps

# Access the dashboard
# http://localhost:8501
```

---

## 🧪 Testing

```bash
# Run all unit tests
poetry run pytest

# Run tests with coverage report
poetry run pytest --cov=src --cov-report=term

# Coverage is currently 100%
```

---

## 🌐 Live Deployment

| Service | URL | Status |
| :--- | :--- | :--- |
| **Dashboard (Streamlit)** | [https://vigildataengine.streamlit.app](https://vigildataengine.streamlit.app) | ✅ Live |
| **Backend (FastAPI)** | [https://vigil-api-rb4z.onrender.com](https://vigil-api-rb4z.onrender.com) | ✅ Live |
| **API Documentation** | [https://vigil-api-rb4z.onrender.com/docs](https://vigil-api-rb4z.onrender.com/docs) | ✅ Swagger UI |

---

## 📊 Key Metrics

| Metric | Value |
| :--- | :--- |
| **Total Rows in Dataset** | 10,000 |
| **Great Expectations Rules** | 5 (1 passed, 4 failed) |
| **Isolation Forest Anomalies** | ~10% |
| **Autoencoder Anomalies** | 436 (4.36%) |
| **Data Trust Score** | 20.00% |
| **Unit Test Coverage** | 100% |
| **Estimated Debugging Reduction** | 70% |

---

## 👤 Author

**Gadde Bhanu Prakash**

- [GitHub](https://github.com/GaddeBhanu9)
- [LinkedIn](https://www.linkedin.com/in/gadde-bhanu-prakash-26aa74389)
- [Portfolio](https://gaddebhanu9.github.io/Portifolio/)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Open-Meteo** for providing free real-time weather data.
- **Google Gemini** for powering the auto-healing agent.
- **Neon** for the free serverless PostgreSQL database.
- **Render** and **Streamlit Cloud** for free hosting.
- **Great Expectations** for the data validation framework.
- **LangChain** for the agent framework.

---

<div align="center">
  ⭐ If you find this project useful, please give it a star! ⭐
</div>
