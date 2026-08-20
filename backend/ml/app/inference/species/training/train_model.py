"""
Trains a bee species classifier using transfer learning
(EfficientNetB0 pre-trained on ImageNet) in two phases:

  Phase 1: freezes the backbone, trains only the classification head
  Phase 2 (fine-tuning): unfreezes the last layers of the backbone and
          trains with a low learning rate

Usage:
    python 03_train_model.py --data-dir dataset --epochs 30 \
        --fine-tune-epochs 15 --output-dir models/v1
"""

import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow import keras  # type: ignore
from tensorflow.keras import layers  # type: ignore

IMG_SIZE = (224, 224)
BATCH_SIZE = 32


def build_datasets(data_dir: Path):
    train_ds = keras.utils.image_dataset_from_directory(
        data_dir / "train",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=True,
        seed=42,
    )
    val_ds = keras.utils.image_dataset_from_directory(
        data_dir / "val",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False,
    )
    class_names = train_ds.class_names

    test_dir = data_dir / "test"
    test_ds = None
    if test_dir.exists() and any(test_dir.iterdir()):
        test_ds = keras.utils.image_dataset_from_directory(
            test_dir,
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="categorical",
            shuffle=False,
        )

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)
    if test_ds is not None:
        test_ds = test_ds.prefetch(autotune)

    return train_ds, val_ds, test_ds, class_names


def compute_class_weights(data_dir: Path, class_names: list[str]) -> dict[int, float]:
    # It compensates for classes with fewer images, which is common when the dataset is collected from scratch.
    counts = []
    for name in class_names:
        n = len(list((data_dir / "train" / name).glob("*")))
        counts.append(n)
    total = sum(counts)
    n_classes = len(class_names)
    weights = {i: total / (n_classes * c) for i, c in enumerate(counts) if c > 0}
    return weights


def build_model(num_classes: int) -> keras.Model:
    data_augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.15),
            layers.RandomZoom(0.15),
            layers.RandomContrast(0.15),
            layers.RandomBrightness(0.15),
        ],
        name="augmentation",
    )

    base_model = keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=IMG_SIZE + (3,),
        pooling="avg",
    )
    base_model.trainable = False

    inputs = keras.Input(shape=IMG_SIZE + (3,))
    x = data_augmentation(inputs)
    x = keras.applications.efficientnet.preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    return model, base_model


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--epochs", type=int, default=30, help="Epochs of phase 1 (frozen backbone)"
    )
    parser.add_argument(
        "--fine-tune-epochs",
        type=int,
        default=15,
        help="Epochs of phase 2 (fine-tuning)",
    )
    parser.add_argument(
        "--fine-tune-layers",
        type=int,
        default=30,
        help="Number of final backbone layers to unfreeze",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    train_ds, val_ds, test_ds, class_names = build_datasets(args.data_dir)
    class_weights = compute_class_weights(args.data_dir, class_names)
    print("Class weights (compensating for imbalance):", class_weights)

    model, base_model = build_model(num_classes=len(class_names))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        keras.callbacks.EarlyStopping(
            patience=6, restore_best_weights=True, monitor="val_accuracy"
        ),
        keras.callbacks.ReduceLROnPlateau(patience=3, factor=0.5, monitor="val_loss"),
    ]

    print("\nPhase 1: training classification head (frozen backbone)")
    history_1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.epochs,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    print("\nPhase 2: fine-tuning the final layers of the backbone")
    base_model.trainable = True
    for layer in base_model.layers[: -args.fine_tune_layers]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    history_2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=args.fine_tune_epochs,
        class_weight=class_weights,
        callbacks=callbacks,
    )

    report = {
        "class_names": class_names,
        "phase1_history": {
            k: [float(v) for v in vals] for k, vals in history_1.history.items()
        },
        "phase2_history": {
            k: [float(v) for v in vals] for k, vals in history_2.history.items()
        },
    }

    if test_ds is not None:
        test_loss, test_acc = model.evaluate(test_ds)
        report["test_loss"] = float(test_loss)
        report["test_accuracy"] = float(test_acc)
        print(f"\nAccuracy on test set: {test_acc:.4f}")

    model_path = args.output_dir / "species_model.keras"
    model.save(model_path)

    labels_path = args.output_dir / "labels.json"
    with open(labels_path, "w") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

    report_path = args.output_dir / "training_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
