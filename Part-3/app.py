from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import os
import re
import smtplib
from email.message import EmailMessage
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SENDER_EMAIL = os.getenv("TOPSIS_EMAIL")
SENDER_PASSWORD = os.getenv("TOPSIS_APP_PASSWORD")


def topsis(data, weights, impacts, output_file):
    if data.shape[1] < 3:
        raise Exception("Input file must contain at least 3 columns")

    values = data.iloc[:, 1:]

    if not all(pd.api.types.is_numeric_dtype(values[col]) for col in values.columns):
        raise Exception("Criteria columns must be numeric")

    weights = np.array(weights, dtype=float)

    norm = np.sqrt((values ** 2).sum())
    normalized = values / norm
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    data["Topsis Score"] = score
    data["Rank"] = data["Topsis Score"].rank(ascending=False).astype(int)
    data.to_csv(output_file, index=False)


def send_email(receiver_email, file_path):
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content("Please find the TOPSIS result attached.")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    file = request.files.get("file")
    weights = request.form.get("weights", "").split(",")
    impacts = request.form.get("impacts", "").split(",")
    email = request.form.get("email", "")

    if not file:
        return "No file uploaded", 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format", 400

    if len(weights) != len(impacts):
        return "Number of weights and impacts must be equal", 400

    for i in impacts:
        if i not in ['+', '-']:
            return "Impacts must be + or -", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    if file.filename.endswith(".xlsx"):
        data = pd.read_excel(file_path)
    else:
        data = pd.read_csv(file_path)

    if data.shape[1] - 1 != len(weights):
        return "Mismatch between criteria and weights", 400

    output_file = f"result_{uuid.uuid4().hex}.csv"
    topsis(data, weights, impacts, output_file)
    send_email(email, output_file)

    return "Result sent successfully to your email", 200


if __name__ == "__main__":
    app.run(debug=True)
