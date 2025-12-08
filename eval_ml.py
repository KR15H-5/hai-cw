import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_curve,
    auc
)

from utils.text_processor import TextProcessor
from config import DATA_DIR


def load_training_data():
    path = os.path.join(DATA_DIR, "training_data.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "greeting": ["hello", "hi", "hey"],
            "farewell": ["bye", "goodbye"],
            "help": ["help"]
        }


def prepare_dataset(intent_data):
    tp = TextProcessor()
    X, y = [], []

    for intent, samples in intent_data.items():
        for s in samples:
            X.append(tp.stem_text(s))
            y.append(intent)

    return X, y


def plot_confusion(cm, labels):
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=(7, 6))
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=300)
    plt.close()


def plot_classification_report(report, labels):
    lines = report.split("\n")
    rows = []
    for line in lines[2:2+len(labels)]:
        parts = line.split()
        if len(parts) >= 5:
            rows.append([float(parts[1]), float(parts[2]), float(parts[3])])

    data = np.array(rows)
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(data, cmap="Oranges")

    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(["Precision", "Recall", "F1"])
    ax.set_yticklabels(labels)

    plt.colorbar(im)
    plt.title("Classification Report Heatmap")
    plt.tight_layout()
    plt.savefig("classification_report_heatmap.png", dpi=300)
    plt.close()


def plot_f1_scores(report, labels):
    lines = report.split("\n")
    f1_scores = []

    for line in lines[2:2+len(labels)]:
        parts = line.split()
        f1_scores.append(float(parts[3]))

    fig = plt.figure(figsize=(7, 4))
    plt.bar(labels, f1_scores)
    plt.ylim(0, 1)
    plt.title("F1 Score per Intent")
    plt.tight_layout()
    plt.savefig("f1_scores.png", dpi=300)
    plt.close()


def plot_cross_validation(scores):
    fig = plt.figure(figsize=(6, 4))
    plt.plot(scores, marker="o")
    plt.title("Cross-Validation Accuracy")
    plt.xlabel("Fold")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("cv_accuracy.png", dpi=300)
    plt.close()


def plot_roc_curves(clf, X_test_vec, y_test, labels):
    if not hasattr(clf, "predict_proba"):
        return

    y_bin = {label: np.array([1 if t == label else 0 for t in y_test]) for label in labels}
    y_proba = clf.predict_proba(X_test_vec)

    fig = plt.figure(figsize=(7, 6))

    for i, label in enumerate(labels):
        fpr, tpr, _ = roc_curve(y_bin[label], y_proba[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{label} (AUC={roc_auc:.2f})")

    plt.plot([0, 1], [0, 1], linestyle="--", color="grey")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curves (One-vs-Rest)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("roc_curves.png", dpi=300)
    plt.close()


def main():
    intent_data = load_training_data()
    X, y = prepare_dataset(intent_data)

    labels = sorted(set(y))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        C=10.0,
        random_state=42
    )

    clf.fit(X_train_vec, y_train)
    y_pred = clf.predict(X_test_vec)

    cm = confusion_matrix(y_test, y_pred)
    plot_confusion(cm, labels)

    report = classification_report(y_test, y_pred, digits=4)
    plot_classification_report(report, labels)
    plot_f1_scores(report, labels)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    X_vec_full = vectorizer.fit_transform(X)
    scores = cross_val_score(clf, X_vec_full, y, cv=skf, scoring="accuracy")
    plot_cross_validation(scores)

    plot_roc_curves(clf, X_test_vec, y_test, labels)

    print("Saved: confusion_matrix.png, classification_report_heatmap.png, f1_scores.png, cv_accuracy.png, roc_curves.png")


if __name__ == "__main__":
    main()
