import numpy as np
import pandas as pd
import pickle
import os
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, precision_recall_curve, auc
from imblearn.over_sampling import SMOTE

# 6 Thuật toán chính
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def evaluate_models(data_dir):
    print("--- Bước 1: Load dữ liệu đã tiền xử lý ---")
    # File dataset gốc là data.csv (đã được preprocess.py đọc, xử lý và chia thành các file dưới đây)
    real_data_dir = os.path.join(data_dir, "data")
    X_train = np.load(os.path.join(real_data_dir, "X_train_processed.npy"))
    y_train = pd.read_csv(os.path.join(real_data_dir, "y_train.csv"))['Target'].values
    
    X_test = np.load(os.path.join(real_data_dir, "X_test_processed.npy"))
    y_test = pd.read_csv(os.path.join(real_data_dir, "y_test.csv"))['Target'].values
    
    print(f"Kích thước X_train: {X_train.shape}, nhãn y_train: {y_train.shape}")
    print(f"Kích thước X_test: {X_test.shape}, nhãn y_test: {y_test.shape}")
    
    # Định nghĩa 6 mô hình
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
        "Decision Tree": DecisionTreeClassifier(class_weight='balanced', max_depth=10, random_state=42),
        "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42, n_estimators=100),
        "XGBoost": XGBClassifier(scale_pos_weight=1.5, eval_metric='logloss', random_state=42, use_label_encoder=False),
        "LightGBM": LGBMClassifier(class_weight='balanced', random_state=42, verbose=-1),
        "CatBoost": CatBoostClassifier(auto_class_weights='Balanced', random_state=42, verbose=0)
    }
    
    # Khởi tạo K-Fold
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = []
    
    print("\n--- Bước 2: Huấn luyện và đánh giá bằng Stratified 5-Fold Cross-Validation ---")
    
    for model_name, model in models.items():
        print(f"\nĐang đánh giá mô hình: {model_name}...")
        
        cv_accuracy = []
        cv_precision = []
        cv_recall = []
        cv_f1 = []
        cv_pr_auc = []
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
            X_tr, X_val = X_train[train_idx], X_train[val_idx]
            y_tr, y_val = y_train[train_idx], y_train[val_idx]
            
            # Áp dụng SMOTE chỉ trên tập train của fold hiện tại (tránh Data Leakage)
            smote = SMOTE(random_state=42)
            X_tr_resampled, y_tr_resampled = smote.fit_resample(X_tr, y_tr)
            
            # Train mô hình
            model.fit(X_tr_resampled, y_tr_resampled)
            
            # Predict
            preds = model.predict(X_val)
            probs = model.predict_proba(X_val)[:, 1]
            
            # Tính toán chỉ số cho lớp 1 (Dropout - nguy cơ cao)
            cv_accuracy.append(accuracy_score(y_val, preds))
            cv_precision.append(precision_score(y_val, preds, zero_division=0))
            cv_recall.append(recall_score(y_val, preds))
            cv_f1.append(f1_score(y_val, preds))
            
            # Tính PR-AUC (Chỉ số quan trọng khi lệch lớp)
            precision_pts, recall_pts, _ = precision_recall_curve(y_val, probs)
            cv_pr_auc.append(auc(recall_pts, precision_pts))
            
        # Lưu kết quả trung bình của 5 folds
        mean_results = {
            "Model": model_name,
            "Accuracy": np.mean(cv_accuracy),
            "Precision": np.mean(cv_precision),
            "Recall": np.mean(cv_recall),
            "F1-Score": np.mean(cv_f1),
            "PR-AUC": np.mean(cv_pr_auc)
        }
        results.append(mean_results)
        print(f"Kết quả {model_name} - F1: {mean_results['F1-Score']:.4f}, PR-AUC: {mean_results['PR-AUC']:.4f}")
        
    df_results = pd.DataFrame(results)
    
    print("\n--- BẢNG SO SÁNH HIỆU NĂNG 6 MÔ HÌNH (CV 5-FOLD) ---")
    print(df_results.to_markdown(index=False))
    
    # Lưu kết quả so sánh ra file csv để đưa vào viết báo
    results_dir = os.path.join(data_dir, "results")
    models_dir = os.path.join(data_dir, "models")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    df_results.to_csv(os.path.join(results_dir, "model_comparison_results.csv"), index=False)
    print(f"\nĐã lưu kết quả so sánh ra file: {os.path.join(results_dir, 'model_comparison_results.csv')}")
    
    # Tìm Top 3 mô hình tốt nhất dựa trên F1-Score để dùng cho Ensemble
    df_sorted = df_results.sort_values(by="F1-Score", ascending=False)
    top_3_names = df_sorted["Model"].head(3).tolist()
    print(f"\nTop 3 mô hình tốt nhất để đưa vào Ensemble trên Website: {top_3_names}")
    
    # Huấn luyện cả 6 mô hình trên toàn bộ X_train (đã resampling bằng SMOTE) và đánh giá trên tập Test để lưu log
    print("\n--- Bước 3: Đánh giá mô hình trên tập Test (20%) và lưu log vẽ biểu đồ ---")
    logs_dir = os.path.join(data_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    smote_full = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote_full.fit_resample(X_train, y_train)
    
    saved_models = {}
    for m_name, model in models.items():
        print(f"Đang train {m_name} trên toàn bộ dữ liệu Train...")
        model.fit(X_train_resampled, y_train_resampled)
        
        # Dự đoán trên Test set
        y_test_pred = model.predict(X_test)
        y_test_proba = model.predict_proba(X_test)[:, 1]
        
        # Tạo dataframe log để vẽ ROC, PR Curve, Confusion Matrix
        df_log = pd.DataFrame({
            'y_true': y_test,
            'y_pred': y_test_pred,
            'y_proba': y_test_proba
        })
        
        # Lưu file log csv riêng cho từng mô hình
        log_filename = f"eval_{m_name.lower().replace(' ', '_')}.csv"
        log_filepath = os.path.join(logs_dir, log_filename)
        df_log.to_csv(log_filepath, index=False)
        print(f"-> Đã lưu log vẽ biểu đồ của {m_name} tại: {log_filepath}")
        
        # Nếu thuộc Top 3 thì lưu lại file pkl để sử dụng trên Website
        if m_name in top_3_names:
            filename = f"model_{m_name.lower().replace(' ', '_')}.pkl"
            model_path = os.path.join(models_dir, filename)
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            print(f"-> Đã lưu mô hình Top 3: {model_path}")
            saved_models[m_name] = filename
        
    # Lưu cấu hình top 3 và trọng số (F1-score tương ứng) phục vụ Soft Voting Ensemble sau này
    ensemble_config = {
        "models": saved_models,
        "weights": {m_name: float(df_sorted[df_sorted["Model"] == m_name]["F1-Score"].values[0]) for m_name in top_3_names}
    }
    config_path = os.path.join(models_dir, "ensemble_config.pkl")
    with open(config_path, "wb") as f:
        pickle.dump(ensemble_config, f)
    print(f"Đã lưu cấu hình Ensemble vào: {config_path}")
    
    print("\n=== HOÀN THÀNH HUẤN LUYỆN VÀ ĐÁNH GIÁ THÀNH CÔNG! ===")

if __name__ == "__main__":
    evaluate_models("S:/Seminar/ai-server")
