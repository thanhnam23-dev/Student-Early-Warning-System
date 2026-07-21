import pandas as pd
import urllib.request
import json

def test_prediction():
    # 1. Đọc dữ liệu sinh viên mẫu từ tập Active Students
    df = pd.read_csv("data/active_students.csv")
    student_row = df.iloc[0].to_dict()

    # Ánh xạ từ cột CSV sang camelCase
    inv_mapping = {
        "Marital status": "maritalStatus",
        "Application mode": "applicationMode",
        "Application order": "applicationOrder",
        "Course": "course",
        "Daytime/evening attendance": "daytimeEvening",
        "Previous qualification": "previousQualification",
        "Previous qualification (grade)": "previousQualificationGrade",
        "Admission grade": "admissionGrade",
        "Displaced": "displaced",
        "Educational special needs": "educationalSpecialNeeds",
        "Debtor": "debtor",
        "Tuition fees up to date": "tuitionFeesUpToDate",
        "Gender": "gender",
        "Scholarship holder": "scholarshipHolder",
        "Age at enrollment": "ageAtEnrollment",
        "International": "international",
        "Nationality": "nationality",
        "Mother's qualification": "motherQualification",
        "Father's qualification": "fatherQualification",
        "Mother's occupation": "motherOccupation",
        "Father's occupation": "fatherOccupation",
        "Curricular units 1st sem (credited)": "sem1Credited",
        "Curricular units 1st sem (enrolled)": "sem1Enrolled",
        "Curricular units 1st sem (evaluations)": "sem1Evaluations",
        "Curricular units 1st sem (approved)": "sem1Approved",
        "Curricular units 1st sem (grade)": "sem1Grade",
        "Curricular units 1st sem (without evaluations)": "sem1WithoutEvaluations",
        "Curricular units 2nd sem (credited)": "sem2Credited",
        "Curricular units 2nd sem (enrolled)": "sem2Enrolled",
        "Curricular units 2nd sem (evaluations)": "sem2Evaluations",
        "Curricular units 2nd sem (approved)": "sem2Approved",
        "Curricular units 2nd sem (grade)": "sem2Grade",
        "Curricular units 2nd sem (without evaluations)": "sem2WithoutEvaluations",
        "Unemployment rate": "unemploymentRate",
        "Inflation rate": "inflationRate",
        "GDP": "gdp"
    }

    # Thiết lập payload JSON với các trường hiển thị mẫu
    payload = {
        "studentCode": "SV-2026-0001",
        "studentName": "Nguyễn Văn Anh",
        "className": "K68-CNTT",
        "faculty": "Công nghệ thông tin"
    }

    for k, v in inv_mapping.items():
        # Đưa dữ liệu thô vào payload camelCase
        val = student_row[k]
        if isinstance(val, (int, float)):
            payload[v] = val
        else:
            payload[v] = int(val)

    # 2. Gửi request POST đến API /predict/single
    req = urllib.request.Request("http://127.0.0.1:8080/predict/single")
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(payload).encode('utf-8')

    try:
        response = urllib.request.urlopen(req, jsondata)
        result = json.loads(response.read().decode())
        print("\n--- KẾT QUẢ DỰ ĐOÁN TỪ FASTAPI ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("---------------------------------")
    except Exception as e:
        print("Lỗi khi kết nối đến API:", e)

if __name__ == "__main__":
    test_prediction()
