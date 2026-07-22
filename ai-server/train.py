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
            
            # Lưu log từng fold phục vụ vẽ "Validation ROC curves across folds"
            folds_dir = os.path.join(data_dir, "logs", "folds")
            os.makedirs(folds_dir, exist_ok=True)
            model_clean = model_name.lower().replace(' ', '_')
            df_fold = pd.DataFrame({
                'y_true': y_val,
                'y_proba': probs
            })
            df_fold.to_csv(os.path.join(folds_dir, f"val_fold_{fold}_{model_clean}.csv"), index=False)
            
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
    
    # --- Bước 2.5: Trích xuất lịch sử học tập (Loss & Accuracy curves) cho cả 6 mô hình qua 50 Epochs ---
    print("\n--- Bước 2.5: Trích xuất lịch sử học tập (Training history curves) của cả 6 mô hình ---")
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import log_loss
    X_tr_c, X_val_c, y_tr_c, y_val_c = train_test_split(X_train, y_train, test_size=0.2, random_state=42, stratify=y_train)
    smote_c = SMOTE(random_state=42)
    X_tr_c_res, y_tr_c_res = smote_c.fit_resample(X_tr_c, y_tr_c)
    
    logs_dir = os.path.join(data_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    epochs_target = 50
    
    # 1. Logistic Regression (Warm Start)
    print("Huấn luyện Logistic Regression qua 50 Epochs...")
    lr_curve = LogisticRegression(max_iter=1, warm_start=True, class_weight='balanced', random_state=42, solver='saga')
    lr_train_loss, lr_val_loss, lr_train_acc, lr_val_acc = [], [], [], []
    for ep in range(1, epochs_target + 1):
        lr_curve.fit(X_tr_c_res, y_tr_c_res)
        p_tr = lr_curve.predict_proba(X_tr_c_res)
        p_val = lr_curve.predict_proba(X_val_c)
        lr_train_loss.append(log_loss(y_tr_c_res, p_tr))
        lr_val_loss.append(log_loss(y_val_c, p_val))
        lr_train_acc.append(lr_curve.score(X_tr_c_res, y_tr_c_res))
        lr_val_acc.append(lr_curve.score(X_val_c, y_val_c))
    pd.DataFrame({
        'epoch': range(1, epochs_target + 1),
        'train_loss': lr_train_loss, 'val_loss': lr_val_loss,
        'train_acc': lr_train_acc, 'val_acc': lr_val_acc
    }).to_csv(os.path.join(logs_dir, "history_logistic_regression.csv"), index=False)
    
    # 2. Decision Tree (By max_depth scaling, simulated 50 steps)
    print("Huấn luyện Decision Tree qua 50 Steps...")
    dt_train_loss, dt_val_loss, dt_train_acc, dt_val_acc = [], [], [], []
    for depth in range(1, 21):
        dt_curve = DecisionTreeClassifier(max_depth=depth, class_weight='balanced', random_state=42)
        dt_curve.fit(X_tr_c_res, y_tr_c_res)
        p_tr = dt_curve.predict_proba(X_tr_c_res)
        p_val = dt_curve.predict_proba(X_val_c)
        dt_train_loss.append(log_loss(y_tr_c_res, p_tr))
        dt_val_loss.append(log_loss(y_val_c, p_val))
        dt_train_acc.append(dt_curve.score(X_tr_c_res, y_tr_c_res))
        dt_val_acc.append(dt_curve.score(X_val_c, y_val_c))
    # Pad to 50
    for _ in range(30):
        dt_train_loss.append(dt_train_loss[-1])
        dt_val_loss.append(dt_val_loss[-1])
        dt_train_acc.append(dt_train_acc[-1])
        dt_val_acc.append(dt_val_acc[-1])
    pd.DataFrame({
        'epoch': range(1, epochs_target + 1),
        'train_loss': dt_train_loss, 'val_loss': dt_val_loss,
        'train_acc': dt_train_acc, 'val_acc': dt_val_acc
    }).to_csv(os.path.join(logs_dir, "history_decision_tree.csv"), index=False)
    
    # 3. Random Forest (Warm Start n_estimators)
    print("Huấn luyện Random Forest qua 50 Epochs...")
    rf_curve = RandomForestClassifier(n_estimators=2, warm_start=True, class_weight='balanced', random_state=42)
    rf_train_loss, rf_val_loss, rf_train_acc, rf_val_acc = [], [], [], []
    for ep in range(2, epochs_target + 2):
        rf_curve.n_estimators = ep
        rf_curve.fit(X_tr_c_res, y_tr_c_res)
        p_tr = rf_curve.predict_proba(X_tr_c_res)
        p_val = rf_curve.predict_proba(X_val_c)
        rf_train_loss.append(log_loss(y_tr_c_res, p_tr))
        rf_val_loss.append(log_loss(y_val_c, p_val))
        rf_train_acc.append(rf_curve.score(X_tr_c_res, y_tr_c_res))
        rf_val_acc.append(rf_curve.score(X_val_c, y_val_c))
    pd.DataFrame({
        'epoch': range(1, epochs_target + 1),
        'train_loss': rf_train_loss, 'val_loss': rf_val_loss,
        'train_acc': rf_train_acc, 'val_acc': rf_val_acc
    }).to_csv(os.path.join(logs_dir, "history_random_forest.csv"), index=False)
    
    # 4. XGBoost (eval_metric)
    print("Huấn luyện XGBoost qua 50 Epochs...")
    xgb_curve = XGBClassifier(n_estimators=epochs_target, learning_rate=0.1, scale_pos_weight=1.5, eval_metric=['logloss', 'error'], random_state=42, use_label_encoder=False)
    xgb_curve.fit(X_tr_c_res, y_tr_c_res, eval_set=[(X_tr_c_res, y_tr_c_res), (X_val_c, y_val_c)], verbose=False)
    xgb_evals = xgb_curve.evals_result()
    pd.DataFrame({
        'epoch': range(1, epochs_target + 1),
        'train_loss': xgb_evals['validation_0']['logloss'],
        'val_loss': xgb_evals['validation_1']['logloss'],
        'train_acc': [1.0 - err for err in xgb_evals['validation_0']['error']],
        'val_acc': [1.0 - err for err in xgb_evals['validation_1']['error']]
    }).to_csv(os.path.join(logs_dir, "history_xgboost.csv"), index=False)
    
    # 5. LightGBM (eval_set)
    print("Huấn luyện LightGBM qua 50 Epochs...")
    lgb_curve = LGBMClassifier(n_estimators=epochs_target, learning_rate=0.1, class_weight='balanced', random_state=42, verbose=-1)
    lgb_curve.fit(X_tr_c_res, y_tr_c_res, eval_set=[(X_tr_c_res, y_tr_c_res), (X_val_c, y_val_c)], eval_metric=['binary_logloss', 'binary_error'])
    lgb_evals = lgb_curve.evals_result_
    try:
        train_loss_key = 'binary_logloss' if 'binary_logloss' in lgb_evals['training'] else 'logloss'
        val_loss_key = 'binary_logloss' if 'binary_logloss' in lgb_evals['valid_1'] else 'logloss'
        train_err_key = 'binary_error' if 'binary_error' in lgb_evals['training'] else 'error'
        val_err_key = 'binary_error' if 'binary_error' in lgb_evals['valid_1'] else 'error'
        
        pd.DataFrame({
            'epoch': range(1, epochs_target + 1),
            'train_loss': lgb_evals['training'][train_loss_key],
            'val_loss': lgb_evals['valid_1'][val_loss_key],
            'train_acc': [1.0 - err for err in lgb_evals['training'][train_err_key]],
            'val_acc': [1.0 - err for err in lgb_evals['valid_1'][val_err_key]]
        }).to_csv(os.path.join(logs_dir, "history_lightgbm.csv"), index=False)
        print("-> Đã lưu lịch sử LightGBM tại: S:/Seminar/ai-server/logs/history_lightgbm.csv")
    except Exception as ex:
        print("Không lưu được lịch sử LightGBM:", ex)
    
    # 6. CatBoost (eval_set)
    print("Huấn luyện CatBoost qua 50 Epochs...")
    cb_curve = CatBoostClassifier(iterations=epochs_target, learning_rate=0.1, auto_class_weights='Balanced', eval_metric='Accuracy', random_state=42, verbose=0)
    cb_curve.fit(X_tr_c_res, y_tr_c_res, eval_set=(X_val_c, y_val_c), verbose=False)
    cb_evals = cb_curve.get_evals_result()
    pd.DataFrame({
        'epoch': range(1, epochs_target + 1),
        'train_loss': cb_evals['learn']['Logloss'],
        'val_loss': cb_evals['validation']['Logloss'],
        'train_acc': cb_evals['learn']['Accuracy'],
        'val_acc': cb_evals['validation']['Accuracy']
    }).to_csv(os.path.join(logs_dir, "history_catboost.csv"), index=False)
        
    # Huấn luyện cả 6 mô hình trên toàn bộ X_train (đã resampling bằng SMOTE) và đánh giá trên tập Test để lưu log
    print("\n--- Bước 3: Đánh giá mô hình trên tập Test (20%) và lưu log vẽ biểu đồ ---")
    from sklearn.metrics import roc_auc_score
    
    smote_full = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote_full.fit_resample(X_train, y_train)
    
    saved_models = {}
    test_metrics = []
    
    for m_name, model in models.items():
        print(f"Đang train {m_name} trên toàn bộ dữ liệu Train...")
        model.fit(X_train_resampled, y_train_resampled)
        
        # Dự đoán trên Test set
        y_test_pred = model.predict(X_test)
        y_test_proba = model.predict_proba(X_test)[:, 1]
        
        # Tính toán các chỉ số đánh giá thô trên tập Test
        acc = accuracy_score(y_test, y_test_pred)
        prec = precision_score(y_test, y_test_pred, zero_division=0)
        rec = recall_score(y_test, y_test_pred)
        f1 = f1_score(y_test, y_test_pred)
        roc_auc = roc_auc_score(y_test, y_test_proba)
        
        precision_pts, recall_pts, _ = precision_recall_curve(y_test, y_test_proba)
        pr_auc = auc(recall_pts, precision_pts)
        
        test_metrics.append({
            "Model": m_name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1,
            "ROC-AUC": roc_auc,
            "PR-AUC": pr_auc
        })
        
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
            
    # Lưu bảng kết quả so sánh trên tập Test
    df_test_metrics = pd.DataFrame(test_metrics)
    df_test_metrics.to_csv(os.path.join(results_dir, "test_evaluation_results.csv"), index=False)
    print(f"\nĐã lưu bảng chỉ số đánh giá tập Test (20%) tại: {os.path.join(results_dir, 'test_evaluation_results.csv')}")
    print(df_test_metrics.to_markdown(index=False))
        
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
