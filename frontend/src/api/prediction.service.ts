import type { StudentPredictionInput, StudentDisplayInfo, StudentAIFeatures } from '../types/student';
import type { PredictionResult, StudentPredictionResult } from '../types/prediction';
import recommendationsDb from '../mocks/recommendations.json';

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const predictionService = {
  /**
   * Simulates an API call to predict early warning status for a single student.
   * Separates display fields from AI feature fields, simulates network latency, and returns the result.
   */
  async predictSingle(input: StudentPredictionInput): Promise<StudentPredictionResult> {
    // 1. Separate UI-only Display Fields from AI features
    const displayInfo: StudentDisplayInfo = {
      studentCode: input.studentCode,
      studentName: input.studentName,
      className: input.className,
      faculty: input.faculty
    };

    // AI model would only receive this payload in production
    const aiFeatures: StudentAIFeatures = {
      maritalStatus: input.maritalStatus,
      applicationMode: input.applicationMode,
      applicationOrder: input.applicationOrder,
      course: input.course,
      daytimeEvening: input.daytimeEvening,
      previousQualification: input.previousQualification,
      previousQualificationGrade: input.previousQualificationGrade,
      admissionGrade: input.admissionGrade,
      displaced: input.displaced,
      educationalSpecialNeeds: input.educationalSpecialNeeds,
      debtor: input.debtor,
      tuitionFeesUpToDate: input.tuitionFeesUpToDate,
      gender: input.gender,
      scholarshipHolder: input.scholarshipHolder,
      ageAtEnrollment: input.ageAtEnrollment,
      international: input.international,
      nationality: input.nationality,
      motherQualification: input.motherQualification,
      fatherQualification: input.fatherQualification,
      motherOccupation: input.motherOccupation,
      fatherOccupation: input.fatherOccupation,
      sem1Credited: input.sem1Credited,
      sem1Enrolled: input.sem1Enrolled,
      sem1Evaluations: input.sem1Evaluations,
      sem1Approved: input.sem1Approved,
      sem1Grade: input.sem1Grade,
      sem1WithoutEvaluations: input.sem1WithoutEvaluations,
      sem2Credited: input.sem2Credited,
      sem2Enrolled: input.sem2Enrolled,
      sem2Evaluations: input.sem2Evaluations,
      sem2Approved: input.sem2Approved,
      sem2Grade: input.sem2Grade,
      sem2WithoutEvaluations: input.sem2WithoutEvaluations,
      unemploymentRate: input.unemploymentRate,
      inflationRate: input.inflationRate,
      gdp: input.gdp
    };

    console.log('API Request - AI Feature Payload Sent to Backend:', aiFeatures);

    // 2. Simulate network latency (600ms)
    await delay(600);

    // 3. Generate prediction outcomes deterministically or randomly (no hardcoded rules)
    const outcomes: ('Graduate' | 'Dropout' | 'Enrolled')[] = ['Graduate', 'Dropout', 'Enrolled'];
    
    // Simple deterministic distribution based on student name hash to make it look stable, 
    // or fallback to random if name is empty
    const hash = displayInfo.studentName 
      ? displayInfo.studentName.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      : Math.floor(Math.random() * 100);

    const outcomeIndex = hash % 3;
    const prediction = outcomes[outcomeIndex] || 'Graduate';

    let probability = 0.5;
    let riskLevel: 'Low' | 'Medium' | 'High' = 'Medium';
    let confidence = 0.85;

    if (prediction === 'Graduate') {
      probability = 0.75 + (hash % 20) / 100; // 0.75 to 0.95
      riskLevel = 'Low';
      confidence = 0.88 + (hash % 10) / 100;  // 0.88 to 0.97
    } else if (prediction === 'Dropout') {
      probability = 0.70 + (hash % 25) / 100; // 0.70 to 0.94
      riskLevel = 'High';
      confidence = 0.80 + (hash % 15) / 100;  // 0.80 to 0.94
    } else {
      probability = 0.35 + (hash % 30) / 100; // 0.35 to 0.65
      riskLevel = 'Medium';
      confidence = 0.60 + (hash % 20) / 100;  // 0.60 to 0.80
    }

    // 4. Query recommendations from recommendations.json mock database
    const recommendations = recommendationsDb[prediction] || [];

    // 5. Package results with display information and return
    const id = `RES-${Date.now()}`;
    const date = new Date().toISOString();

    const result: StudentPredictionResult = {
      id,
      date,
      ...displayInfo,
      prediction,
      probability,
      confidence,
      riskLevel,
      recommendations
    };

    return result;
  },

  /**
   * Simulates an API call to predict status for a batch of students.
   */
  async predictBatch(inputs: StudentPredictionInput[]): Promise<StudentPredictionResult[]> {
    await delay(1200); // Higher delay for batch processing
    
    // Predict each student using the single prediction logic
    const results = await Promise.all(
      inputs.map(async (input, index) => {
        const res = await this.predictSingle(input);
        // Ensure unique IDs
        res.id = `RES-${Date.now()}-${index}`;
        return res;
      })
    );

    return results;
  }
};
