# ✅ Danh sách việc cần làm — Student Early Warning System

> **Chiến lược**: Phát triển theo thứ tự từ dưới lên: AI Server → Backend → Frontend  
> **Mục tiêu bài báo**: Dùng 6 mô hình để so sánh, chọn Top 3 đưa vào Ensemble → tích hợp website

---

## 🔬 PHASE 1 — AI Server (Python + FastAPI)

### 1.1 Chuẩn bị môi trường

- [ ] Tạo thư mục `ai-server/` với cấu trúc project Python
- [ ] Tạo file `requirements.txt` với các thư viện: `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `numpy`, `joblib`, `xgboost`, `lightgbm`, `catboost`, `imbalanced-learn`, `shap`, `matplotlib`
- [ ] Tạo và kích hoạt môi trường ảo `venv`
- [ ] Cài đặt toàn bộ dependencies

### 1.2 Data Pipeline (Tiền xử lý dữ liệu)

- [ ] **Bước 1**: Đọc `data.csv` (phân cách `;`), chuẩn hóa tên cột
- [ ] **Bước 2**: Lọc dữ liệu huấn luyện — chỉ giữ `Graduate` và `Dropout`, loại `Enrolled`
- [ ] **Bước 3**: Mã hóa Target: `Dropout → 1`, `Graduate → 0`
- [ ] **Bước 4**: Feature Engineering — tạo 5 đặc trưng mới:
  - `Sem1_Approved_Ratio` = approved1 / enrolled1
  - `Sem2_Approved_Ratio` = approved2 / enrolled2
  - `Evaluation_Rate_Sem1` = evaluations1 / enrolled1
  - `Grade_Trend` = grade_sem2 - grade_sem1
  - `Financial_Risk` = 1 nếu (Debtor==1 OR Tuition_fees==0)
  - `Parental_Education_Score` = mother_qual + father_qual
- [ ] **Bước 5**: Chia train/test = 80/20 (stratified, random_state=42)
- [ ] **Bước 6**: Thiết lập `ColumnTransformer`:
  - Numerical: `StandardScaler`
  - Categorical: `OneHotEncoder(handle_unknown='ignore')`
  - Binary: `passthrough`
- [ ] **Bước 7**: Fit preprocessor trên X_train, transform X_test
- [ ] **Bước 8**: Áp dụng SMOTE trên tập train (sau chia, trước train)
- [ ] **Bước 9**: Lưu `preprocessor.pkl` và `active_students.csv`

### 1.3 Xây dựng 3 Checkpoint Model (Cho bài báo)

> Mỗi Checkpoint dùng tập features khác nhau

- [ ] **Checkpoint 1** (Lúc nhập học): Chỉ dùng nhân khẩu học + kinh tế-xã hội + điểm tuyển sinh
- [ ] **Checkpoint 2** (Sau HK1): Thêm kết quả học tập HK1
- [ ] **Checkpoint 3** (Sau HK2): Toàn bộ 36 đặc trưng + features mới

### 1.4 Huấn luyện và so sánh 6 mô hình (Nội dung bài báo)

> Thực hiện cho **Checkpoint 2** (mốc vàng) để so sánh trong bài báo

- [ ] **Mô hình 1**: Logistic Regression (baseline)
- [ ] **Mô hình 2**: Decision Tree
- [ ] **Mô hình 3**: Random Forest
- [ ] **Mô hình 4**: XGBoost
- [ ] **Mô hình 5**: LightGBM
- [ ] **Mô hình 6**: CatBoost
- [ ] Đánh giá tất cả 6 mô hình bằng **Stratified 5-Fold Cross-Validation**
- [ ] Thu thập chỉ số: `Accuracy`, `Precision`, `Recall`, `F1-Score`, `PR-AUC` cho **lớp Dropout**
- [ ] Vẽ bảng so sánh hiệu năng 6 mô hình → **đưa vào bài báo**
- [ ] Vẽ Confusion Matrix, ROC Curve, PR Curve cho từng mô hình

### 1.5 Xây dựng Ensemble Model (Tích hợp website)

- [ ] Chọn **Top 3** mô hình tốt nhất dựa theo F1-Score + PR-AUC của lớp Dropout
- [ ] Xây dựng **Soft Voting Ensemble** với trọng số theo F1-Score
  - `Risk Score(i) = w1*P_XGB + w2*P_LGBM + w3*P_Cat` (thay tên theo top 3 thực tế)
- [ ] Đánh giá lại Ensemble trên tập test
- [ ] Tối ưu hóa ngưỡng quyết định (threshold optimization thay vì mặc định 0.5)
- [ ] Lưu 3 mô hình thành phần: `model_xgb.pkl`, `model_lgbm.pkl`, `model_cat.pkl`
- [ ] Lưu Ensemble wrapper hoặc trọng số vào `ensemble_config.json`

### 1.6 Explainable AI — SHAP

- [ ] Tính SHAP values cho 3 mô hình thành phần
- [ ] Tạo **SHAP Summary Plot** (global) → đưa vào bài báo
- [ ] Tạo **SHAP Waterfall Plot** (per-student) → hiển thị trên Dashboard
- [ ] Tạo **SHAP Force Plot** (per-student)
- [ ] Lưu hàm `explain_student(student_features)` → trả về dict SHAP values

### 1.7 Phân loại Risk Level

- [ ] Áp dụng quy tắc phân nhóm:
  - Risk Score < 0.30 → `Low` (🟢)
  - 0.30 ≤ Risk Score ≤ 0.70 → `Medium` (🟡)
  - Risk Score > 0.70 → `High` (🔴)

### 1.8 Xây dựng FastAPI Server

- [ ] Tạo `main.py` khởi động FastAPI
- [ ] **Endpoint 1**: `POST /predict/single` — dự đoán 1 sinh viên
- [ ] **Endpoint 2**: `POST /predict/batch` — dự đoán nhiều sinh viên
- [ ] **Endpoint 3**: `GET /health` — kiểm tra trạng thái server
- [ ] Load model và preprocessor khi server khởi động (`lifespan` event)
- [ ] Định nghĩa **Pydantic schemas** cho Request/Response (input 36 features → output Risk Score + Risk Level + SHAP + Recommendations)
- [ ] Xử lý CORS cho phép Backend Laravel gọi đến
- [ ] Viết `Dockerfile` cho AI server (tùy chọn)

### 1.9 Kiểm thử AI Server

- [ ] Test endpoint đơn lẻ với dữ liệu mẫu từ `active_students.csv`
- [ ] Test endpoint batch với nhiều sinh viên
- [ ] Xác nhận SHAP values trả về đúng định dạng

---

## ⚙️ PHASE 2 — Backend (Laravel/PHP)

### 2.1 Chuẩn bị môi trường

- [ ] Cài đặt Laravel mới hoặc khởi tạo project trong thư mục `backend/`
- [ ] Cấu hình `.env`: `AI_SERVER_URL=http://localhost:8000`
- [ ] Cài `guzzlehttp/guzzle` để gọi HTTP đến AI server

### 2.2 API cho Single Prediction

- [ ] Route: `POST /api/predict/single`
- [ ] Validate 36 fields đầu vào (Request Validation)
- [ ] Map tên field frontend → tên field AI server
- [ ] Gọi AI server `POST /predict/single`
- [ ] Nhận kết quả và format response
- [ ] Lưu lịch sử dự đoán vào `storage/predictions/{date}.json`
- [ ] Trả response về Frontend

### 2.3 API cho Batch Prediction

- [ ] Route: `POST /api/predict/batch`
- [ ] Upload và validate file Excel (`.xlsx`)
- [ ] Parse Excel → array of student records (dùng `PhpSpreadsheet`)
- [ ] Gọi AI server `POST /predict/batch`
- [ ] Nhận kết quả và merge với thông tin hiển thị
- [ ] Lưu lịch sử batch vào JSON
- [ ] Tạo file Excel kết quả để export (thêm cột: Prediction, Risk Score, Risk Level, Recommendations)
- [ ] Trả về link download file Excel kết quả

### 2.4 API cho Prediction History

- [ ] Route: `GET /api/history` — lấy danh sách session lịch sử
- [ ] Route: `GET /api/history/{id}` — lấy chi tiết 1 session
- [ ] Route: `DELETE /api/history/{id}` — xóa 1 session (tùy chọn)

### 2.5 API cho Dashboard

- [ ] Route: `GET /api/dashboard/stats` — thống kê tổng quan:
  - Tổng số sinh viên đã dự đoán
  - Phân bố: Dropout / Graduate / Enrolled
  - Phân bố Risk Level: High / Medium / Low
- [ ] Cung cấp data cho các biểu đồ

### 2.6 Excel Template

- [ ] Tạo file Excel template mẫu trong `dataset/` để user download về nhập liệu
- [ ] Đặt header cột đúng với mapping field

### 2.7 Kiểm thử Backend

- [ ] Test tất cả API endpoints bằng Postman/Insomnia
- [ ] Test upload Excel và export kết quả

---

## 🖥️ PHASE 3 — Frontend (Vue 3 + TypeScript)

### 3.1 Kết nối Backend thực (thay thế Mock)

- [ ] Cập nhật `prediction.service.ts` — thay mock data bằng gọi API thực: `POST /api/predict/single`
- [ ] Cập nhật `upload.service.ts` — kết nối `POST /api/predict/batch`
- [ ] Cập nhật `dashboard.service.ts` — kết nối `GET /api/dashboard/stats`
- [ ] Cập nhật `history.service.ts` — kết nối `GET /api/history`
- [ ] Thêm base URL trong `.env`: `VITE_API_BASE_URL=http://localhost:8080/api`

### 3.2 Cập nhật kiểu dữ liệu (Types)

- [ ] Cập nhật `PredictionResult` trong `prediction.ts` — thêm trường `shap_values`, `risk_score`
- [ ] Thêm type cho SHAP response: `ShapFeature { name: string, value: number, impact: number }`

### 3.3 Trang Single Prediction — nâng cấp UI

- [ ] Chia form nhập liệu thành các bước (Step/Tab): Thông tin cá nhân → Học thuật HK1 → Học thuật HK2 → Kinh tế
- [ ] Thêm tooltip giải thích từng trường (vì nhiều trường phức tạp)
- [ ] Hiển thị kết quả với: Risk Score (% bỏ học), Risk Level badge (màu xanh/vàng/đỏ), danh sách Recommendations

### 3.4 Trang Prediction Result — hiển thị SHAP

- [ ] Hiển thị **SHAP Waterfall chart** hoặc **Bar chart** giải thích yếu tố ảnh hưởng
- [ ] Danh sách top 5 yếu tố đóng góp lớn nhất (tích cực / tiêu cực)
- [ ] Nhóm đề xuất can thiệp theo nguyên nhân (Học thuật / Tài chính / Tâm lý)

### 3.5 Trang Batch Prediction — nâng cấp

- [ ] Download template Excel mẫu
- [ ] Upload file Excel → preview bảng dữ liệu trước khi submit
- [ ] Hiển thị progress bar khi đang xử lý batch
- [ ] Bảng kết quả với cột Risk Level (màu badge) + Risk Score
- [ ] Nút Export kết quả ra Excel

### 3.6 Dashboard — nâng cấp biểu đồ

- [ ] Pie/Donut chart: phân bố Dropout / Graduate / Enrolled
- [ ] Bar chart: phân bố Risk Level (High / Medium / Low)
- [ ] Số liệu thống kê nhanh: tổng sinh viên, tỷ lệ nguy cơ cao
- [ ] Kết nối dữ liệu thực từ Backend API

### 3.7 Trang Prediction History

- [ ] Danh sách các session dự đoán (Single / Batch)
- [ ] Xem chi tiết từng session
- [ ] Filter theo ngày, loại dự đoán, risk level

---

## 📄 PHASE 4 — Tài liệu bài báo

### 4.1 Kết quả thực nghiệm (cần có số liệu thực)

- [ ] Bảng so sánh 6 mô hình (Checkpoint 2): Accuracy, Precision, Recall, F1, PR-AUC
- [ ] Bảng so sánh hiệu năng theo 3 Checkpoint (Checkpoint 1 vs 2 vs 3)
- [ ] Biểu đồ: ROC Curve của 6 mô hình trên cùng 1 đồ thị
- [ ] Biểu đồ: Confusion Matrix của Ensemble model
- [ ] SHAP Summary Plot: Top 15 features quan trọng nhất

### 4.2 Kiến trúc hệ thống (cho bài báo)

- [ ] Vẽ sơ đồ kiến trúc 3 lớp (Frontend → Backend → AI Server)
- [ ] Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram)
- [ ] Vẽ sơ đồ pipeline ML (Data → Preprocess → Train → Evaluate → Ensemble → SHAP → API)

---

## 🗂️ Thứ tự ưu tiên đề xuất

| Giai đoạn | Việc cần làm | Lý do |
|:---:|:---|:---|
| **1** | Phase 1.1 → 1.4 | Phải có dữ liệu & model mới làm được phần còn lại |
| **2** | Phase 1.5 → 1.8 | Ensemble + SHAP + API là trái tim của hệ thống |
| **3** | Phase 2 toàn bộ | Backend kết nối AI Server với Frontend |
| **4** | Phase 3.1 → 3.2 | Thay mock bằng API thực |
| **5** | Phase 3.3 → 3.7 | Hoàn thiện giao diện |
| **6** | Phase 4 | Thu thập số liệu thực → viết bài báo |

---

> 💡 **Gợi ý**: Bắt đầu từ việc chạy `Data_Setup_Guide.md` → `load_and_preprocess_data()` để xác nhận file `data.csv` đọc được. Đây là bước nền tảng cho tất cả các bước sau.
