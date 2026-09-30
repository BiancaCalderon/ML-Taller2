import argparse
import sys
from datetime import datetime
from pathlib import Path

from transactions_pipeline.pipeline import clean, extract, train


class Tee:
    """Writes to multiple streams at once (console + log file)."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def cmd_extract(args):
    extract(args.csv_path, args.out)


def cmd_clean(args):
    clean(args.input, args.out, args.features_out)


def cmd_train(args):
    log_file = args.log_file or f"training_{datetime.now():%Y%m%d_%H%M%S}.log"
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    original_stdout, original_stderr = sys.stdout, sys.stderr
    with open(log_path, "w", encoding="utf-8") as f:
        sys.stdout = Tee(original_stdout, f)
        sys.stderr = Tee(original_stderr, f)
        try:
            train(args.input, args.features, args.model_out)
        finally:
            sys.stdout, sys.stderr = original_stdout, original_stderr

    print(f"Log guardado en: {log_path.resolve()}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Pipeline de entrenamiento para clasificar transacciones grandes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_extract = subparsers.add_parser("extract", help="Extrae los datos crudos del CSV de entrada.")
    p_extract.add_argument("csv_path", type=str, help="Path al CSV de transacciones")
    p_extract.add_argument(
        "--out", type=str, default="data/extracted.csv", help="Path de salida para los datos extraidos"
    )
    p_extract.set_defaults(func=cmd_extract)

    p_clean = subparsers.add_parser("clean", help="Limpia los datos y genera la variable objetivo.")
    p_clean.add_argument("--input", type=str, required=True, help="Path al CSV extraido")
    p_clean.add_argument(
        "--out", type=str, default="data/cleaned.csv", help="Path de salida para los datos limpios"
    )
    p_clean.add_argument(
        "--features-out",
        type=str,
        default="data/features.json",
        help="Path de salida para las columnas numericas/categoricas",
    )
    p_clean.set_defaults(func=cmd_clean)

    p_train = subparsers.add_parser("train", help="Entrena y selecciona el mejor modelo.")
    p_train.add_argument("--input", type=str, required=True, help="Path al CSV limpio")
    p_train.add_argument("--features", type=str, required=True, help="Path al JSON de columnas")
    p_train.add_argument(
        "--model-out",
        type=str,
        default="models/model.joblib",
        help="Path de salida para el modelo entrenado",
    )
    p_train.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Path al log (default: training_<timestamp>.log)",
    )
    p_train.set_defaults(func=cmd_train)

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
