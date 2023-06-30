# README

This README file provides instructions on how to set up a virtual environment, install requirements, and run a Python command using Git.

## Prerequisites

Before proceeding with the instructions, ensure that you have the following software installed on your machine:

- Git: [Download and install Git](https://git-scm.com/downloads)
- Python: [Download and install Python](https://www.python.org/downloads/)

## Instructions

1. Clone the repository: 

    ```sh
    git clone https://github.com/monika-kh/LinkedIn_scrapping.git
    ```
2. Change into the repository directory:
    ```sh
    cd LinkedIn_scrapping
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    or
    python3 -m venv venv
    ```
4. Activate the virtual environment:

    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```sh
      source venv/bin/activate
      ```
5. Install requirements:
    ```sh
    pip install -r requirements.txt
    ```
    This command installs the necessary Python packages specified in the requirements.txt file.
6. Also install playwright in system:
    ```sh
    playwright install
    ```
7. Run a Python command:
    ```sh
    python test_job.py task.csv
    ```

