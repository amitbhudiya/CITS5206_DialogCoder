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
    - [Running the App](#running-the-app)
  - [Testing](#testing)
    - [Running Tests](#running-tests)
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

### Running the App

Start the Streamlit application:

```bash
streamlit run app/Home.py
```

The application will be available at http://localhost:8501 in your web browser.

## Testing

### Running Tests

Run unit tests:
```bash
pytest tests/unit/ -v
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
├── tests/                # Test suite
│   ├── e2e/              # End-to-end browser tests
│   ├── unit/             # Unit tests
│   └── sample_files/     # Test data
└── .github/              # CI/CD configuration
```

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow:
- Builds the application
- Runs linting checks
- Executes unit tests
- Performs end-to-end testing
- Verifies Streamlit startup