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
    fig, ax = plt.subplots(figsize=(12, 10))
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    plt.title("Confusion Matrix", fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.xlabel("Predicted label", fontsize=11)
    plt.ylabel("True label", fontsize=11)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_classification_report(report, labels):
    lines = report.split("\n")
    rows = []
    for line in lines[2:2+len(labels)]:
        parts = line.split()
        if len(parts) >= 5:
            rows.append([float(parts[1]), float(parts[2]), float(parts[3])])

    data = np.array(rows)
    fig, ax = plt.subplots(figsize=(10, max(6, len(labels) * 0.4)))
    im = ax.imshow(data, cmap="Oranges")

    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(["Precision", "Recall", "F1"], fontsize=10)
    ax.set_yticklabels(labels, fontsize=9)

    # Add text annotations
    for i in range(len(labels)):
        for j in range(3):
            text = ax.text(j, i, f'{data[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=8)

    plt.colorbar(im)
    plt.title("Classification Report Heatmap", fontsize=12, pad=15)
    plt.tight_layout()
    plt.savefig("classification_report_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_f1_scores(report, labels):
    lines = report.split("\n")
    f1_scores = []

    for line in lines[2:2+len(labels)]:
        parts = line.split()
        f1_scores.append(float(parts[3]))

    fig = plt.figure(figsize=(max(10, len(labels) * 0.5), 6))
    plt.bar(labels, f1_scores, color='steelblue', alpha=0.8)
    plt.ylim(0, 1)
    plt.title("F1 Score per Intent", fontsize=12, pad=15)
    plt.xlabel("Intent", fontsize=10)
    plt.ylabel("F1 Score", fontsize=10)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("f1_scores.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_cross_validation(scores):
    fig = plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(scores) + 1), scores, marker="o", linewidth=2, markersize=8, color='steelblue')
    plt.title("Cross-Validation Accuracy", fontsize=12, pad=15)
    plt.xlabel("Fold", fontsize=10)
    plt.ylabel("Accuracy", fontsize=10)
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(range(1, len(scores) + 1))
    plt.tight_layout()
    plt.savefig("cv_accuracy.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_roc_curves(clf, X_test_vec, y_test, labels):
    if not hasattr(clf, "predict_proba"):
        return

    y_bin = {label: np.array([1 if t == label else 0 for t in y_test]) for label in labels}
    y_proba = clf.predict_proba(X_test_vec)

    fig = plt.figure(figsize=(10, 8))

    for i, label in enumerate(labels):
        fpr, tpr, _ = roc_curve(y_bin[label], y_proba[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{label} (AUC={roc_auc:.2f})", linewidth=2)

    plt.plot([0, 1], [0, 1], linestyle="--", color="grey", linewidth=2)
    plt.xlabel("False Positive Rate", fontsize=11)
    plt.ylabel("True Positive Rate", fontsize=11)
    plt.title("ROC Curves (One-vs-Rest)", fontsize=12, pad=15)
    plt.legend(loc='lower right', fontsize=9)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("roc_curves.png", dpi=300, bbox_inches='tight')
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