# CITS5206_DialogCoder

## Problem Statement: What Are We Building and Why?

### Overview
Researchers analyzing submarine simulator team exercises face a labor-intensive challenge. Each one-hour voice recording is transcribed into a CSV file containing 400–500 dialogue rows, which must be manually coded by two independent raters. This manual process is slow, prone to error, and not scalable as the volume of data increases.

### The Current Challenge
- **Time-Intensive Process:** Manually coding extensive transcripts takes hours per file.
- **Human Error and Inconsistency:** Repetitive tasks lead to potential mistakes and varying interpretations.
- **Scalability Issues:** As data volume grows, the manual method becomes increasingly unmanageable.
- **Coder Fatigue:** Monotonous work increases the likelihood of oversight and reduces overall accuracy.

### Why the Client Wants This Software
The client is seeking a solution that transforms a repetitive, error-prone manual process into an efficient, automated workflow. By leveraging a user-defined dictionary of keywords and phrases, the software will:
- **Reduce Processing Time:** Automate coding to turn hours of work into minutes.
- **Ensure Consistency:** Apply a predefined qualitative coding frame uniformly across all transcripts.
- **Support Scalability:** Handle bulk uploads of transcripts, making it feasible to process large datasets.
- **Enhance Data Security:** Operate entirely offline to ensure sensitive information remains secure.
- **Improve Resource Allocation:** Allow researchers to focus on higher-value analysis rather than manual coding tasks.

### Key Deliverables for the MVP
1. **Automated Transcript Coding:**  
   - Process CSV transcripts by mapping each dialogue row to a communication category based on a user-defined keyword dictionary.
   - Append a new column to each CSV file with the assigned code.

2. **Bulk Data Processing:**  
   - Enable simultaneous processing of multiple CSV files to efficiently handle large volumes of data.

3. **Frequency Summary Report:**  
   - Generate summary reports that provide frequency counts for each communication code across the dataset.

4. **Offline Operation:**  
   - Ensure the application functions entirely offline, keeping all sensitive data secure and eliminating dependency on external services.


