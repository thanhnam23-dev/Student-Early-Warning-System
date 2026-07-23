import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# CONFIG
# ==========================================================

MODEL = "lightgbm"

# logistic_regression
# decision_tree
# random_forest
# xgboost
# lightgbm
# catboost

CSV_FILE = f"history_{MODEL}.csv"

SAVE_NAME = f"{MODEL}_learning_curves.png"

# ==========================================================
# READ DATA
# ==========================================================

df = pd.read_csv(CSV_FILE)

epochs = df["epoch"]

# ==========================================================
# STYLE
# ==========================================================

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 11

fig, axes = plt.subplots(
    1,
    2,
    figsize=(14, 5)
)

# ==========================================================
# LEFT : LOSS
# ==========================================================

axes[0].plot(
    epochs,
    df["train_loss"],
    color="#d62728",
    linewidth=2,
    marker="o",
    markersize=3,
    label="Training Loss"
)

axes[0].plot(
    epochs,
    df["val_loss"],
    color="#ff7f0e",
    linewidth=2,
    marker="o",
    markersize=3,
    label="Validation Loss"
)

axes[0].set_title(
    f"{MODEL.replace('_',' ').title()} - Training and Validation Loss",
    fontsize=12
)

axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Loss (LogLoss)")

axes[0].set_xlim(1,50)
axes[0].set_xticks(range(1,51,5))

axes[0].grid(
    linestyle="--",
    alpha=0.4
)

axes[0].legend()

# ==========================================================
# RIGHT : ACCURACY
# ==========================================================

axes[1].plot(
    epochs,
    df["train_acc"],
    color="#2ca02c",
    linewidth=2,
    marker="o",
    markersize=3,
    label="Training Accuracy"
)

axes[1].plot(
    epochs,
    df["val_acc"],
    color="#1f77b4",
    linewidth=2,
    marker="o",
    markersize=3,
    label="Validation Accuracy"
)

axes[1].set_title(
    f"{MODEL.replace('_',' ').title()} - Training and Validation Accuracy",
    fontsize=12
)

axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Accuracy")

axes[1].set_xlim(1,50)
axes[1].set_xticks(range(1,51,5))

axes[1].grid(
    linestyle="--",
    alpha=0.4
)

axes[1].legend()

# ==========================================================
# MAIN TITLE
# ==========================================================

plt.suptitle(
    f"Learning Curves (Training vs Validation) - {MODEL.replace('_',' ').title()}",
    fontsize=15,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    SAVE_NAME,
    dpi=600,
    bbox_inches="tight"
)

plt.show()