import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, auc

# ==========================================================
# CONFIG
# ==========================================================

MODELS = {
    "Logistic Regression": "eval_logistic_regression.csv",
    "Decision Tree": "eval_decision_tree.csv",
    "Random Forest": "eval_random_forest.csv",
    "XGBoost": "eval_xgboost.csv",
    "LightGBM": "eval_lightgbm.csv",
    "CatBoost": "eval_catboost.csv",
}

SAVE_NAME = "roc_comparison.png"

# ==========================================================
# STYLE
# ==========================================================

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

plt.figure(figsize=(8, 6))

# ==========================================================
# DRAW ROC
# ==========================================================

for model_name, csv_file in MODELS.items():

    df = pd.read_csv(csv_file)

    fpr, tpr, _ = roc_curve(
        df["y_true"],
        df["y_proba"]
    )

    roc_auc = auc(fpr, tpr)

    plt.plot(
        fpr,
        tpr,
        linewidth=1.6,
        label=f"{model_name} (AUC={roc_auc:.3f})"
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
# FIGURE SETTINGS
# ==========================================================

plt.title(
    "ROC Curve Comparison on Test Set",
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
    loc="lower right",
    fontsize=9,
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