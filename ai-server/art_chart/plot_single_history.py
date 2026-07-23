import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# CONFIG
# ==========================================================

MODEL = "catboost"

# logistic_regression
# decision_tree
# random_forest
# xgboost
# lightgbm
# catboost

METRIC = "accuracy"

# accuracy
# loss

CSV_FILE = f"history_{MODEL}.csv"

SAVE_NAME = f"{MODEL}_{METRIC}.png"

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

plt.figure(figsize=(8,6))

# ==========================================================
# ACCURACY
# ==========================================================

if METRIC.lower() == "accuracy":

    train = df["train_acc"]
    val = df["val_acc"]

    plt.plot(
        epochs,
        train,
        linewidth=2,
        label="Training Accuracy"
    )

    plt.plot(
        epochs,
        val,
        linewidth=2,
        linestyle="--",
        label="Validation Accuracy"
    )

    ymin = min(train.min(), val.min())
    ymax = max(train.max(), val.max())

    padding = (ymax - ymin) * 0.08

    plt.ylabel("Accuracy")

    plt.title(
        f"{MODEL.replace('_',' ').title()} Training History (Accuracy)",
        fontsize=14,
        fontweight="bold"
    )

# ==========================================================
# LOSS
# ==========================================================

elif METRIC.lower() == "loss":

    train = df["train_loss"]
    val = df["val_loss"]

    plt.plot(
        epochs,
        train,
        linewidth=2,
        label="Training Loss"
    )

    plt.plot(
        epochs,
        val,
        linewidth=2,
        linestyle="--",
        label="Validation Loss"
    )

    ymin = min(train.min(), val.min())
    ymax = max(train.max(), val.max())

    padding = (ymax - ymin) * 0.08

    plt.ylabel("Loss")

    plt.title(
        f"{MODEL.replace('_',' ').title()} Training History (Loss)",
        fontsize=14,
        fontweight="bold"
    )

# ==========================================================
# SETTINGS
# ==========================================================

plt.xlabel("Epoch")

plt.xlim(1,50)
plt.xticks(range(1,51,5))

plt.ylim(
    ymin-padding,
    ymax+padding
)

plt.grid(
    linestyle="--",
    alpha=0.4
)

plt.legend(
    fontsize=10,
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