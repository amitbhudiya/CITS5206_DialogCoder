# Functional Testing Document - Plan A (Keyword Matching)

## 1. **Introduction**

### 1.1 Purpose

The purpose of this functional testing is to ensure that the **DialogCoder (Plan A)** performs as expected and meets the specified functional requirements. This document outlines the tests performed on key platform functionalities, including transcript upload, dictionary management, and automated coding.

### 1.2 Scope

The functional testing covers the following features of the platform:

- Transcript CSV file upload functionality
- Dictionary CSV file upload and management
- Automated keyword-based coding of dialogue transcripts
- Report generation and frequency analysis
- Results visualization and export

Out of scope:
- Performance testing under high volume
- Security testing
- Plan B (LLM-assisted) functionality

## 2. **Test Environment**

### 2.1 Hardware

- **Processor**: Intel Core i7/AMD Ryzen 7 or equivalent
- **RAM**: 8 GB minimum
- **Storage**: 256 GB SSD
- **Operating System**: Windows 10/11, macOS, or Linux

### 2.2 Software

- **Python Version**: 3.11+
- **Streamlit Version**: 1.44.1
- **Pandas Version**: 2.2.3
- **Matplotlib Version**: 3.10.1

### 2.3 Test Data

- Sample transcript CSV files with 100-500 rows of dialogue
- Sample dictionary CSV files with predefined keywords and codes
- Various column layouts to test column inference

## 3. **Test Objectives**

The main objectives of the testing are:

- Ensure transcript CSV files can be uploaded successfully
- Verify that dictionary files are correctly processed
- Confirm that keyword matching accurately assigns codes based on the dictionary
- Ensure report generation provides expected frequency analyses
- Verify error handling works as expected (invalid files, missing columns)
- Confirm results can be exported in the expected format

## 4. **Test Cases**

### 4.1 Test Case Summary

| Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Status |
| ------- | ----------- | ------------- | ---------- | --------------- | ------------- | ------ |
| TC001 | Test application startup | Python and dependencies installed | 1. Run `streamlit run app/Home.py`<br>2. Observe home page | Application starts and displays home page with navigation | Application starts correctly | Pass |
| TC002 | Test transcript CSV upload | Application running | 1. Navigate to Upload page<br>2. Upload valid transcript CSV<br>3. Verify file loads | Transcript file uploads, success message displayed, preview shown | File uploads successfully | Pass |
| TC003 | Test dictionary CSV upload | Application running | 1. Navigate to Upload page<br>2. Upload valid dictionary CSV<br>3. Verify file loads | Dictionary file uploads, success message displayed, preview shown | File uploads successfully | Pass |
| TC004 | Test keyword matching processing | Transcript and dictionary uploaded (TC002, TC003) | 1. Click "Process" button<br>2. Wait for processing<br>3. View results | Results table shows transcript with added code column based on keyword matches | Processing completes correctly | Pass |
| TC005 | Test results download | Processing completed (TC004) | 1. Click "Download Results" button<br>2. Check downloaded file | CSV file downloads with original data plus coding columns | File downloads correctly | Pass |
| TC006 | Test frequency report generation | Processing completed (TC004) | 1. Navigate to Reports page<br>2. Select options<br>3. Generate report | Frequency report displays showing code distribution | Report generates correctly | Pass |
| TC007 | Test invalid CSV upload | Application running | 1. Upload invalid file format<br>2. Observe response | Error message displayed, invalid file rejected | Error handled correctly | Pass |
| TC008 | Test missing column handling | Application running | 1. Upload CSV without required columns<br>2. Observe response | Warning about missing columns, option to select alternatives | Warning displayed correctly | Pass |
| TC009 | Test bulk processing | Application running | 1. Upload multiple transcript files<br>2. Upload dictionary<br>3. Process all files | All files processed sequentially, results available for each | Bulk processing works | Pass |

## 5. **Test Results Summary**

### 5.1 Summary

In total, 9 test cases were executed for Plan A functionality. All test cases passed, indicating that the core keyword-matching functions are working as expected.

- **Total Test Cases**: 9
- **Pass**: 9
- **Fail**: 0

### 5.2 Pass/Fail Criteria

- A test case is marked as **Pass** if the actual result matches the expected result.
- A test case is marked as **Fail** if the actual result does not match the expected result or the function breaks during testing.

## 6. **Issues and Bugs**

No critical issues were identified during functional testing of Plan A. Minor observations include:

- **Observation**: Large CSV files (>10,000 rows) may cause slower processing times
  - **Impact**: Minimal impact on functionality; only affects user experience with very large datasets
  - **Possible Solution**: Consider implementing batch processing or progress indicators for large files

## 7. **Conclusion**

The functional testing for **DialogCoder Plan A** was successfully completed. All core functionalities, including file uploads, keyword matching, and report generation, worked as expected. The application handles errors appropriately and provides clear feedback to users. Plan A is ready for user acceptance testing and deployment. 