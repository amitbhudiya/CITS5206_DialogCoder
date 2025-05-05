# DialogCoder

A streamlined application to automate the coding of dialogue transcripts for research teams.

## Table of Contents
- [DialogCoder](#dialogcoder)
  - [Table of Contents](#table-of-contents)
  - [Problem Statement](#problem-statement)
    - [Overview](#overview)
    - [The Current Challenge](#the-current-challenge)
    - [Why This Solution](#why-this-solution)
  - [Key Features](#key-features)
  - [Tech Stack](#tech-stack)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Plan B (LLM-assisted pipeline)](#plan-b-llm-assisted-pipeline)
    - [Running the App](#running-the-app)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
- [Plan B tests (27 fast unit tests)](#plan-b-tests-27-fast-unit-tests)
    - [Test Types](#test-types)
  - [Project Structure](#project-structure)
  - [CI/CD](#cicd)

## Problem Statement

### Overview

Researchers analyzing submarine simulator team exercises face a labor-intensive challenge. Each one-hour voice recording is transcribed into a CSV file containing 400–500 dialogue rows, which must be manually coded by two independent raters. This manual process is slow, prone to error, and not scalable as the volume of data increases.

### The Current Challenge

- **Time-Intensive Process:** Manually coding extensive transcripts takes hours per file.
- **Human Error and Inconsistency:** Repetitive tasks lead to potential mistakes and varying interpretations.
- **Scalability Issues:** As data volume grows, the manual method becomes increasingly unmanageable.
- **Coder Fatigue:** Monotonous work increases the likelihood of oversight and reduces overall accuracy.

### Why This Solution

The application transforms a repetitive, error-prone manual process into an efficient, automated workflow. By leveraging a user-defined dictionary of keywords and phrases, the software will:

- **Reduce Processing Time:** Automate coding to turn hours of work into minutes.
- **Ensure Consistency:** Apply a predefined qualitative coding frame uniformly across all transcripts.
- **Support Scalability:** Handle bulk uploads of transcripts, making it feasible to process large datasets.
- **Enhance Data Security:** Operate entirely offline to ensure sensitive information remains secure.
- **Improve Resource Allocation:** Allow researchers to focus on higher-value analysis rather than manual coding tasks.

## Key Features

1. **Automated Transcript Coding:**
   - Process CSV transcripts by mapping each dialogue row to a communication category based on a user-defined keyword dictionary.
   - Append a new column to each CSV file with the assigned code.

2. **Bulk Data Processing:**
   - Enable simultaneous processing of multiple CSV files to efficiently handle large volumes of data.

3. **Frequency Summary Report:**
   - Generate summary reports that provide frequency counts for each communication code across the dataset.

4. **Offline Operation:**
   - Ensure the application functions entirely offline, keeping all sensitive data secure and eliminating dependency on external services.

## Tech Stack

- **Frontend & Backend:** Streamlit
- **Data Processing:** Python, Pandas
- **Testing:** Pytest, Selenium
- **CI/CD:** GitHub Actions

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CITS5206_DialogCoder.git
   cd CITS5206_DialogCoder
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Plan B (LLM-assisted pipeline)

Plan B is an experimental, self-contained pipeline that augments the classic
keyword matcher with an LLM (via **OpenRouter**) and a small set of additional
components written under `planb/`.

1. **Install Plan B requirements**

   ```bash
   pip install -r planb/requirements-planb.txt
   ```

2. **Create a `.env` file** in the repo root with your API key (and optional
   threshold override):

   ```env
   OPENROUTER_API_KEY="sk-..."
   CONFIDENCE_THRESHOLD=0.50  # default is 0.50 if omitted
   ```

3. **Run the demo UI** (separate from the classic Streamlit multipage app):

   ```bash
   streamlit run planb/ui/app.py
   ```

4. **Run Plan B tests** (27 fast unit tests):

   ```bash
   pytest -q tests/planb
   ```

The Plan B workflow is isolated from Plan A: it has its own dependencies, test
suite and GitHub Action (`.github/workflows/planb-ci.yml`).

### Running the App

Start the Streamlit application:

```bash
streamlit run app/Home.py            # ← classic Plan A UI

## Plan B Demo UI (LLM-assisted)

```bash
streamlit run planb/ui/app.py        # ← experimental Plan B interface
```

The application will be available at http://localhost:8501 in your web browser.

## Testing

### Running Tests

Run unit tests:
```bash
pytest tests/unit/ -v
```

# Plan B tests (27 fast unit tests)
```bash
pytest -q tests/planb
```

Run end-to-end tests:
```bash
pytest tests/e2e/ -v
```

Run all tests with coverage:
```bash
pytest tests/ --cov=app -v
```

### Test Types

- **Unit Tests:** Fast tests that validate individual functions and components
- **End-to-End Tests:** Browser-based tests that validate the complete application workflow

## Project Structure

```
CITS5206_DialogCoder/
├── app/                  # Main application code
│   ├── Home.py           # Streamlit entry point
│   ├── pages/            # Additional Streamlit pages
│   └── services/         # Business logic
├── planb/                # **Plan B** — self-contained LLM pipeline
│   ├── ui/               # Streamlit single-page demo
│   ├── controller/       # Dispatcher / orchestration
│   ├── pipeline/         # Keyword → LLM → Aggregator components
│   ├── column_inference/ # Helpers to map dictionary columns
│   ├── persistence/      # CSV exporter
│   ├── logging/          # Minimal logger stub
│   ├── manual-test-files/# Sample CSVs for quick experimentation
│   └── requirements-planb.txt
├── tests/                # Test suite
│   ├── e2e/              # End-to-end browser tests
│   ├── unit/             # Unit tests (Plan A)
│   └── planb/            # 🆕  Plan B unit tests (27 passing)
│   └── sample_files/     # Test data
└── .github/              # CI/CD configuration
    ├── workflows/ci.yml        # Plan A checks
    └── workflows/planb-ci.yml  # Plan B checks
```

## CI/CD

This project uses GitHub Actions for continuous integration. Two workflows now
run in parallel:

1. **ci.yml** – legacy Plan A lint / unit / e2e tests
2. **planb-ci.yml** – lightweight Plan B pytest run (`tests/planb`)

Each workflow is triggered only when files relevant to that plan are modified.

The CI steps:
- Builds the application
- Runs linting checks
- Executes unit tests
- Performs end-to-end testing
- Verifies Streamlit startup 
