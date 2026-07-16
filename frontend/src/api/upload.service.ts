import { parseExcelFile, downloadTemplateExcel } from '../utils/excel';
import type { StudentPredictionInput } from '../types/student';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const uploadService = {
  /**
   * Simulates downloading the prediction excel template.
   */
  async downloadTemplate(): Promise<void> {
    await delay(300);
    downloadTemplateExcel();
  },

  /**
   * Parses the uploaded Excel file into raw JSON objects.
   * Maps Excel column headers to the keys expected by the StudentPredictionInput interface.
   * Later, this JSON payload will be sent directly to the backend endpoint.
   */
  async parseUpload(file: File): Promise<StudentPredictionInput[]> {
    await delay(800); // Simulate processing latency
    
    const rawRows = await parseExcelFile(file);
    console.log('API Request - Excel Sheet Cells Parsed:', rawRows);
    
    // Map human-readable Excel column headers to StudentPredictionInput properties
    const mappedStudents: StudentPredictionInput[] = rawRows.map((row) => {
      return {
        studentCode: String(row['Student Code'] || ''),
        studentName: String(row['Student Name'] || ''),
        className: String(row['Class'] || ''),
        faculty: String(row['Faculty'] || ''),
        maritalStatus: Number(row['Marital Status'] ?? 1),
        ageAtEnrollment: Number(row['Age at Enrollment'] ?? 18),
        gender: Number(row['Gender'] ?? 1),
        nationality: Number(row['Nationality'] ?? 1),
        international: Number(row['International'] ?? 0),
        applicationMode: Number(row['Application Mode'] ?? 1),
        applicationOrder: Number(row['Application Order'] ?? 1),
        course: Number(row['Course'] ?? 9119),
        daytimeEvening: Number(row['Daytime/Evening Attendance'] ?? 1),
        previousQualification: Number(row['Previous Qualification'] ?? 1),
        previousQualificationGrade: Number(row['Previous Qualification Grade'] ?? 100),
        admissionGrade: Number(row['Admission Grade'] ?? 100),
        motherQualification: Number(row['Mother\'s Qualification'] ?? 1),
        fatherQualification: Number(row['Father\'s Qualification'] ?? 1),
        motherOccupation: Number(row['Mother\'s Occupation'] ?? 1),
        fatherOccupation: Number(row['Father\'s Occupation'] ?? 1),
        scholarshipHolder: Number(row['Scholarship Holder'] ?? 0),
        debtor: Number(row['Debtor'] ?? 0),
        tuitionFeesUpToDate: Number(row['Tuition Fees Up To Date'] ?? 1),
        displaced: Number(row['Displaced'] ?? 0),
        educationalSpecialNeeds: Number(row['Educational Special Needs'] ?? 0),
        
        sem1Credited: Number(row['Sem1 Credited'] ?? 0),
        sem1Enrolled: Number(row['Sem1 Enrolled'] ?? 0),
        sem1Evaluations: Number(row['Sem1 Evaluations'] ?? 0),
        sem1Approved: Number(row['Sem1 Approved'] ?? 0),
        sem1Grade: Number(row['Sem1 Grade'] ?? 0),
        sem1WithoutEvaluations: Number(row['Sem1 Without Evaluations'] ?? 0),
        
        sem2Credited: Number(row['Sem2 Credited'] ?? 0),
        sem2Enrolled: Number(row['Sem2 Enrolled'] ?? 0),
        sem2Evaluations: Number(row['Sem2 Evaluations'] ?? 0),
        sem2Approved: Number(row['Sem2 Approved'] ?? 0),
        sem2Grade: Number(row['Sem2 Grade'] ?? 0),
        sem2WithoutEvaluations: Number(row['Sem2 Without Evaluations'] ?? 0),
        
        unemploymentRate: Number(row['Unemployment Rate'] ?? 0),
        inflationRate: Number(row['Inflation Rate'] ?? 0),
        gdp: Number(row['GDP'] ?? 0)
      };
    });

    return mappedStudents;
  }
};
