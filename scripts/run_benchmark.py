import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from evaluation.evaluator import run_benchmark


if __name__ == "__main__":
    run_benchmark()