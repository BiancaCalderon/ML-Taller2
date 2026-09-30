# transactions-pipeline

ML training pipeline package.

## Install

```bash
pip install -e .
```

## Usage

```bash
transactions-pipeline extract path/to/data.csv --out data/extracted.csv
transactions-pipeline clean --input data/extracted.csv --out data/cleaned.csv --features-out data/features.json
transactions-pipeline train --input data/cleaned.csv --features data/features.json --model-out models/model.joblib
```
