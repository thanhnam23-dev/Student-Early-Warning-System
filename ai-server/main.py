import os
import json
import shutil
import pickle
import numpy as np
import pandas as pd
import shap
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

# ----------------------------------------------------------------------
# 1. Định nghĩa các Schema Pydantic cho Dữ liệu & Lịch sử
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

class StudentPredictionResult(BaseModel):
    id: str
    date: str
    studentCode: str
    studentName: str
    className: str
    faculty: str
    prediction: str
    probability: float
    confidence: float
    riskLevel: str
    recommendations: List[str]
    shapValues: Optional[List[Dict[str, Any]]] = None

class StudentPredictionResponse(BaseModel):
    id: str
    date: str
    studentCode: str
    studentName: str
    className: str
    faculty: str
    prediction: str
    probability: float
    riskLevel: str
    confidence: float
    recommendations: List[str]
    shapValues: Optional[List[Dict[str, Any]]] = None

class PredictionHistoryItem(BaseModel):
    id: str
    date: str
    type: str # 'single' hoặc 'batch'
    studentCount: int
    resultSummary: str
    details: List[StudentPredictionResult]

# Các schema phục vụ Dashboard
class DashboardStats(BaseModel):
    totalPredictions: int
    singlePredictions: int
    batchPredictions: int
    graduateCount: int
    dropoutCount: int
    enrolledCount: int

class DistributionItem(BaseModel):
    label: str
    value: int

class HistoryTimelineItem(BaseModel):
    label: str
    value: int

class ActivityTimelineEvent(BaseModel):
    id: str
    timestamp: str
    type: str
    message: str
    studentName: Optional[str] = None
    studentCode: Optional[str] = None
    prediction: Optional[str] = None
    riskLevel: Optional[str] = None

class DashboardDataResponse(BaseModel):
    stats: DashboardStats
    distribution: List[DistributionItem]
    history: List[HistoryTimelineItem]
    latestSingle: Optional[StudentPredictionResult] = None
    latestBatch: Optional[Dict[str, Any]] = None
    recentActivity: List[ActivityTimelineEvent]
    recentPredictions: List[StudentPredictionResult]

# ----------------------------------------------------------------------
# 2. Ánh xạ trường dữ liệu & Đề xuất can thiệp
# ----------------------------------------------------------------------
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

def generate_dynamic_recommendations(prediction: str, shap_list: List[Dict[str, Any]]) -> List[str]:
    # Lấy danh sách khuyến nghị cơ sở cho lớp dự đoán
    base_recs = RECOMMENDATIONS_DB.get(prediction, []).copy()
    
    # Nếu kết quả là Graduate (Tốt nghiệp - rủi ro thấp) thì không cần khuyến nghị cảnh báo
    if prediction == "Graduate":
        return base_recs
        
    # Lọc ra các yếu tố làm tăng nguy cơ bỏ học (positive impact trong SHAP)
    risk_factors = [item for item in shap_list if item["type"] == "positive"]
    
    # Kiểm tra xem có yếu tố rủi ro tài chính nào làm tăng nguy cơ không
    has_financial_risk = any(item["feature"] in ["Tuition fees up to date", "Debtor", "Financial_Risk"] and item["type"] == "positive" for item in shap_list)
    
    # Nếu sinh viên không có rủi ro tài chính (hoặc đóng học phí đầy đủ, biểu thị bằng SHAP âm)
    # Ta sẽ xóa các khuyến nghị liên quan đến học phí và nợ nần khỏi danh sách cơ sở
    if not has_financial_risk:
        base_recs = [rec for rec in base_recs if "tài chính" not in rec.lower() and "học phí" not in rec.lower()]
        
    if not risk_factors:
        return base_recs[:5]
        
    # Lấy yếu tố rủi ro hàng đầu (tác động lớn nhất)
    top_risk = risk_factors[0]
    top_feature = top_risk["feature"]
    
    dynamic_recs = []
    
    # Phân loại nguyên nhân dựa trên tên đặc trưng SHAP hàng đầu
    # 1. Rủi ro về Tài chính (Chưa đóng học phí hoặc nợ nần)
    if top_feature in ["Tuition fees up to date", "Debtor", "Financial_Risk"]:
        dynamic_recs.append("🔴 KHUYẾN NGHỊ KHẨN CẤP (TÀI CHÍNH): Mô hình phát hiện nguyên nhân rủi ro hàng đầu là do sinh viên chậm nộp học phí hoặc đang nợ học phí học tập. Đề xuất: Sinh viên cần liên hệ ngay với Phòng Kế hoạch Tài chính để làm thủ tục giãn nợ, trả góp học phí học tập, hoặc đăng ký nhận gói hỗ trợ tín dụng học tập khó khăn từ nhà trường.")
        
    # 2. Rủi ro về Học lực yếu (Tỷ lệ đỗ môn thấp hoặc trượt nhiều môn)
    elif "Approved" in top_feature or "Ratio" in top_feature or "Grade" in top_feature or "Without" in top_feature:
        dynamic_recs.append("🔴 KHUYẾN NGHỊ KHẨN CẤP (HỌC THUẬT): Mô hình phát hiện nguyên nhân rủi ro chính đến từ kết quả học tập yếu kém (tỷ lệ trượt môn cao hoặc điểm trung bình học kỳ thấp). Đề xuất: Sinh viên cần đặt lịch hẹn khẩn cấp với Cố vấn học tập để rà soát chương trình học, đăng ký tham gia lớp phụ đạo (Peer-tutoring) và xem xét giảm tải số lượng tín chỉ đăng ký kỳ sau để tránh áp lực học tập quá tải.")
        
    # 3. Điểm đầu vào thấp (Nền tảng học vấn yếu)
    elif "admissionGrade" in top_feature or "Previous qualification (grade)" in top_feature:
        dynamic_recs.append("🔴 KHUYẾN NGHỊ KHẨN CẤP (NỀN TẢNG): Điểm xét tuyển đại học hoặc điểm học lực cấp 3 của sinh viên thấp hơn mức trung bình của ngành học. Đề xuất: Cố vấn học tập cần định hướng sinh viên tham gia các lớp học bổ trợ kiến thức đại cương bắt buộc và kết nối đội nhóm bạn cùng tiến để nhanh chóng làm quen với phương pháp học đại học.")
        
    # 4. Mất học bổng
    elif top_feature == "Scholarship holder":
        dynamic_recs.append("🔴 KHUYẾN NGHỊ KHẨN CẤP (HỌC BỔNG): Sinh viên bị mất học bổng hoặc không duy trì được điều kiện nhận học bổng làm tăng áp lực kinh tế. Đề xuất: Sinh viên cần gặp phòng Công tác sinh viên để tìm kiếm các học bổng tài trợ xã hội khác hoặc đăng ký các công việc bán thời gian (part-time) trong khuôn viên trường.")
        
    # 5. Khó khăn hòa nhập (Sinh viên xa nhà)
    elif top_feature == "Displaced":
        dynamic_recs.append("🔴 KHUYẾN NGHỊ KHẨN CẤP (HÒA NHẬP): Sinh viên thuộc diện đi học xa nhà, đang gặp khó khăn về chỗ ở và tâm lý hòa nhập. Đề xuất: Sinh viên cần đăng ký ở Ký túc xá nhà trường để đảm bảo an ninh, đồng thời liên hệ Đoàn thanh niên/Hội sinh viên để tham gia các câu lạc bộ ngoại khóa hỗ trợ tinh thần.")

    # Điền thêm các khuyến nghị cơ sở để đảm bảo đủ 4-5 lời khuyên, tránh trùng lặp
    for rec in base_recs:
        if rec not in dynamic_recs and len(dynamic_recs) < 5:
            # Loại bỏ các khuyến nghị cơ sở có nội dung trùng lặp với khuyến nghị khẩn cấp
            if "tài chính" in rec.lower() and any("tài chính" in r.lower() for r in dynamic_recs):
                continue
            if "phụ đạo" in rec.lower() and any("học thuật" in r.lower() for r in dynamic_recs):
                continue
            dynamic_recs.append(rec)
            
    return dynamic_recs

# ----------------------------------------------------------------------
# 3. Quản lý vòng đời ứng dụng (Lifespan Context Manager)
# ----------------------------------------------------------------------
models_state = {}
history_file_path = ""

def init_history_file(base_dir):
    global history_file_path
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    history_file_path = os.path.join(data_dir, "prediction_history.json")
    
    # Nếu chưa có file lịch sử trong Python, sao chép file mock từ frontend
    if not os.path.exists(history_file_path):
        mock_path = os.path.abspath(os.path.join(base_dir, "..", "frontend", "src", "mocks", "prediction-history.json"))
        if os.path.exists(mock_path):
            try:
                shutil.copy(mock_path, history_file_path)
                print(f"Đã sao chép lịch sử mẫu từ frontend vào: {history_file_path}")
            except Exception as e:
                print(f"Lỗi sao chép tệp mẫu: {e}")
        else:
            with open(history_file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False)
            print("Đã tạo file lịch sử mới trống.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi động: Nạp các mô hình AI lên RAM
    print("--- Khởi động Server: Đang nạp các mô hình AI lên bộ nhớ RAM ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    
    init_history_file(base_dir)
    
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
        
    # Khởi tạo SHAP TreeExplainer
    models_state["shap_explainer"] = shap.TreeExplainer(models_state["model_catboost"])
    
    print("--- Đã nạp thành công toàn bộ mô hình và bộ giải thích SHAP ---")
    yield
    # Tắt server
    models_state.clear()
    print("--- Đã giải phóng toàn bộ mô hình khỏi bộ nhớ RAM ---")

# Khởi tạo FastAPI
app = FastAPI(
    title="Student Early Warning System Integrated Backend",
    description="Máy chủ API hợp nhất cho hệ thống cảnh báo sớm sinh viên học yếu/bỏ học",
    version="2.0.0",
    lifespan=lifespan
)

# Cấu hình CORS cho phép giao tiếp trực tiếp với Frontend Vue 3
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# 4. Các hàm bổ trợ xử lý dữ liệu (Helpers)
# ----------------------------------------------------------------------
def process_single_student(student: StudentInput) -> tuple:
    student_dict = student.model_dump()
    ai_features = {}
    for camel_key, raw_key in FIELD_MAPPING.items():
        ai_features[raw_key] = student_dict[camel_key]
        
    df = pd.DataFrame([ai_features])
    
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
    
    preprocessor = models_state["preprocessor"]
    X_processed = preprocessor.transform(df)
    feature_names = preprocessor.get_feature_names_out()
    
    return X_processed, feature_names

def run_predictions(X_processed, feature_names) -> dict:
    model_cat = models_state["model_catboost"]
    model_rf = models_state["model_random_forest"]
    model_xgb = models_state["model_xgboost"]
    config = models_state["ensemble_config"]
    
    p_cat = model_cat.predict_proba(X_processed)[0, 1]
    p_rf = model_rf.predict_proba(X_processed)[0, 1]
    p_xgb = model_xgb.predict_proba(X_processed)[0, 1]
    
    w_cat = config["weights"]["CatBoost"]
    w_rf = config["weights"]["Random Forest"]
    w_xgb = config["weights"]["XGBoost"]
    w_sum = w_cat + w_rf + w_xgb
    
    prob_dropout = (w_cat * p_cat + w_rf * p_rf + w_xgb * p_xgb) / w_sum
    
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
        
    # SHAP Explainability
    explainer = models_state["shap_explainer"]
    shap_vals = explainer.shap_values(X_processed)
    
    if isinstance(shap_vals, list):
        shap_scores = shap_vals[1][0]
    else:
        shap_scores = shap_vals[0]
        
    shap_list = []
    for idx, f_name in enumerate(feature_names):
        clean_name = f_name.replace("num__", "").replace("cat__", "").replace("remainder__", "")
        impact = float(shap_scores[idx])
        if abs(impact) > 0.001:
            shap_list.append({
                "feature": clean_name,
                "impact": impact,
                "type": "positive" if impact > 0 else "negative"
            })
            
    shap_list = sorted(shap_list, key=lambda x: abs(x["impact"]), reverse=True)[:8]
    
    # Sinh khuyến nghị động cá nhân hóa dựa trên nguyên nhân rủi ro hàng đầu từ SHAP
    recommendations = generate_dynamic_recommendations(prediction, shap_list)
    
    return {
        "prediction": prediction,
        "probability": float(prob_dropout),
        "riskLevel": risk_level,
        "confidence": float(confidence),
        "recommendations": recommendations,
        "shapValues": shap_list
    }

# Read / Write Lịch sử JSON
def load_history_data() -> List[Dict[str, Any]]:
    if not os.path.exists(history_file_path):
        return []
    try:
        with open(history_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history_data(data: List[Dict[str, Any]]):
    try:
        with open(history_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Lỗi khi lưu lịch sử: {e}")

# ----------------------------------------------------------------------
# 5. Các Endpoint API cho Tiền xử lý, Dự đoán, Lịch sử và Dashboard
# ----------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models_loaded": list(models_state.keys()),
        "history_file": history_file_path
    }

@app.post("/predict/single", response_model=StudentPredictionResponse)
def predict_single(student: StudentInput):
    try:
        X_processed, feature_names = process_single_student(student)
        res = run_predictions(X_processed, feature_names)
        current_date = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return StudentPredictionResponse(
            id=f"RES-{int(np.datetime64('now').astype(int))}",
            date=current_date,
            studentCode=student.studentCode,
            studentName=student.studentName,
            className=student.className,
            faculty=student.faculty,
            **res
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý dự đoán đơn: {str(e)}")

@app.post("/predict/batch", response_model=List[StudentPredictionResponse])
def predict_batch(students: List[StudentInput]):
    try:
        results = []
        current_date = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        for idx, student in enumerate(students):
            X_processed, feature_names = process_single_student(student)
            res = run_predictions(X_processed, feature_names)
            results.append(StudentPredictionResponse(
                id=f"RES-{int(np.datetime64('now').astype(int))}-{idx}",
                date=current_date,
                studentCode=student.studentCode,
                studentName=student.studentName,
                className=student.className,
                faculty=student.faculty,
                **res
            ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý dự đoán batch: {str(e)}")

# GET Lịch sử
@app.get("/history", response_model=List[PredictionHistoryItem])
def get_history():
    return load_history_data()

# POST Lịch sử (Để lưu phiên làm việc mới)
@app.post("/history", response_model=PredictionHistoryItem)
def save_prediction_session(session: PredictionHistoryItem):
    history_list = load_history_data()
    
    # Kiểm tra xem ID đã tồn tại chưa để cập nhật hoặc thêm mới
    session_dict = session.model_dump()
    
    # Tìm kiếm phần tử trùng lặp
    existing_index = next((i for i, item in enumerate(history_list) if item["id"] == session.id), None)
    if existing_index is not None:
        history_list[existing_index] = session_dict
    else:
        # Chèn lên đầu danh sách (Newest first)
        history_list.insert(0, session_dict)
        
    save_history_data(history_list)
    return session

# GET chi tiết 1 bản ghi của sinh viên trong lịch sử bằng ID kết quả
@app.get("/history/{result_id}", response_model=StudentPredictionResult)
def get_prediction_result_by_id(result_id: str):
    history_list = load_history_data()
    for session in history_list:
        for detail in session.get("details", []):
            if detail.get("id") == result_id:
                return detail
    raise HTTPException(status_code=404, detail="Không tìm thấy kết quả dự đoán với ID đã cho.")

# GET Thống kê Dashboard
@app.get("/dashboard/stats", response_model=DashboardDataResponse)
def get_dashboard_data():
    history_list = load_history_data()
    
    # Lấy các giá trị mặc định từ database
    total_preds = 0
    single_preds = 0
    batch_preds = 0
    grads = 0
    drops = 0
    enrolls = 0
    
    flat_history = []
    latest_batch_event = None
    latest_single_event = None
    
    # Sắp xếp lịch sử theo ngày giảm dần
    sorted_history = sorted(history_list, key=lambda x: x.get("date", ""), reverse=True)
    
    for item in sorted_history:
        details = item.get("details", [])
        student_count = item.get("studentCount", 0)
        s_type = item.get("type", "single")
        
        total_preds += student_count
        if s_type == "single":
            single_preds += student_count
            if len(details) > 0 and latest_single_event is None:
                latest_single_event = details[0]
        else:
            batch_preds += student_count
            if latest_batch_event is None:
                g_count = len([d for d in details if d.get("prediction") == "Graduate"])
                d_count = len([d for d in details if d.get("prediction") == "Dropout"])
                e_count = len([d for d in details if d.get("prediction") == "Enrolled"])
                latest_batch_event = {
                    "id": item.get("id"),
                    "date": item.get("date"),
                    "total": student_count,
                    "graduates": g_count,
                    "dropouts": d_count,
                    "enrolled": e_count,
                    "successRate": g_count / student_count if student_count > 0 else 0
                }
                
        for d in details:
            flat_history.append(d)
            pred = d.get("prediction")
            if pred == "Graduate":
                grads += 1
            elif pred == "Dropout":
                drops += 1
            else:
                enrolls += 1
                
    recent_predictions = flat_history[:5]
    
    # Phân bố (Distribution)
    distribution = [
        {"label": "Graduate", "value": grads},
        {"label": "Dropout", "value": drops},
        {"label": "Enrolled", "value": enrolls}
    ]
    
    # Dòng hoạt động gần đây (Timeline)
    recent_activity = []
    for idx, item in enumerate(sorted_history[:4]):
        timestamp = item.get("date", "")
        if item.get("type") == "single":
            student_name = ""
            student_code = ""
            prediction = "Graduate"
            risk_level = "Low"
            if len(item.get("details", [])) > 0:
                det = item["details"][0]
                student_name = det.get("studentName", "")
                student_code = det.get("studentCode", "")
                prediction = det.get("prediction", "Graduate")
                risk_level = det.get("riskLevel", "Low")
            
            message = f"Single prediction run completed for student {student_name}. Outcome: {prediction} ({risk_level} Risk)."
            recent_activity.append({
                "id": f"ACT-{item.get('id')}",
                "timestamp": timestamp,
                "type": "single",
                "message": message,
                "studentName": student_name,
                "studentCode": student_code,
                "prediction": prediction,
                "riskLevel": risk_level
            })
        else:
            recent_activity.append({
                "id": f"ACT-{item.get('id')}",
                "timestamp": timestamp,
                "type": "batch",
                "message": f"Batch prediction run completed for {item.get('studentCount')} students. Result breakdown: {item.get('resultSummary')}."
            })
            
    # Lịch sử theo dòng thời gian (mặc định giả lập 6 tháng gần nhất)
    # Lọc và đếm số lượng dự đoán của từng tháng từ lịch sử thực tế
    monthly_counts = {}
    for item in history_list:
        date_str = item.get("date", "")
        if len(date_str) >= 7: # YYYY-MM
            month_label = date_str[5:7] # Lấy số tháng MM
            # Chuyển MM thành Tên tháng rút gọn tiếng Anh
            month_map = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
            month_name = month_map.get(month_label, month_label)
            monthly_counts[month_name] = monthly_counts.get(month_name, 0) + item.get("studentCount", 0)
            
    # Sắp xếp hoặc bổ sung mặc định cho đủ biểu đồ nếu dữ liệu ít
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    timeline = []
    
    # Lấy 6 tháng có dữ liệu gần đây hoặc mặc định 6 tháng đầu năm
    for m in months:
        if m in monthly_counts or len(timeline) < 6:
            timeline.append({
                "label": m,
                "value": monthly_counts.get(m, 0 if m not in ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] else 15 + months.index(m) * 5)
            })
            
    timeline = timeline[-6:] # Giữ đúng 6 tháng
    
    return DashboardDataResponse(
        stats=DashboardStats(
            totalPredictions=total_preds,
            singlePredictions=single_preds,
            batchPredictions=batch_preds,
            graduateCount=grads,
            dropoutCount=drops,
            enrolledCount=enrolls
        ),
        distribution=distribution,
        history=timeline,
        latestSingle=latest_single_event,
        latestBatch=latest_batch_event,
        recentActivity=recent_activity,
        recentPredictions=recent_predictions
    )

# ----------------------------------------------------------------------
# 6. Khởi chạy máy chủ API
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # Khởi chạy cổng 8080 tích hợp đầy đủ backend và API
    uvicorn.run(app, host="127.0.0.1", port=8080)
