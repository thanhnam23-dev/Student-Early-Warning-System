export interface StudentDisplayInfo {
  studentCode: string;
  studentName: string;
  className: string;
  faculty: string;
}

export interface StudentAIFeatures {
  maritalStatus: number;
  applicationMode: number;
  applicationOrder: number;
  course: number;
  daytimeEvening: number;
  previousQualification: number;
  previousQualificationGrade: number;
  admissionGrade: number;
  displaced: number;
  educationalSpecialNeeds: number;
  debtor: number;
  tuitionFeesUpToDate: number;
  gender: number;
  scholarshipHolder: number;
  ageAtEnrollment: number;
  international: number;
  nationality: number;
  motherQualification: number;
  fatherQualification: number;
  motherOccupation: number;
  fatherOccupation: number;
  
  // Academic performance Semester 1
  sem1Credited: number;
  sem1Enrolled: number;
  sem1Evaluations: number;
  sem1Approved: number;
  sem1Grade: number;
  sem1WithoutEvaluations: number;

  // Academic performance Semester 2
  sem2Credited: number;
  sem2Enrolled: number;
  sem2Evaluations: number;
  sem2Approved: number;
  sem2Grade: number;
  sem2WithoutEvaluations: number;

  // Economic indicators
  unemploymentRate: number;
  inflationRate: number;
  gdp: number;
}

export type StudentPredictionInput = StudentDisplayInfo & StudentAIFeatures;
