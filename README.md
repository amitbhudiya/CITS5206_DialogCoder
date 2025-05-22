# DialogCoder (aka PulsarBurp)

A streamlined application to automate the coding of dialogue transcripts for research teams.


## Table of Contents

<details closed>
<summary> Click to open Table of Contents</summary

- [DialogCoder (aka PulsarBurp)](#dialogcoder-aka-pulsarburp)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Project Scope](#project-scope)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
- [Plan A - Keyword Matching (MVP)](#plan-a---keyword-matching-mvp)
  - [Getting Started with Plan A - MVP](#getting-started-with-plan-a---mvp)
    - [Prerequisites](#prerequisites)
    - [Installation / Setup](#installation--setup)
    - [Running the Streamlit App](#running-the-streamlit-app)
    - [In-App Guidance](#in-app-guidance)
    - [Using the Application (GUI)](#using-the-application-gui)
      - [1. Upload Your Coding Dictionary:](#1-upload-your-coding-dictionary)
      - [2. Upload Your Transcript Files:](#2-upload-your-transcript-files)
      - [3. Processing:](#3-processing)
      - [4. Frequency Table Reports (optional):](#4-frequency-table-reports-optional)
    - [Testing](#testing)
- [Plan B - LLM-assisted pipeline (POC)](#plan-b---llm-assisted-pipeline-poc)
  - [Getting Started with Plan B - LLM POC](#getting-started-with-plan-b---llm-poc)
    - [Installation / Setup](#installation--setup-1)
    - [Running the Streamlit App](#running-the-streamlit-app-1)
  - [Using the Application (GUI)](#using-the-application-gui-1)
      - [1. Upload Your Files:](#1-upload-your-files)
      - [2. Configure Confidence Settings:](#2-configure-confidence-settings)
      - [3. Run the Classification:](#3-run-the-classification)
      - [4. Review and Save Results:](#4-review-and-save-results)
    - [Testing](#testing-1)
  - [Additional Testing](#additional-testing)
  - [CI/CD](#cicd)
  - [Project Structure](#project-structure)

</details>

## Project Overview

**DialogCoder** (aka *PulsarBurp*) is a streamlined offline application designed to automate the qualitative coding of dialogue transcripts, particularly in research settings involving high-volume team interactions such as submarine simulator exercises. The tool eliminates repetitive manual work by tagging transcript rows based on a user-defined dictionary — or optionally, using LLM-enhanced classification.

This project includes two distinct pipelines:

- **Plan A (MVP):** A production-ready pipeline that uses rule-based keyword matching to code transcript data. Plan A was delivered as the **Minimum Viable Product (MVP)** and is fully functional for secure, offline use.
- **Plan B (POC):** A **proof-of-concept** pipeline that integrates Large Language Model (LLM) predictions via OpenRouter to enhance classification accuracy. Plan B is experimental and not part of the MVP.

## Project Scope

This project includes:

- Development of a user-friendly multi-page Streamlit web interface for Plan A.
- Implementation of a standalone demo UI for Plan B (LLM-enhanced).
- Support for automated coding of transcript CSV files using a predefined dictionary.
- Capability to process multiple files in batch.
- Generation of frequency reports summarizing code usage.
- Complete offline operation (Plan A) to safeguard sensitive data.
- CI/CD workflows for both pipelines using GitHub Actions.
- A comprehensive test suite including unit and end-to-end tests.

> ✅ **Note:** Only **Plan A** is part of the MVP and intended for production use. **Plan B** is a standalone **proof-of-concept** to explore LLM integration in this context.

## Features

- 🔍 **Automated Transcript Coding (Plan A)**  
  Apply a user-defined keyword dictionary to assign communication codes to dialogue rows in CSV transcript files.

- 📂 **Bulk File Processing**  
  Upload and process multiple transcripts simultaneously, dramatically reducing manual workload.

- 📊 **Frequency Summary Report**  
  Automatically generate summaries showing how often each communication code appears across transcripts.

- 🧱 **Modular Architecture**  
  Clean separation between keyword matching, UI logic, LLM dispatching, and persistence.

- 🔐 **Offline Operation (Plan A)**  
  Designed for secure environments — no internet connection is required to use the core MVP.

  - 🧠 **LLM-Augmented Classification (Plan B, optional)**  
  Use OpenRouter to classify dialogue lines when keyword matches are insufficient or ambiguous *(experimental)*.

- 🧪 **Robust Testing**  
  Unit tests, end-to-end tests, and isolated test suites for Plan A and Plan B pipelines.

- 🔄 **Continuous Integration**  
  GitHub Actions automate testing, linting, and CI checks for both pipelines with separate workflows.



## Tech Stack

**Frontend & Backend:** ![Streamlit](https://img.shields.io/badge/Streamlit-v1.28.0+-orange)
**Data Processing:** ![Python](https://img.shields.io/badge/Python-v3.11+-blue), ![Pandas](https://img.shields.io/badge/Pandas-v2.1.0+-blue)
**Testing:** ![Pytest](https://img.shields.io/badge/Pytest-v7.4.0+-blue), ![Selenium](https://img.shields.io/badge/Selenium-v4.11.0+-blue)
**CI/CD:** ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-blue)
**LLM Integration:** ![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM_API-green)



---

# Plan A - Keyword Matching (MVP)

## Getting Started with Plan A - MVP

Plan A is the **original, production-ready implementation** that uses a classic keyword matching approach to automate dialogue transcript coding. It provides a streamlined multi-page interface built with Streamlit and includes core components for transcript processing, coding dictionary management, and report generation, all contained within the `app/` directory.

<details closed>
<summary> Click to open the Plan A section</summary>

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation / Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CITS5206_DialogCoder.git
   cd CITS5206_DialogCoder
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Streamlit App

Start the Streamlit application:

```bash
streamlit run app/Home.py   # ← classic Plan A UI
```
Open a web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).


### In-App Guidance

**Each page of the application includes built-in instructions that clearly explain how to use its specific features**. These contextual guides walk you through uploading transcripts, selecting dictionaries, generating reports, and more—ensuring a smooth user experience without needing to refer back to external documentation. *For a specific workflow, please take a look at the next section: Using the Application (GUI)*


### Using the Application (GUI)

Here's how to use the app through the graphical interface, step by step of a typical workflow:

#### 1. Upload Your Coding Dictionary:
- Navigate to the Dictionary page from the sidebar
- Make sure your file meets for the formatting requirements specified on the page
- Upload your dictionary CSV file
- Modify if needed and then hit `save`

#### 2. Upload Your Transcript Files:
- Navigate to the Upload page from the sidebar
- Make sure your file meets for the formatting requirements specified on the page
- Upload your files

#### 3. Processing:
- Files will automatically begin to be processed as and when they are uploaded
- Preview of the results of the files will appear on the screen
- Summary statistics will be calculated concurrently
- You will be able to download each processed transcript individually

#### 4. Frequency Table Reports (optional):
- Navigate to the Reports page
- View the summary statistics for each uploaded CSV
- Download a frequency table of the codes aggregated over all uploads
  

### Testing

To verify the core functionality of the application, you can run unit tests. 
These tests validate individual components to ensure correctness and reliability.

**Run unit tests:**
```bash
pytest tests/unit/ -v
```

<details>
<summary>Click to view detailed functional testing documentation</summary>

<br>
A comprehensive functional testing document for Plan A is available in `functional_testing_planA.md`. This document covers:

- Test environment specifications
- 9 detailed test cases covering core functionality
- Test results and pass/fail criteria
- Known limitations and observations
- Testing conclusions and deployment readiness

The functional testing confirms that Plan A successfully implements all core features including file uploads, keyword matching, and report generation, with appropriate error handling and user feedback.
</details>
</details>

---

# Plan B - LLM-assisted pipeline (POC)

## Getting Started with Plan B - LLM POC

Plan B is an experimental, self-contained pipeline that augments the classic
keyword matcher with an LLM (via **OpenRouter**) and a small set of additional
components written under `planb/`.

>⚠️ Note: Plan B is a proof of concept and not part of the production-ready MVP. It is provided as an experimental extension for further exploration.

<details closed>
<summary> Click to open the Plan B section</summary>


### Installation / Setup

1. **Install Plan B specfic requirements**

   ```bash
   pip install -r planb/requirements-planb.txt
   ```

2. **Create a `.env` file** in the repo root with your API key (and optional threshold override):

   ```env
   OPENROUTER_API_KEY="sk-..."
   CONFIDENCE_THRESHOLD=0.50  # default is 0.50 if omitted
   ```

### Running the Streamlit App

Start the Streamlit application:

 ```bash
   streamlit run planb/ui/app.py #Plan B - UI
   ```
Open a web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).


## Using the Application (GUI)

Following is the instrcutions on how to navigate and use the program using the Graphical User Interface:

#### 1. Upload Your Files:
- Click "Upload transcript CSV or Excel file" on the left side
- Click "Upload dictionary CSV or Excel file" on the right side
- Success messages will confirm when files are loaded

#### 2. Configure Confidence Settings: 
- Use the "Confidence Threshold" slider to adjust how strict the matching should be:
   - Higher values (closer to 1.0): Only high-confidence matches
   - Lower values (closer to 0.0): More inclusive matching
   - Default (0.5): Balanced approach

#### 3. Run the Classification:
- Click the blue "Run Classification" button
- Wait while the system processes your files

#### 4. Review and Save Results:

- Review the color-coded results:
  - Green: High confidence matches (0.8+)
  - Yellow: Medium confidence matches (0.5-0.8)
  - Red: Low confidence matches (below 0.5)
  
- Click "Download Results CSV" to save the classified data

### Testing

The Plan B pipeline includes its own isolated test suite to ensure modular integrity and correct LLM-assisted behavior. These tests are lightweight and run quickly, making them ideal for rapid development and experimentation.


 **Run Plan B tests**:

   ```bash
   pytest -q tests/planb
   ```

</details>

---


## Additional Testing

To run additional tests across the broader app, you can also execute the end-to-end test suite and generate coverage reports.

Run end-to-end tests:
```bash
pytest tests/e2e/ -v
```

Run all tests with coverage:
```bash
pytest tests/ --cov=app -v
```
---

## CI/CD

This project uses GitHub Actions for continuous integration. Two workflows now
run in parallel:

1. **ci.yml** –  Plan A lint / unit / e2e tests
2. **planb-ci.yml** – lightweight Plan B pytest run (`tests/planb`)


Each workflow is triggered only when files relevant to that plan are modified.

The CI steps:
- Builds the application
- Runs linting checks
- Executes unit tests
- Performs end-to-end testing
- Verifies Streamlit startup 

---

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
---

