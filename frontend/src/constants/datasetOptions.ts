export interface OptionItem {
  label: string;
  value: number;
}

export const MARITAL_STATUS_OPTIONS: OptionItem[] = [
  { label: 'Single', value: 1 },
  { label: 'Married', value: 2 },
  { label: 'Widower', value: 3 },
  { label: 'Divorced', value: 4 },
  { label: 'Facto Union', value: 5 },
  { label: 'Legally Separated', value: 6 }
];

export const GENDER_OPTIONS: OptionItem[] = [
  { label: 'Female', value: 0 },
  { label: 'Male', value: 1 }
];

export const DAYTIME_EVENING_OPTIONS: OptionItem[] = [
  { label: 'Evening', value: 0 },
  { label: 'Daytime', value: 1 }
];

export const YES_NO_OPTIONS: OptionItem[] = [
  { label: 'No', value: 0 },
  { label: 'Yes', value: 1 }
];

export const COURSE_OPTIONS: OptionItem[] = [
  { label: 'Biofuel Production Technologies', value: 33 },
  { label: 'Animation and Multimedia Design', value: 171 },
  { label: 'Social Service (Evening Attendance)', value: 8014 },
  { label: 'Agronomy', value: 9003 },
  { label: 'Communication Design', value: 9070 },
  { label: 'Veterinary Nursing', value: 9085 },
  { label: 'Informatics Engineering', value: 9119 },
  { label: 'Equiniculture', value: 9130 },
  { label: 'Management', value: 9147 },
  { label: 'Social Service', value: 9238 },
  { label: 'Tourism', value: 9254 },
  { label: 'Nursing', value: 9500 },
  { label: 'Oral Hygiene', value: 9556 },
  { label: 'Advertising and Marketing Management', value: 9670 },
  { label: 'Journalism and Communication', value: 9773 },
  { label: 'Basic Education', value: 9853 },
  { label: 'Management (Evening Attendance)', value: 9991 }
];

export const APPLICATION_MODE_OPTIONS: OptionItem[] = [
  { label: '1st phase - general contingent', value: 1 },
  { label: 'Ordinance No. 854-B/99', value: 2 },
  { label: '1st phase - special contingent (Azores Island)', value: 5 },
  { label: 'Holders of other higher courses', value: 7 },
  { label: 'Ordinances No. 533-A/99, item b2 (Different Plan)', value: 10 },
  { label: 'Ordinances No. 533-A/99, item b3 (Other Institution)', value: 15 },
  { label: 'Over 23 years old', value: 17 },
  { label: 'Transfer', value: 18 },
  { label: 'Change of course', value: 26 },
  { label: 'Technological specialization diploma holders', value: 27 },
  { label: 'Over 23 years old (International)', value: 39 },
  { label: 'Change of institution/course (International)', value: 43 }
];

export const QUALIFICATION_OPTIONS: OptionItem[] = [
  { label: 'Secondary Education - 12th Year of Schooling or Eq.', value: 1 },
  { label: 'Higher Education - Bachelor\'s Degree', value: 2 },
  { label: 'Higher Education - Degree', value: 3 },
  { label: 'Higher Education - Master\'s', value: 4 },
  { label: 'Higher Education - Doctorate', value: 5 },
  { label: 'Frequency of Higher Education', value: 6 },
  { label: '12th Year of Schooling - Not Completed', value: 9 },
  { label: '11th Year of Schooling - Not Completed', value: 10 },
  { label: '7th Year (Old)', value: 11 },
  { label: 'Other - 11th Year of Schooling', value: 12 },
  { label: '10th Year of Schooling', value: 14 },
  { label: 'General commerce course', value: 18 },
  { label: 'Basic education 3rd cycle (9th/10th/11th year) or equiv.', value: 19 },
  { label: 'Basic education 1st cycle (4th/5th year) or equiv.', value: 37 },
  { label: 'Basic education 2nd cycle (6th/7th/8th year) or equiv.', value: 38 },
  { label: 'Technological course', value: 39 },
  { label: 'Specialized higher education course', value: 41 }
];

export const OCCUPATION_OPTIONS: OptionItem[] = [
  { label: 'Student', value: 1 },
  { label: 'Representatives of the Legislative Power and Executive Bodies', value: 2 },
  { label: 'Directors of Administrative and Commercial Services', value: 3 },
  { label: 'Directors of Production and Specialized Services', value: 4 },
  { label: 'Directors of Hospitality, Catering, Trade and Other Services', value: 5 },
  { label: 'Specialists in Intellectual and Scientific Careers', value: 6 },
  { label: 'Intermediate Level Technicians and Professions', value: 7 },
  { label: 'Administrative Personnel', value: 8 },
  { label: 'Personal Service, Security and Safety Workers, and Sellers', value: 9 },
  { label: 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry', value: 10 },
  { label: 'Skilled Construction Workers (excl. electricity)', value: 20 },
  { label: 'Skilled Workers in Metallurgy, Metalworking and Machinery', value: 21 },
  { label: 'Handcraft, printing, precision instrument makers, jewellers, etc.', value: 22 },
  { label: 'Workers in Electricity and Electronics', value: 23 },
  { label: 'Food Processing, Woodworking, Garment and Other Industries', value: 24 },
  { label: 'Fixed Plant and Machine Operators, Assembly Workers', value: 25 },
  { label: 'Assembly Workers', value: 26 },
  { label: 'Unskilled Workers', value: 27 },
  { label: 'Armed Forces', value: 90 },
  { label: 'Other / Unknown', value: 99 }
];
