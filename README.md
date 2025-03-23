# CITS5206_SubmarineTrans
Researchers studying submarine simulator team exercises are faced with the labor-intensive task of manually coding each utterance in dozens of one-hour voice recordings. These recordings, transcribed into CSV format, often exceed 400–500 rows of dialogue per file and demand consistent application of a qualitative coding frame. Currently, this manual process requires two independent raters, is highly repetitive, and risks human error or coder fatigue. As the volume of transcripts continues to grow, scalability and efficiency become critical concerns. To address this, we seek an offline deterministic coding application that leverages a user-defined dictionary of keywords and phrases. By mapping each utterance to specific communication categories, researchers can dramatically reduce the time spent on repetitive coding tasks, maintain high accuracy, and streamline future data analysis—without relying on internet connectivity or external services.

## Table Of Content
  1. Overview

## Overview
Researchers studying submarine simulator exercises often need to analyze communication patterns among team members. Manually coding each dialog line is slow, error-prone, and difficult to scale. This application automates the process by:
* Allowing a user-defined dictionary of keywords → codes (e.g., “down all masts” → `TL:ORD`).
* Processing multiple CSV transcripts at once, appending a new column of codes.
* Generating a frequency summary of how often each code appears.
* Operating entirely offline, ensuring sensitive data never leaves the local environment.

