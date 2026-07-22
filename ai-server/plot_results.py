import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix

# Thiết lập style vẽ đồ thị khoa học
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_theme(style='whitegrid')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 14,
    'savefig.dpi': 300
})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 1. Vẽ biểu đồ so sánh đường cong ROC (ROC Curve) của 6 mô hình trên tập Test
# ----------------------------------------------------------------------
def plot_test_roc_comparison():
    print("Vẽ biểu đồ ROC so sánh 6 mô hình...")
    plt.figure(figsize=(8, 6.5))
    
    models = {
        "Logistic Regression": "eval_logistic_regression.csv",
        "Decision Tree": "eval_decision_tree.csv",
        "Random Forest": "eval_random_forest.csv",
        "XGBoost": "eval_xgboost.csv",
        "LightGBM": "eval_lightgbm.csv",
        "CatBoost": "eval_catboost.csv"
    }
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2']
    
    for (model_name, filename), color in zip(models.items(), colors):
        filepath = os.path.join(LOGS_DIR, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Tính ROC
            fpr, tpr, _ = roc_curve(df['y_true'], df['y_proba'])
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.4f})', color=color, linewidth=2)
            
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guessing (AUC = 0.5000)', linewidth=1.5)
    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.02])
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.title('Receiver Operating Characteristic (ROC) - Test Set Comparison')
    plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='none', shadow=True)
    plt.tight_layout()
    
    out_path = os.path.join(PLOTS_DIR, "roc_comparison_test.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"-> Đã lưu biểu đồ ROC so sánh tại: {out_path}")

# ----------------------------------------------------------------------
# 2. Vẽ biểu đồ Validation ROC Curves của 5 Folds (đối với mô hình tốt nhất CatBoost)
# ----------------------------------------------------------------------
def plot_validation_roc_folds(model_name="catboost", model_title="CatBoost"):
    print(f"Vẽ biểu đồ ROC trên 5-Folds của {model_title}...")
    folds_dir = os.path.join(LOGS_DIR, "folds")
    if not os.path.exists(folds_dir):
        print("Không tìm thấy log của các Folds để vẽ.")
        return
        
    plt.figure(figsize=(8, 6.5))
    
    mean_fpr = np.linspace(0, 1, 100)
    tprs = []
    aucs = []
    
    colors = ['#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5']
    
    for fold in range(5):
        filename = f"val_fold_{fold}_{model_name}.csv"
        filepath = os.path.join(folds_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            fpr, tpr, _ = roc_curve(df['y_true'], df['y_proba'])
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            
            plt.plot(fpr, tpr, label=f'Fold {fold+1} (AUC = {roc_auc:.4f})', color=colors[fold], alpha=0.8, linewidth=1.5)
            
            # Interpolate to compute mean ROC
            interp_tpr = np.interp(mean_fpr, fpr, tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)
            
    if tprs:
        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        
        plt.plot(mean_fpr, mean_tpr, color='#1f77b4', linestyle='-', linewidth=2.5,
                 label=f'Mean ROC (AUC = {mean_auc:.4f} $\\pm$ {std_auc:.4f})')
                 
        # Vẽ dải độ lệch chuẩn (std fill)
        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=0.2, label='$\\pm$ 1 std. dev.')
        
    plt.plot([0, 1], [0, 1], 'r--', label='Random Guessing (AUC = 0.5000)', linewidth=1.5)
    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.02])
    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('True Positive Rate (TPR)')
    plt.title(f'5-Fold Cross-Validation ROC Curves ({model_title})')
    plt.legend(loc='lower right', frameon=True, facecolor='white', shadow=True)
    plt.tight_layout()
    
    out_path = os.path.join(PLOTS_DIR, f"roc_5fold_{model_name}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"-> Đã lưu biểu đồ ROC 5-Folds tại: {out_path}")

# ----------------------------------------------------------------------
# 3. Vẽ các đường cong Loss & Accuracy curves (Training vs Validation)
# ----------------------------------------------------------------------
def plot_learning_curves(model_name="catboost", model_title="CatBoost"):
    print(f"Vẽ đường cong Loss và Accuracy của {model_title}...")
    filename = f"history_{model_name}.csv"
    filepath = os.path.join(LOGS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Không tìm thấy file lịch sử: {filepath}")
        return
        
    df = pd.read_csv(filepath)
    epochs = df['epoch']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # A. Biểu đồ Loss
    ax1.plot(epochs, df['train_loss'], color='#d62728', linestyle='-', linewidth=2, label='Training Loss')
    ax1.plot(epochs, df['val_loss'], color='#ff7f0e', linestyle='--', linewidth=2, label='Validation Loss')
    ax1.set_xlabel('Boosting Iterations (Epochs)')
    ax1.set_ylabel('Loss (Logloss)')
    ax1.set_title(f'{model_title} - Training and Validation Loss')
    ax1.legend(loc='upper right', frameon=True, shadow=True)
    
    # B. Biểu đồ Accuracy
    ax2.plot(epochs, df['train_acc'], color='#2ca02c', linestyle='-', linewidth=2, label='Training Accuracy')
    ax2.plot(epochs, df['val_acc'], color='#1f77b4', linestyle='--', linewidth=2, label='Validation Accuracy')
    ax2.set_xlabel('Boosting Iterations (Epochs)')
    ax2.set_ylabel('Accuracy')
    ax2.set_title(f'{model_title} - Training and Validation Accuracy')
    ax2.legend(loc='lower right', frameon=True, shadow=True)
    
    plt.suptitle(f'Learning Curves (Training vs Validation) - {model_title}', y=0.98)
    plt.tight_layout()
    
    out_path = os.path.join(PLOTS_DIR, f"learning_curves_{model_name}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"-> Đã lưu biểu đồ Learning Curves tại: {out_path}")

# ----------------------------------------------------------------------
# 4. Vẽ Confusion Matrix Heatmap cho mô hình tốt nhất (CatBoost)
# ----------------------------------------------------------------------
def plot_confusion_matrix_best_model():
    print("Vẽ Ma trận nhầm lẫn (Confusion Matrix) của CatBoost trên tập Test...")
    filepath = os.path.join(LOGS_DIR, "eval_catboost.csv")
    if not os.path.exists(filepath):
        print("Không có log eval của CatBoost.")
        return
        
    df = pd.read_csv(filepath)
    cm = confusion_matrix(df['y_true'], df['y_pred'])
    
    # Vẽ heatmap
    plt.figure(figsize=(6, 5))
    group_names = ['True Graduate (0)', 'False Dropout (1)', 'False Graduate (0)', 'True Dropout (1)']
    group_counts = ["{0:0.0f}".format(value) for value in cm.flatten()]
    group_percentages = ["{0:.2%}".format(value) for value in cm.flatten()/np.sum(cm)]
    
    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names, group_counts, group_percentages)]
    labels = np.asarray(labels).reshape(2, 2)
    
    sns.heatmap(cm, annot=labels, fmt='', cmap='Blues', cbar=True,
                xticklabels=['Graduate', 'Dropout'],
                yticklabels=['Graduate', 'Dropout'])
                
    plt.xlabel('Predicted Label')
    plt.ylabel('Actual Label')
    plt.title('Confusion Matrix (CatBoost best model) on Test Set')
    plt.tight_layout()
    
    out_path = os.path.join(PLOTS_DIR, "confusion_matrix_catboost.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"-> Đã lưu Confusion Matrix tại: {out_path}")

# Run all plotting functions
if __name__ == "__main__":
    print("=== BẮT ĐẦU VẼ CÁC BIỂU ĐỒ BÁO CÁO KHOA HỌC ===")
    plot_test_roc_comparison()
    plot_validation_roc_folds("catboost", "CatBoost")
    plot_validation_roc_folds("xgboost", "XGBoost")
    plot_learning_curves("catboost", "CatBoost")
    plot_learning_curves("xgboost", "XGBoost")
    plot_confusion_matrix_best_model()
    print("=== HOÀN THÀNH VẼ BIỂU ĐỒ THÀNH CÔNG! ===")
