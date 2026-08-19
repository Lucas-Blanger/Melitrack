"""
Organizes a directory of raw images (one subfolder per species) into
train/val/test splits ready for `keras.utils.image_dataset_from_directory`.

Usage:
    python 02_prepare_dataset.py --input raw_dataset --output dataset \
        --val-split 0.15 --test-split 0.1
"""

import os
import argparse
import random
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATASET_INPUT_DIR = Path(os.getenv("DATASET_INPUT_DIR"))
DATASET_OUTPUT_DIR = Path(os.getenv("DATASET_OUTPUT_DIR"))
DATASET_VAL_SPLIT = float(os.getenv("DATASET_VAL_SPLIT"))
DATASET_TEST_SPLIT = float(os.getenv("DATASET_TEST_SPLIT"))
DATASET_RANDOM_SEED = int(os.getenv("DATASET_RANDOM_SEED"))

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def split_dataset(
    input_dir: Path,
    output_dir: Path,
    val_split: float,
    test_split: float,
    seed: int = 42,
) -> None:
    random.seed(seed)

    species_dirs = [d for d in input_dir.iterdir() if d.is_dir()]
    if not species_dirs:
        raise ValueError(f"No species subfolders found in {input_dir}")

    summary = {}

    for species_dir in species_dirs:
        images = [
            p for p in species_dir.iterdir() if p.suffix.lower() in VALID_EXTENSIONS
        ]
        random.shuffle(images)

        n = len(images)
        n_test = int(n * test_split)
        n_val = int(n * val_split)
        n_train = n - n_val - n_test

        if n_train <= 0:
            print(
                f"WARNING: {species_dir.name} has few images ({n}). Skipping val/test splits."
            )
            n_train, n_val, n_test = n, 0, 0

        splits = {
            "train": images[:n_train],
            "val": images[n_train : n_train + n_val],
            "test": images[n_train + n_val :],
        }

        for split_name, split_images in splits.items():
            dest_dir = output_dir / split_name / species_dir.name
            dest_dir.mkdir(parents=True, exist_ok=True)
            for img_path in split_images:
                shutil.copy2(img_path, dest_dir / img_path.name)

        summary[species_dir.name] = {
            "total": n,
            "train": len(splits["train"]),
            "val": len(splits["val"]),
            "test": len(splits["test"]),
        }

    print("\nSummary of the split:")
    print(f"{'Species':<20}{'Total':>8}{'Train':>8}{'Val':>8}{'Test':>8}")
    for species, counts in summary.items():
        print(
            f"{species:<20}{counts['total']:>8}{counts['train']:>8}{counts['val']:>8}{counts['test']:>8}"
        )

    min_train = min(c["train"] for c in summary.values())
    if min_train < 50:
        print(
            f"\nWARNING: the species with the fewest training images has only {min_train}. "
            "At least ~80–100 per class is recommended for reasonable results. "
            "Consider collecting more data before training."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", required=True, type=Path, help="Directory with species subfolders"
    )
    parser.add_argument(
        "--output", required=True, type=Path, help="Output directory (train/val/test)"
    )
    parser.add_argument("--val-split", type=float, default=0.15)
    parser.add_argument("--test-split", type=float, default=0.1)
    args = parser.parse_args()

    split_dataset(
        input_dir=DATASET_INPUT_DIR,
        output_dir=DATASET_OUTPUT_DIR,
        val_split=DATASET_VAL_SPLIT,
        test_split=DATASET_TEST_SPLIT,
        seed=DATASET_RANDOM_SEED,
    )


if __name__ == "__main__":
    main()
