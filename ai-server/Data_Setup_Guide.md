# HƯỚNG DẪN THIẾT LẬP ĐẦU VÀO DỮ LIỆU (DATA PIPELINE SETUP)

Tài liệu này hướng dẫn chi tiết cách thiết lập, phân loại và tiền xử lý dữ liệu đầu vào từ file `data.csv` của bộ dữ liệu **"Predict Students Dropout and Academic Success" (UCI)** để phục vụ cho việc huấn luyện mô hình Machine Learning và tích hợp vào hệ thống Dashboard cảnh báo sớm.

---

## 1. Quy tắc xử lý Biến mục tiêu (Target)

Bộ dữ liệu gốc chứa 3 trạng thái trong cột `Target`: `Graduate` (Tốt nghiệp), `Dropout` (Bỏ học), và `Enrolled` (Đang học). Để xây dựng mô hình có hiệu năng cao và đúng logic thực tế, ta áp dụng quy tắc sau:

*   **Giai đoạn Huấn luyện (Training Phase):**
    *   **Loại bỏ nhóm `Enrolled`**: Chỉ giữ lại các dòng dữ liệu của những sinh viên đã có kết quả rõ ràng là `Graduate` hoặc `Dropout`.
    *   **Mã hóa nhị phân**: Chuyển đổi cột `Target` thành dạng số:
        *   `Dropout` $\rightarrow$ **1** (Lớp tích cực - sinh viên có nguy cơ/cần cảnh báo).
        *   `Graduate` $\rightarrow$ **0** (Lớp tiêu cực - sinh viên an toàn/tốt nghiệp).
    *   *Ý nghĩa*: Việc này giúp thuật toán phân loại (như XGBoost, Random Forest) học được ranh giới rõ ràng nhất giữa các yếu tố dẫn đến bỏ học và tốt nghiệp từ dữ liệu lịch sử.
*   **Giai đoạn Ứng dụng (Deployment Phase):**
    *   Khi hệ thống đi vào hoạt động, ta sẽ nạp dữ liệu của những sinh viên đang học (`Enrolled`) vào mô hình.
    *   Mô hình sẽ dự đoán xác suất sinh viên đó thuộc lớp `Dropout` (giá trị từ 0.0 đến 1.0). Xác suất này chính là **Risk Score (Điểm số rủi ro)** hiển thị trên Dashboard.

---

## 2. Phân nhóm các đặc trưng đầu vào (Features Classification)

Cần phân loại 36 đặc trưng đầu vào của file `data.csv` thành các nhóm riêng biệt để áp dụng các phương pháp tiền xử lý phù hợp, tránh lỗi rò rỉ dữ liệu (`Data Leakage`):

### 2.1. Nhóm đặc trưng số (Numerical Features)
Các đặc trưng này có giá trị liên tục, cần được chuẩn hóa bằng phương pháp **Standardization** (đưa về phân phối chuẩn có trung bình $\mu = 0$ và độ lệch chuẩn $\sigma = 1$) để đảm bảo các mô hình tuyến tính hoặc thuật toán khoảng cách hoạt động ổn định.

*   `Application order` (Thứ tự nguyện vọng đăng ký - *cột bị bỏ sót ở tài liệu cũ*)
*   `Age at enrollment` (Tuổi khi nhập học)
*   `Admission grade` (Điểm xét tuyển đầu vào)
*   `Previous qualification (grade)` (Điểm bằng cấp trước đó)
*   `Curricular units 1st sem (credited)` (Tín chỉ miễn giảm HK1)
*   `Curricular units 1st sem (enrolled)` (Tín chỉ đăng ký HK1)
*   `Curricular units 1st sem (evaluations)` (Số lượt đánh giá/thi HK1)
*   `Curricular units 1st sem (approved)` (Tín chỉ tích lũy thành công HK1)
*   `Curricular units 1st sem (grade)` (Điểm trung bình HK1)
*   `Curricular units 1st sem (without evaluations)` (Tín chỉ không có đánh giá HK1)
*   `Curricular units 2nd sem (credited)` (Tín chỉ miễn giảm HK2)
*   `Curricular units 2nd sem (enrolled)` (Tín chỉ đăng ký HK2)
*   `Curricular units 2nd sem (evaluations)` (Số lượt đánh giá/thi HK2)
*   `Curricular units 2nd sem (approved)` (Tín chỉ tích lũy thành công HK2)
*   `Curricular units 2nd sem (grade)` (Điểm trung bình HK2)
*   `Curricular units 2nd sem (without evaluations)` (Tín chỉ không có đánh giá HK2)
*   `Unemployment rate` (Tỷ lệ thất nghiệp vĩ mô)
*   `Inflation rate` (Tỷ lệ lạm phát vĩ mô)
*   `GDP` (Chỉ số tăng trưởng GDP vĩ mô)

### 2.2. Nhóm đặc trưng phân loại (Categorical Features)
Các cột này được lưu dưới dạng số nguyên nhưng mang bản chất định danh (Nominal), cần áp dụng **One-Hot Encoding** để chuyển đổi thành các cột nhị phân (0 hoặc 1), tránh việc mô hình coi các mã số này là biến liên tục có thứ tự.

*   `Marital status` (Tình trạng hôn nhân: 1-Độc thân, 2-Kết hôn,...)
*   `Course` (Mã ngành học: 33, 171, 9254,...)
*   `Nationality` (Quốc tịch)
*   `Application mode` (Phương thức tuyển sinh)
*   `Previous qualification` (Bằng cấp trước đó)
*   `Mother's qualification` & `Father's qualification` (Trình độ học vấn của bố/mẹ)
*   `Mother's occupation` & `Father's occupation` (Nghề nghiệp của bố/mẹ)

### 2.3. Nhóm đặc trưng nhị phân (Binary Features)
Đây là các đặc trưng có sẵn giá trị 0 hoặc 1, được **giữ nguyên (Pass-through)** không cần xử lý thêm.

*   `Gender` (Giới tính: 1-Nam, 0-Nữ)
*   `Daytime/evening attendance` (Ca học: 1-Ngày, 0-Tối - *lưu ý trong file CSV gốc có tab ẩn cuối tên cột `"Daytime/evening attendance\t"`, cần strip để loại bỏ*)
*   `Displaced` (Diện xa nhà: 1-Có, 0-Không)
*   `Educational special needs` (Nhu cầu giáo dục đặc biệt: 1-Có, 0-Không)
*   `Debtor` (Có nợ phí học tập hay không: 1-Có, 0-Không)
*   `Tuition fees up to date` (Đóng học phí đúng hạn: 1-Đã đóng đủ, 0-Còn nợ)
*   `Scholarship holder` (Có học bổng: 1-Có, 0-Không)
*   `International` (Sinh viên quốc tế: 1-Có, 0-Không)

---

## 3. Thiết lập Data Pipeline bằng Python (Scikit-Learn)

Dưới đây là mã nguồn Python chuẩn mực để thực hiện tiền xử lý dữ liệu tự động. Script này tách biệt quá trình tiền xử lý để có thể dễ dàng lưu lại (`export`) phục vụ cho Dashboard Streamlit.

```python
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_and_preprocess_data(csv_path):
    # 1. Đọc file dữ liệu gốc
    df = pd.read_csv(csv_path, sep=";")
    
    # Chuẩn hóa tên cột (loại bỏ khoảng trắng thừa hoặc ký tự tab ẩn ở cuối cột)
    df.columns = df.columns.str.strip()
    
    # 2. Tách dữ liệu huấn luyện (Huấn luyện nhị phân: Dropout vs Graduate)
    df_train_val = df[df['Target'] != 'Enrolled'].copy()
    df_train_val['Target'] = df_train_val['Target'].map({'Dropout': 1, 'Graduate': 0})
    
    # Tách dữ liệu thực tế đang học (Enrolled) dùng để Dashboard dự đoán sau này
    df_active_students = df[df['Target'] == 'Enrolled'].copy()
    
    # 3. Phân tách Features (X) và Target (y)
    X = df_train_val.drop(columns=['Target'])
    y = df_train_val['Target']
    
    # 4. Phân chia Train/Test tỷ lệ 80/20 có Stratified (phân tầng theo tỷ lệ lớp Target)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 5. Khai báo danh sách các cột theo nhóm xử lý
    num_features = [
        'Application order', 'Age at enrollment', 'Admission grade', 'Previous qualification (grade)',
        'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
        'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
        'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)',
        'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
        'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',
        'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)',
        'Unemployment rate', 'Inflation rate', 'GDP'
    ]

    cat_features = [
        'Marital status', 'Course', 'Nationality', 'Application mode',
        'Previous qualification', "Mother's qualification", "Father's qualification",
        "Mother's occupation", "Father's occupation"
    ]
    
    # 6. Thiết lập bộ Tiền xử lý tự động (ColumnTransformer)
    # handle_unknown='ignore' giúp tránh lỗi khi gặp mã ngành học/quốc tịch mới trong tương lai
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ],
        remainder='passthrough' # Giữ nguyên các cột nhị phân (Gender, Debtor, Tuition,...)
    )
    
    # 7. Huấn luyện bộ tiền xử lý trên tập huấn luyện
    # Điều này đảm bảo StandardScaler chỉ tính toán trung bình/độ lệch chuẩn dựa trên X_train
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    print(f"Kích thước tập huấn luyện sau tiền xử lý: {X_train_processed.shape}")
    print(f"Kích thước tập kiểm thử sau tiền xử lý: {X_test_processed.shape}")
    
    return preprocessor, X_train_processed, X_test_processed, y_train, y_test, df_active_students

# Chạy thử nghiệm và lưu trữ bộ tiền xử lý
if __name__ == "__main__":
    csv_file_path = "S:/Seminar/predict+students+dropout+and+academic+success/data.csv"
    preprocessor, X_train, X_test, y_train, y_test, active_df = load_and_preprocess_data(csv_file_path)
    
    # Lưu bộ tiền xử lý preprocessor để sử dụng lại trong file chạy thử nghiệm và Dashboard
    with open("S:/Seminar/preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)
    
    # Lưu tập dữ liệu sinh viên đang học hoạt động (Enrolled) để Dashboard truy vấn mẫu
    active_df.to_csv("S:/Seminar/active_students.csv", index=False)
    print("Đã lưu preprocessor.pkl và active_students.csv thành công!")
```

---

## 4. Các lưu ý cốt lõi khi tích hợp vào Dashboard (Streamlit)

1.  **Đồng bộ định dạng đầu vào**: Khi cố vấn học tập tra cứu một sinh viên đang học (`active_students.csv`), hệ thống cần:
    *   Lấy toàn bộ 36 đặc trưng của sinh viên đó (loại bỏ cột `Target`).
    *   Sử dụng file `preprocessor.pkl` đã load để biến đổi: `X_processed = preprocessor.transform(student_features_df)`.
    *   Đưa `X_processed` vào mô hình để tính xác suất bỏ học (`model.predict_proba(X_processed)[:, 1]`).
2.  **Độ tương thích SHAP**: 
    *   Khi sử dụng SHAP để giải thích mô hình Boosting, việc giải thích dữ liệu sau khi mã hóa One-Hot sẽ tạo ra rất nhiều cột nhị phân (ví dụ: `Course_171`, `Course_9254`). 
    *   *Mẹo*: Để giảng viên dễ đọc biểu đồ SHAP, bạn có thể truyền tên cột sau khi biến đổi (`preprocessor.get_feature_names_out()`) vào đối tượng giải thích SHAP để biểu thị rõ ràng tên biến (ví dụ: `cat__Course_9254` hoặc chuẩn hóa lại thành dạng dễ hiểu).
3.  **Kỹ nghệ đặc trưng trước hay sau ColumnTransformer?**:
    *   Nếu bạn tự viết thêm các đặc trưng mới (như `Sem_Approved_Rate` hay `Financial_Risk` trong **Mục 5** của tài liệu chính), bạn cần thực hiện tính toán các cột này **trước** khi đưa qua `ColumnTransformer`. Hãy thêm các phép toán tính cột trực tiếp vào dataframe trước bước chia Train/Test.
