import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def load_and_preprocess_data(csv_path, output_dir):
    print("--- Bước 1: Đọc file dữ liệu gốc ---")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại: {csv_path}")
        
    df = pd.read_csv(csv_path, sep=";")
    print(f"Kích thước tập dữ liệu thô: {df.shape}")
    
    # Chuẩn hóa tên cột (loại bỏ khoảng trắng thừa hoặc ký tự tab ẩn ở cuối cột)
    df.columns = df.columns.str.strip()
    
    # Xử lý đồng bộ cột Nacionality/Nationality
    if 'Nacionality' in df.columns:
        df = df.rename(columns={'Nacionality': 'Nationality'})
        print("Đã phát hiện và đổi tên cột 'Nacionality' thành 'Nationality'")

    print("\n--- Bước 2: Phân tách tập dữ liệu huấn luyện và sinh viên đang học ---")
    # Giai đoạn Huấn luyện nhị phân: Chỉ giữ lại Dropout và Graduate
    df_train_val = df[df['Target'] != 'Enrolled'].copy()
    df_train_val['Target'] = df_train_val['Target'].map({'Dropout': 1, 'Graduate': 0})
    print(f"Kích thước tập huấn luyện & kiểm thử (loại bỏ Enrolled): {df_train_val.shape}")
    print(f"Phân bố lớp Target: \n{df_train_val['Target'].value_counts()}")
    
    # Tách dữ liệu thực tế đang học (Enrolled) dùng để Dashboard dự đoán sau này
    df_active_students = df[df['Target'] == 'Enrolled'].copy()
    print(f"Kích thước tập sinh viên đang học hoạt động (Enrolled): {df_active_students.shape}")

    print("\n--- Bước 3: Thực hiện Kỹ nghệ đặc trưng (Feature Engineering) ---")
    for data in [df_train_val, df_active_students]:
        # 1. Tỷ lệ hoàn thành học phần kỳ 1 và kỳ 2 (tránh chia cho 0 bằng cách điền 0 nếu enrolled = 0)
        data['Sem1_Approved_Ratio'] = np.where(
            data['Curricular units 1st sem (enrolled)'] > 0,
            data['Curricular units 1st sem (approved)'] / data['Curricular units 1st sem (enrolled)'],
            0.0
        )
        data['Sem2_Approved_Ratio'] = np.where(
            data['Curricular units 2nd sem (enrolled)'] > 0,
            data['Curricular units 2nd sem (approved)'] / data['Curricular units 2nd sem (enrolled)'],
            0.0
        )
        
        # 2. Mức độ tích cực thi cử kỳ 1
        data['Evaluation_Rate_Sem1'] = np.where(
            data['Curricular units 1st sem (enrolled)'] > 0,
            data['Curricular units 1st sem (evaluations)'] / data['Curricular units 1st sem (enrolled)'],
            0.0
        )
        
        # 3. Xu hướng tiến bộ điểm số (kỳ 2 - kỳ 1)
        data['Grade_Trend'] = data['Curricular units 2nd sem (grade)'] - data['Curricular units 1st sem (grade)']
        
        # 4. Chỉ số rủi ro tài chính
        data['Financial_Risk'] = ((data['Debtor'] == 1) | (data['Tuition fees up to date'] == 0)).astype(int)
        
        # 5. Chỉ số hỗ trợ học tập từ gia đình
        data['Parental_Education_Score'] = data["Mother's qualification"] + data["Father's qualification"]

    print("Đã hoàn thành thêm 6 đặc trưng mới.")

    print("\n--- Bước 4: Phân tách Features (X) và Target (y) ---")
    X = df_train_val.drop(columns=['Target'])
    y = df_train_val['Target']
    
    print("\n--- Bước 5: Phân chia Train/Test tỷ lệ 80/20 có Stratified ---")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Kích thước X_train: {X_train.shape}, X_test: {X_test.shape}")

    print("\n--- Bước 6: Thiết lập bộ Tiền xử lý tự động (ColumnTransformer) ---")
    # Định nghĩa danh sách cột
    num_features = [
        'Application order', 'Age at enrollment', 'Admission grade', 'Previous qualification (grade)',
        'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
        'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
        'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)',
        'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
        'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',
        'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)',
        'Unemployment rate', 'Inflation rate', 'GDP',
        # Các đặc trưng số mới tạo
        'Sem1_Approved_Ratio', 'Sem2_Approved_Ratio', 'Evaluation_Rate_Sem1', 'Grade_Trend', 'Parental_Education_Score'
    ]

    cat_features = [
        'Marital status', 'Course', 'Nationality', 'Application mode',
        'Previous qualification', "Mother's qualification", "Father's qualification",
        "Mother's occupation", "Father's occupation"
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ],
        remainder='passthrough'
    )
    
    print("\n--- Bước 7: Huấn luyện bộ tiền xử lý trên tập Train ---")
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    print(f"Kích thước X_train sau tiền xử lý: {X_train_processed.shape}")
    print(f"Kích thước X_test sau tiền xử lý: {X_test_processed.shape}")
    
    # Tạo các thư mục con nếu chưa có
    data_dir = os.path.join(output_dir, "data")
    models_dir = os.path.join(output_dir, "models")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    # Lưu các file kết quả
    preprocessor_path = os.path.join(models_dir, "preprocessor.pkl")
    active_students_path = os.path.join(data_dir, "active_students.csv")
    
    print(f"\n--- Bước 8: Lưu trữ kết quả đầu ra ---")
    with open(preprocessor_path, "wb") as f:
        pickle.dump(preprocessor, f)
    print(f"Đã lưu bộ tiền xử lý vào: {preprocessor_path}")
    
    df_active_students.to_csv(active_students_path, index=False)
    print(f"Đã lưu tập sinh viên đang học hoạt động vào: {active_students_path}")
    
    # Lưu X_train, X_test, y_train, y_test dạng numpy/pandas để tiện cho bước train model sau này
    np.save(os.path.join(data_dir, "X_train_processed.npy"), X_train_processed)
    np.save(os.path.join(data_dir, "X_test_processed.npy"), X_test_processed)
    y_train.to_csv(os.path.join(data_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(data_dir, "y_test.csv"), index=False)
    print("Đã lưu các file numpy trung gian vào thư mục 'data/' phục vụ cho quá trình huấn luyện mô hình.")
    
    print("\n=== HOÀN THÀNH TIỀN XỬ LÝ DỮ LIỆU THÀNH CÔNG! ===")

if __name__ == "__main__":
    csv_file = "S:/Seminar/ai-server/predict+students+dropout+and+academic+success/data.csv"
    output_directory = "S:/Seminar/ai-server"
    load_and_preprocess_data(csv_file, output_directory)
