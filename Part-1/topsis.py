import sys
import os
import pandas as pd
import numpy as np


def error(msg):
    print("Error:", msg)
    sys.exit(1)


def main():
    if len(sys.argv) != 5:
        error("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")

    input_file = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file = sys.argv[4]

    if not os.path.exists(input_file):
        error("Input file not found")

    try:
        if input_file.endswith(".xlsx"):
            df = pd.read_excel(input_file)
        else:
            df = pd.read_csv(input_file)
    except Exception:
        error("Unable to read input file")

    if df.shape[1] < 3:
        error("Input file must contain at least 3 columns")

    data = df.iloc[:, 1:]

    if not all(pd.api.types.is_numeric_dtype(data[col]) for col in data.columns):
        error("Columns from 2nd to last must contain numeric values only")

    weights = weights.split(',')
    impacts = impacts.split(',')

    if len(weights) != data.shape[1]:
        error("Number of weights must be equal to number of criteria")

    if len(impacts) != data.shape[1]:
        error("Number of impacts must be equal to number of criteria")

    try:
        weights = np.array(list(map(float, weights)))
    except:
        error("Weights must be numeric")

    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be either + or -")

    norm = np.sqrt((data ** 2).sum())
    normalized = data / norm
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

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    df.to_csv(output_file, index=False)
    print("TOPSIS result saved to:", output_file)


if __name__ == "__main__":
    main()
