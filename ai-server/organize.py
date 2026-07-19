import os
import shutil

def organize_files(base_dir):
    # Định nghĩa các thư mục đích
    data_dir = os.path.join(base_dir, "data")
    models_dir = os.path.join(base_dir, "models")
    results_dir = os.path.join(base_dir, "results")
    
    # Tạo các thư mục nếu chưa tồn tại
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Danh sách các file cần chuyển vào thư mục 'data'
    data_files = [
        "X_train_processed.npy",
        "X_test_processed.npy",
        "y_train.csv",
        "y_test.csv",
        "active_students.csv"
    ]
    
    # Danh sách các file cần chuyển vào thư mục 'models'
    model_files = [
        "preprocessor.pkl",
        "model_catboost.pkl",
        "model_random_forest.pkl",
        "model_xgboost.pkl",
        "ensemble_config.pkl"
    ]
    
    # Danh sách các file cần chuyển vào thư mục 'results'
    result_files = [
        "model_comparison_results.csv"
    ]
    
    print("--- Bắt đầu sắp xếp file ---")
    
    # Di chuyển các file data
    for f in data_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(data_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Đã chuyển: {f} -> data/")
            
    # Di chuyển các file model
    for f in model_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(models_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Đã chuyển: {f} -> models/")
            
    # Di chuyển các file kết quả
    for f in result_files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(results_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Đã chuyển: {f} -> results/")
            
    print("\n--- Sắp xếp hoàn tất! ---")

if __name__ == "__main__":
    organize_files("S:/Seminar/ai-server")
