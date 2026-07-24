import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, auc

# ==========================================================
# CONFIG
# ==========================================================

# Chỉ cần đổi tên model tại đây
MODEL = "catboost"

# Các lựa chọn:
# logistic_regression
# decision_tree
# random_forest
# xgboost
# lightgbm
# catboost

FOLDS_DIR = "folds"

SAVE_NAME = f"{MODEL}_roc_5folds.png"

# ==========================================================
# STYLE
# ==========================================================

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

plt.figure(figsize=(8, 6))

# ==========================================================
# DRAW ROC OF EACH FOLD
# ==========================================================

auc_scores = []

for fold in range(5):

    file_path = os.path.join(
        FOLDS_DIR,
        f"val_fold_{fold}_{MODEL}.csv"
    )

    df = pd.read_csv(file_path)

    fpr, tpr, _ = roc_curve(
        df["y_true"],
        df["y_proba"]
    )

    roc_auc = auc(fpr, tpr)
    auc_scores.append(roc_auc)

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"Fold {fold + 1} (AUC={roc_auc:.3f})"
    )

# ==========================================================
# RANDOM LINE
# ==========================================================

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    color="gray",
    linewidth=1.5,
    label="Random Guess"
)

# ==========================================================
# TITLE
# ==========================================================

mean_auc = sum(auc_scores) / len(auc_scores)

plt.title(
    f"{MODEL.replace('_',' ').title()} - ROC Across 5 Folds\nMean AUC = {mean_auc:.3f}",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.xlim(0, 1)
plt.ylim(0, 1.02)

plt.grid(
    linestyle="--",
    alpha=0.4
)

plt.legend(
    fontsize=9,
    loc="lower right",
    frameon=True
)

plt.tight_layout()

# ==========================================================
# SAVE
# ==========================================================

plt.savefig(
    SAVE_NAME,
    dpi=600,
    bbox_inches="tight"
)

plt.show()