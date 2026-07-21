import os
import pickle
import numpy as np
import pandas as pd
import shap
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from contextlib import asynccontextmanager

# ----------------------------------------------------------------------
# 1. Định nghĩa Schema đầu vào & đầu ra từ Frontend / Laravel
# ----------------------------------------------------------------------
class StudentInput(BaseModel):
    # Thông tin hiển thị (Display information)
    studentCode: str
    studentName: str
    className: str
    faculty: str
    
    # 36 Đặc trưng đưa vào mô hình AI
    maritalStatus: int
    applicationMode: int
    applicationOrder: int
    course: int
    daytimeEvening: int
    previousQualification: int
    previousQualificationGrade: float
    admissionGrade: float
    displaced: int
    educationalSpecialNeeds: int
    debtor: int
    tuitionFeesUpToDate: int
    gender: int
    scholarshipHolder: int
    ageAtEnrollment: int
    international: int
    nationality: int
    motherQualification: int
    fatherQualification: int
    motherOccupation: int
    fatherOccupation: int
    sem1Credited: int
    sem1Enrolled: int
    sem1Evaluations: int
    sem1Approved: int
    sem1Grade: float
    sem1WithoutEvaluations: int
    sem2Credited: int
    sem2Enrolled: int
    sem2Evaluations: int
    sem2Approved: int
    sem2Grade: float
    sem2WithoutEvaluations: int
    unemploymentRate: float
    inflationRate: float
    gdp: float

class RecommendationResponse(BaseModel):
    prediction: str
    probability: float
    riskLevel: str
    confidence: float
    recommendations: List[str]
    shapValues: List[Dict[str, Any]]

class StudentPredictionResponse(BaseModel):
    id: str
    studentCode: str
    studentName: str
    className: str
    faculty: str
    prediction: str
    probability: float
    riskLevel: str
    confidence: float
    recommendations: List[str]
    shapValues: List[Dict[str, Any]]

# Từ điển ánh xạ từ camelCase (Frontend) sang tên cột gốc trong CSV
FIELD_MAPPING = {
    "maritalStatus": "Marital status",
    "applicationMode": "Application mode",
    "applicationOrder": "Application order",
    "course": "Course",
    "daytimeEvening": "Daytime/evening attendance",
    "previousQualification": "Previous qualification",
    "previousQualificationGrade": "Previous qualification (grade)",
    "admissionGrade": "Admission grade",
    "displaced": "Displaced",
    "educationalSpecialNeeds": "Educational special needs",
    "debtor": "Debtor",
    "tuitionFeesUpToDate": "Tuition fees up to date",
    "gender": "Gender",
    "scholarshipHolder": "Scholarship holder",
    "ageAtEnrollment": "Age at enrollment",
    "international": "International",
    "nationality": "Nationality",
    "motherQualification": "Mother's qualification",
    "fatherQualification": "Father's qualification",
    "motherOccupation": "Mother's occupation",
    "fatherOccupation": "Father's occupation",
    "sem1Credited": "Curricular units 1st sem (credited)",
    "sem1Enrolled": "Curricular units 1st sem (enrolled)",
    "sem1Evaluations": "Curricular units 1st sem (evaluations)",
    "sem1Approved": "Curricular units 1st sem (approved)",
    "sem1Grade": "Curricular units 1st sem (grade)",
    "sem1WithoutEvaluations": "Curricular units 1st sem (without evaluations)",
    "sem2Credited": "Curricular units 2nd sem (credited)",
    "sem2Enrolled": "Curricular units 2nd sem (enrolled)",
    "sem2Evaluations": "Curricular units 2nd sem (evaluations)",
    "sem2Approved": "Curricular units 2nd sem (approved)",
    "sem2Grade": "Curricular units 2nd sem (grade)",
    "sem2WithoutEvaluations": "Curricular units 2nd sem (without evaluations)",
    "unemploymentRate": "Unemployment rate",
    "inflationRate": "Inflation rate",
    "gdp": "GDP"
}

# Ngân hàng đề xuất can thiệp cá nhân hóa (Personalized Recommendations)
RECOMMENDATIONS_DB = {
    "Graduate": [
        "Tiếp tục duy trì kết quả học tập xuất sắc và tỷ lệ chuyên cần hiện tại.",
        "Xem xét đăng ký làm gia sư hoặc người hướng dẫn học tập (Peer Mentor) cho khóa dưới.",
        "Tham gia các hoạt động nghiên cứu khoa học sinh viên hoặc đồ án danh dự.",
        "Tham gia các chương trình tư vấn hướng nghiệp và ngày hội thực tập của khoa."
    ],
    "Enrolled": [
        "Đặt lịch hẹn với cố vấn học tập để rà soát tiến độ tích lũy tín chỉ.",
        "Sử dụng phòng tự học và tài liệu thư viện để chuẩn bị tốt cho các bài đánh giá.",
        "Tham gia các câu lạc bộ học thuật để bổ trợ kỹ năng.",
        "Xác nhận lại chi tiết đăng ký môn học và điều kiện tiên quyết cho các kỳ học tới."
    ],
    "Dropout": [
        "Liên hệ khẩn cấp với cố vấn học tập hoặc văn phòng hỗ trợ sinh viên của Khoa.",
        "Liên hệ phòng kế hoạch tài chính để nhận hỗ trợ trả góp học phí hoặc giãn nợ học phí.",
        "Đăng ký tham gia lớp phụ đạo (Peer-tutoring) cho các môn học có tỷ lệ trượt cao.",
        "Xem xét chuyển sang hệ vừa học vừa làm (lớp tối) để cân bằng thời gian cá nhân.",
        "Chủ động giảm tải số lượng tín chỉ đăng ký ở kỳ sau để tránh áp lực học tập quá tải."
    ]
}

# ----------------------------------------------------------------------
# 2. Quản lý vòng đời ứng dụng (Lifespan Context Manager)
# ----------------------------------------------------------------------
models_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Chạy khi bắt đầu khởi động Server
    print("--- Khởi động Server: Đang nạp các mô hình AI lên bộ nhớ RAM ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    
    # Đọc preprocessor
    with open(os.path.join(models_dir, "preprocessor.pkl"), "rb") as f:
        models_state["preprocessor"] = pickle.load(f)
        
    # Đọc Top 3 mô hình thành phần
    with open(os.path.join(models_dir, "model_catboost.pkl"), "rb") as f:
        models_state["model_catboost"] = pickle.load(f)
    with open(os.path.join(models_dir, "model_random_forest.pkl"), "rb") as f:
        models_state["model_random_forest"] = pickle.load(f)
    with open(os.path.join(models_dir, "model_xgboost.pkl"), "rb") as f:
        models_state["model_xgboost"] = pickle.load(f)
        
    # Đọc cấu hình trọng số Ensemble
    with open(os.path.join(models_dir, "ensemble_config.pkl"), "rb") as f:
        models_state["ensemble_config"] = pickle.load(f)
        
    # Khởi tạo bộ giải thích SHAP TreeExplainer trên mô hình tốt nhất (CatBoost)
    # TreeExplainer chạy cực nhanh (mili-giây) trên mô hình dạng cây
    models_state["shap_explainer"] = shap.TreeExplainer(models_state["model_catboost"])
    
    print("--- Đã nạp thành công toàn bộ mô hình và bộ giải thích SHAP ---")
    yield
    # Chạy khi tắt Server
    models_state.clear()
    print("--- Đã giải phóng toàn bộ mô hình khỏi bộ nhớ RAM ---")

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Student Early Warning AI API",
    description="API dự báo nguy cơ học tập yếu và bỏ học của sinh viên",
    version="1.0.0",
    lifespan=lifespan
)

# Cấu hình CORS để kết nối với Laravel / Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# 3. Các hàm bổ trợ xử lý dữ liệu (Helpers)
# ----------------------------------------------------------------------
def process_single_student(student: StudentInput) -> tuple:
    # Trích xuất dữ liệu AI và ánh xạ sang tên cột gốc
    student_dict = student.model_dump()
    ai_features = {}
    for camel_key, raw_key in FIELD_MAPPING.items():
        ai_features[raw_key] = student_dict[camel_key]
        
    # Tạo DataFrame để xử lý
    df = pd.DataFrame([ai_features])
    
    # Thực hiện Kỹ nghệ đặc trưng (Feature Engineering) giống lúc train
    df['Sem1_Approved_Ratio'] = np.where(
        df['Curricular units 1st sem (enrolled)'] > 0,
        df['Curricular units 1st sem (approved)'] / df['Curricular units 1st sem (enrolled)'],
        0.0
    )
    df['Sem2_Approved_Ratio'] = np.where(
        df['Curricular units 2nd sem (enrolled)'] > 0,
        df['Curricular units 2nd sem (approved)'] / df['Curricular units 2nd sem (enrolled)'],
        0.0
    )
    df['Evaluation_Rate_Sem1'] = np.where(
        df['Curricular units 1st sem (enrolled)'] > 0,
        df['Curricular units 1st sem (evaluations)'] / df['Curricular units 1st sem (enrolled)'],
        0.0
    )
    df['Grade_Trend'] = df['Curricular units 2nd sem (grade)'] - df['Curricular units 1st sem (grade)']
    df['Financial_Risk'] = ((df['Debtor'] == 1) | (df['Tuition fees up to date'] == 0)).astype(int)
    df['Parental_Education_Score'] = df["Mother's qualification"] + df["Father's qualification"]
    
    # Biến đổi dữ liệu thông qua preprocessor đã lưu
    preprocessor = models_state["preprocessor"]
    X_processed = preprocessor.transform(df)
    
    # Lấy danh sách tên đặc trưng sau khi xử lý (để gán vào SHAP)
    feature_names = preprocessor.get_feature_names_out()
    
    return X_processed, feature_names

def run_predictions(X_processed, feature_names) -> dict:
    # Gọi dự đoán từ Top 3 mô hình
    model_cat = models_state["model_catboost"]
    model_rf = models_state["model_random_forest"]
    model_xgb = models_state["model_xgboost"]
    config = models_state["ensemble_config"]
    
    # Tính xác suất của lớp Dropout (lớp 1)
    p_cat = model_cat.predict_proba(X_processed)[0, 1]
    p_rf = model_rf.predict_proba(X_processed)[0, 1]
    p_xgb = model_xgb.predict_proba(X_processed)[0, 1]
    
    # Soft Voting theo trọng số F1-Score
    w_cat = config["weights"]["CatBoost"]
    w_rf = config["weights"]["Random Forest"]
    w_xgb = config["weights"]["XGBoost"]
    w_sum = w_cat + w_rf + w_xgb
    
    prob_dropout = (w_cat * p_cat + w_rf * p_rf + w_xgb * p_xgb) / w_sum
    
    # Phân loại kết quả và tính mức độ rủi ro (Risk Level)
    if prob_dropout > 0.70:
        prediction = "Dropout"
        risk_level = "High"
        confidence = prob_dropout
    elif prob_dropout >= 0.30:
        prediction = "Enrolled"
        risk_level = "Medium"
        confidence = prob_dropout if prob_dropout > 0.5 else (1.0 - prob_dropout)
    else:
        prediction = "Graduate"
        risk_level = "Low"
        confidence = 1.0 - prob_dropout
        
    # Lấy các gợi ý can thiệp từ DB
    recommendations = RECOMMENDATIONS_DB[prediction]
    
    # ------------------------------------------------------------------
    # Tính toán SHAP value để giải thích nguyên nhân bằng mô hình CatBoost
    # ------------------------------------------------------------------
    explainer = models_state["shap_explainer"]
    shap_vals = explainer.shap_values(X_processed)
    
    # Xử lý an toàn định dạng đầu ra của SHAP
    if isinstance(shap_vals, list):
        shap_scores = shap_vals[1][0] # Class 1 (Dropout)
    else:
        shap_scores = shap_vals[0] # Class 1 (Dropout)
        
    # Tạo danh sách các thuộc tính ảnh hưởng
    shap_list = []
    for idx, f_name in enumerate(feature_names):
        # Làm sạch tên cột hiển thị cho UI
        clean_name = f_name.replace("num__", "").replace("cat__", "").replace("remainder__", "")
        # Phân loại tác động
        impact = float(shap_scores[idx])
        if abs(impact) > 0.001: # Bỏ qua các tác động quá nhỏ
            shap_list.append({
                "feature": clean_name,
                "impact": impact,
                "type": "positive" if impact > 0 else "negative"
            })
            
    # Sắp xếp theo giá trị tuyệt đối tác động giảm dần và lấy Top 8 tác động mạnh nhất
    shap_list = sorted(shap_list, key=lambda x: abs(x["impact"]), reverse=True)[:8]
    
    return {
        "prediction": prediction,
        "probability": float(prob_dropout),
        "riskLevel": risk_level,
        "confidence": float(confidence),
        "recommendations": recommendations,
        "shapValues": shap_list
    }

# ----------------------------------------------------------------------
# 4. Thiết lập Endpoint API
# ----------------------------------------------------------------------
@app.get("/health", summary="Kiểm tra trạng thái hoạt động của Server")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": list(models_state.keys())
    }

@app.post("/predict/single", response_model=StudentPredictionResponse, summary="Dự đoán rủi ro cho một sinh viên đơn lẻ")
def predict_single(student: StudentInput):
    try:
        # Tiền xử lý dữ liệu đầu vào
        X_processed, feature_names = process_single_student(student)
        
        # Dự đoán kết quả
        res = run_predictions(X_processed, feature_names)
        
        # Trả về kết quả hoàn chỉnh
        return StudentPredictionResponse(
            id=f"RES-{int(np.datetime64('now').astype(int))}",
            studentCode=student.studentCode,
            studentName=student.studentName,
            className=student.className,
            faculty=student.faculty,
            **res
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

@app.post("/predict/batch", response_model=List[StudentPredictionResponse], summary="Dự đoán rủi ro cho nhiều sinh viên (Batch)")
def predict_batch(students: List[StudentInput]):
    try:
        results = []
        for idx, student in enumerate(students):
            X_processed, feature_names = process_single_student(student)
            res = run_predictions(X_processed, feature_names)
            results.append(StudentPredictionResponse(
                id=f"RES-{int(np.datetime64('now').astype(int))}-{idx}",
                studentCode=student.studentCode,
                studentName=student.studentName,
                className=student.className,
                faculty=student.faculty,
                **res
            ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống khi dự báo hàng loạt: {str(e)}")

# ----------------------------------------------------------------------
# 5. Lệnh chạy thử nghiệm
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # Khởi chạy server uvicorn ở cổng 8080 để tránh trùng với cổng 8000 của Laravel
    uvicorn.run(app, host="127.0.0.1", port=8080)
