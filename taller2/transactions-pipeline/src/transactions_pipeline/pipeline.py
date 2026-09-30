import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

AMOUNT_COLUMN = "Amount (INR)"
TARGET_COLUMN = "is_large_transaction"


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    print(f"Primeras 5 filas del dataset {csv_path}:")
    print(df.head())
    print("\nInformacion del dataset:")
    df.info()
    print("\nValores nulos por columna:")
    print(df.isnull().sum())
    return df


def build_target(df):
    df_procesado = df.copy()

    if AMOUNT_COLUMN in df_procesado.columns:
        median_amount = df_procesado[AMOUNT_COLUMN].median()
        df_procesado[TARGET_COLUMN] = (df_procesado[AMOUNT_COLUMN] > median_amount).astype(int)
        cols_to_exclude_from_x = [AMOUNT_COLUMN, TARGET_COLUMN]
    else:
        print(f"Advertencia: La columna '{AMOUNT_COLUMN}' no se encontro. Creando un target dummy.")
        df_procesado[TARGET_COLUMN] = np.random.randint(0, 2, len(df_procesado))
        cols_to_exclude_from_x = [TARGET_COLUMN]

    numeric_features = df_procesado.select_dtypes(include=np.number).columns.tolist()
    for col in cols_to_exclude_from_x:
        if col in numeric_features:
            numeric_features.remove(col)
    categorical_features = df_procesado.select_dtypes(include="object").columns.tolist()

    X = df_procesado.drop(columns=cols_to_exclude_from_x, errors="ignore")
    y = df_procesado[TARGET_COLUMN]

    print(f"Variable objetivo creada: '{TARGET_COLUMN}'")
    print(f"Columnas numericas identificadas para el pipeline: {numeric_features}")
    print(f"Columnas categoricas identificadas para el pipeline: {categorical_features}")
    print("\nPrimeras 5 filas de X (caracteristicas):")
    print(X.head())
    print("\nPrimeras 5 filas de y (variable objetivo):")
    print(y.head())

    return X, y, numeric_features, categorical_features


def build_preprocessor(numeric_features, categorical_features):
    transformador_numerico = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler()),
    ])
    transformador_categorico = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer(transformers=[
        ("num", transformador_numerico, numeric_features),
        ("cat", transformador_categorico, categorical_features),
    ])


def build_param_grid():
    return [
        {
            "clasificador": [LogisticRegression(solver="liblinear", max_iter=1000)],
            "clasificador__C": [0.01, 0.1, 1, 10],
            "clasificador__penalty": ["l1", "l2"],
        },
        {
            "clasificador": [RandomForestClassifier(random_state=42, n_jobs=-1)],
            "clasificador__n_estimators": [200, 400],
            "clasificador__max_depth": [None, 10, 20],
            "clasificador__min_samples_leaf": [1, 5],
        },
        {
            "clasificador": [HistGradientBoostingClassifier(random_state=42)],
            "clasificador__learning_rate": [0.05, 0.1],
            "clasificador__max_depth": [None, 5, 10],
        },
    ]


def extract(csv_path, output_path):
    """Etapa de extraccion: lee el CSV crudo y lo copia al workspace del pipeline."""
    df = load_data(csv_path)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Datos extraidos guardados en: {output_path.resolve()}")

    return output_path


def clean(input_path, output_path, features_path):
    """Etapa de limpieza: construye la variable objetivo y separa columnas por tipo."""
    df = pd.read_csv(input_path)
    X, y, numeric_features, categorical_features = build_target(df)

    cleaned = X.copy()
    cleaned[TARGET_COLUMN] = y

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)

    features_path = Path(features_path)
    features_path.parent.mkdir(parents=True, exist_ok=True)
    with open(features_path, "w", encoding="utf-8") as f:
        json.dump(
            {"numeric_features": numeric_features, "categorical_features": categorical_features},
            f,
        )

    print(f"Datos limpios guardados en: {output_path.resolve()}")
    print(f"Columnas guardadas en: {features_path.resolve()}")

    return output_path, features_path


def train(input_path, features_path, model_out):
    """Etapa de entrenamiento: grid search sobre los modelos y guardado del mejor."""
    df = pd.read_csv(input_path)
    with open(features_path, "r", encoding="utf-8") as f:
        features = json.load(f)
    numeric_features = features["numeric_features"]
    categorical_features = features["categorical_features"]

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    preprocesador = build_preprocessor(numeric_features, categorical_features)
    print("Preprocesadores definidos.")

    full_pipeline = Pipeline(steps=[
        ("preprocesador", preprocesador),
        ("clasificador", LogisticRegression()),
    ])
    print("Pipeline completo definido.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Tamano del conjunto de entrenamiento: {X_train.shape}")
    print(f"Tamano del conjunto de prueba: {X_test.shape}")

    grid = GridSearchCV(
        estimator=full_pipeline,
        param_grid=build_param_grid(),
        cv=5,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=1,
    )
    grid.fit(X_train, y_train)

    print("Mejor combinacion:", grid.best_params_)
    print(f"Mejor ROC-AUC (CV): {grid.best_score_:.4f}")

    model_out = Path(model_out)
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(grid.best_estimator_, model_out)
    print(f"Modelo guardado en: {model_out.resolve()}")

    return grid
