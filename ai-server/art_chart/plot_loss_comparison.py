import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# CONFIG
# ==========================================================

MODELS = {
    "Logistic Regression": "history_logistic_regression.csv",
    "Decision Tree": "history_decision_tree.csv",
    "Random Forest": "history_random_forest.csv",
    "XGBoost": "history_xgboost.csv",
    "LightGBM": "history_lightgbm.csv",
    "CatBoost": "history_catboost.csv",
}

SAVE_NAME = "validation_loss_comparison.png"

# ==========================================================
# STYLE
# ==========================================================

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

plt.figure(figsize=(8, 6))

# ==========================================================
# FIND Y RANGE
# ==========================================================

all_values = []

for file in MODELS.values():
    df = pd.read_csv(file)
    all_values.extend(df["val_loss"].tolist())

ymin = min(all_values)
ymax = max(all_values)

padding = (ymax - ymin) * 0.08

# ==========================================================
# DRAW
# ==========================================================

for model_name, csv_file in MODELS.items():

    df = pd.read_csv(csv_file)

    plt.plot(
        df["epoch"],
        df["val_loss"],
        linewidth=1.8,
        marker=".",
        markersize=6,
        markevery=1,
        label=model_name
    )

# ==========================================================
# FIGURE SETTINGS
# ==========================================================

plt.title(
    "Validation Loss Across Epochs",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Epoch")
plt.ylabel("Validation Loss")

plt.xlim(1, 50)
plt.xticks(range(1, 51, 5))

plt.ylim(
    ymin - padding,
    ymax + padding
)

plt.grid(
    linestyle="--",
    alpha=0.4
)

plt.legend(
    fontsize=9,
    ncol=2,
    loc="upper right",
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