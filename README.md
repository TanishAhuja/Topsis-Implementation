# TOPSIS Assignment – Tanish Ahuja (Roll No: 102313008)

This repository contains the complete implementation of the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method as part of the assignment.  
The work is divided into three parts:

- Part 1: Command-line TOPSIS program  
- Part 2: Python package uploaded to PyPI  
- Part 3: Web service with email-based result delivery  

---

## Repository Structure

Topsis-Tanish-102313008/  
├── Part-1/  
│   ├── topsis.py  
│   ├── data.xlsx  
│   └── result.csv  
│  
├── Part-2/  
│   ├── setup.py  
│   ├── README.md  
│   └── Topsis_Tanish_102313008/  
│       ├── __init__.py  
│       └── topsis.py  
│  
├── Part-3/  
│   ├── app.py  
│   ├── templates/  
│   │   └── index.html  
│   └── uploads/  
│  
└── README.md  

---

## Part 1: Command-Line TOPSIS Program

### Description  
A Python script that implements the TOPSIS method and runs from the command line.

### Features  
- Accepts input file (CSV / Excel)  
- Accepts weights and impacts  
- Validates inputs  
- Generates TOPSIS score and rank  
- Outputs result as CSV file  

### Usage  
python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>

### Example  
python topsis.py data.xlsx "1,1,1,1,1" "+,+,-,-,-" result.csv

### Input File Rules  
- Minimum 3 columns  
- First column: Alternatives  
- Remaining columns: Numeric criteria  

---

## Part 2: Python Package (PyPI)

### Description  
The TOPSIS implementation was converted into a reusable Python package and uploaded to PyPI.

### PyPI Package Name  
Topsis-Tanish-102313008

### PyPI Link  
https://pypi.org/project/Topsis-Tanish-102313008/

### Installation  
pip install Topsis-Tanish-102313008

### Usage (Command Line)  
topsis <InputFile> <Weights> <Impacts> <OutputFile>

### Example  
topsis data.xlsx "1,1,1,1,1" "+,+,-,-,-" result.csv

The package was tested by installing it from PyPI and executing it via the command line.

---

## Part 3: Web Service (Flask + Email)

### Description  
A Flask-based web service that allows users to:
- Upload an input file  
- Provide weights and impacts  
- Enter an email address  
- Receive the TOPSIS result via email  

### Features  
- File upload (CSV / Excel)  
- Input validation  
- Email format validation  
- Result file sent as email attachment  
- Simple HTML interface  

---

### How to Run Part 3

1. Set Environment Variables (Email Credentials)

export TOPSIS_EMAIL="your_email@gmail.com"  
export TOPSIS_APP_PASSWORD="your_app_password"

2. Install Dependencies  

pip install flask pandas numpy openpyxl

3. Run the Flask App  

python app.py

4. Open in Browser  

http://127.0.0.1:5000/

5. Submit Form  
- Upload file  
- Enter weights (comma-separated)  
- Enter impacts (+ / -)  
- Enter email ID  

The result file is emailed to the provided address.

---

## TOPSIS Methodology

The following steps are implemented:

1. Normalize the decision matrix  
2. Apply weights  
3. Determine ideal best and ideal worst  
4. Calculate Euclidean distances  
5. Compute TOPSIS score  
6. Rank alternatives  

---

## Technologies Used

- Python  
- Pandas  
- NumPy  
- Flask  
- SMTP (Email)  
- PyPI  

---

## Assignment Completion Status

Part 1 – CLI Program: Completed  
Part 2 – PyPI Package: Completed  
Part 3 – Web Service: Completed  

---

## Author

Tanish Ahuja  
Roll Number: 102313008  