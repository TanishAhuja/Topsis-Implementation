import sys
import os
import pandas as pd
import numpy as np


def topsis(input_file, weights, impacts, output_file):
    if not os.path.exists(input_file):
        raise Exception("Input file not found")

    if input_file.endswith(".xlsx"):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)

    if df.shape[1] < 3:
        raise Exception("Input file must contain at least 3 columns")

    data = df.iloc[:, 1:]

    if not all(pd.api.types.is_numeric_dtype(data[col]) for col in data.columns):
        raise Exception("Columns from 2nd to last must be numeric")

    weights = weights.split(',')
    impacts = impacts.split(',')

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        raise Exception("Weights, impacts and criteria count must match")

    weights = np.array(list(map(float, weights)))

    for i in impacts:
        if i not in ['+', '-']:
            raise Exception("Impacts must be + or -")

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


def main():
    if len(sys.argv) != 5:
        print("Usage: topsis <InputFile> <Weights> <Impacts> <OutputFile>")
        sys.exit(1)

    try:
        topsis(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        print("TOPSIS analysis completed")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
