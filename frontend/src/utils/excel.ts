import { read, utils, writeFile } from 'xlsx';

/**
 * Parses an Excel (.xlsx/.xls) file into a JSON array of objects.
 */
export const parseExcelFile = (file: File): Promise<any[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        // Read as array buffer to support multiple platforms safely
        const workbook = read(data, { type: 'array' });
        const firstSheetName = workbook.SheetNames[0];
        if (!firstSheetName) {
          throw new Error('Workbook contains no sheets.');
        }
        const worksheet = workbook.Sheets[firstSheetName];
        if (!worksheet) {
          throw new Error('Worksheet not found in workbook.');
        }
        const jsonData = utils.sheet_to_json(worksheet, { defval: null });
        resolve(jsonData);
      } catch (error) {
        reject(error);
      }
    };
    reader.onerror = (error) => reject(error);
    reader.readAsArrayBuffer(file);
  });
};

/**
 * Exports data objects to an Excel (.xlsx) file.
 */
export const exportToExcel = (data: any[], fileName: string, sheetName = 'Sheet1') => {
  const worksheet = utils.json_to_sheet(data);
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, sheetName);
  writeFile(workbook, `${fileName}.xlsx`);
};

/**
 * Generates and downloads a sample Excel template for batch predictions.
 */
export const downloadTemplateExcel = () => {
  const headers = [
    {
      'Student Code': '22010001',
      'Student Name': 'Nguyen Van A',
      'Class': 'IT-01',
      'Faculty': 'Information Technology',
      'Marital Status': 1,
      'Age at Enrollment': 20,
      'Gender': 1,
      'Nationality': 1,
      'International': 0,
      'Application Mode': 1,
      'Application Order': 1,
      'Course': 9119,
      'Daytime/Evening Attendance': 1,
      'Previous Qualification': 1,
      'Previous Qualification Grade': 120.5,
      'Admission Grade': 125.4,
      'Mother\'s Qualification': 1,
      'Father\'s Qualification': 1,
      'Mother\'s Occupation': 1,
      'Father\'s Occupation': 1,
      'Scholarship Holder': 1,
      'Debtor': 0,
      'Tuition Fees Up To Date': 1,
      'Displaced': 0,
      'Educational Special Needs': 0,
      'Sem1 Credited': 0,
      'Sem1 Enrolled': 6,
      'Sem1 Evaluations': 6,
      'Sem1 Approved': 6,
      'Sem1 Grade': 14.5,
      'Sem1 Without Evaluations': 0,
      'Sem2 Credited': 0,
      'Sem2 Enrolled': 6,
      'Sem2 Evaluations': 6,
      'Sem2 Approved': 5,
      'Sem2 Grade': 13.8,
      'Sem2 Without Evaluations': 0,
      'Unemployment Rate': 10.8,
      'Inflation Rate': 1.4,
      'GDP': 3.5
    },
    {
      'Student Code': '22010002',
      'Student Name': 'Tran Thi B',
      'Class': 'NUR-02',
      'Faculty': 'Nursing',
      'Marital Status': 1,
      'Age at Enrollment': 18,
      'Gender': 0,
      'Nationality': 1,
      'International': 0,
      'Application Mode': 1,
      'Application Order': 1,
      'Course': 9500,
      'Daytime/Evening Attendance': 1,
      'Previous Qualification': 1,
      'Previous Qualification Grade': 115.0,
      'Admission Grade': 118.2,
      'Mother\'s Qualification': 19,
      'Father\'s Qualification': 19,
      'Mother\'s Occupation': 9,
      'Father\'s Occupation': 9,
      'Scholarship Holder': 0,
      'Debtor': 1,
      'Tuition Fees Up To Date': 0,
      'Displaced': 1,
      'Educational Special Needs': 0,
      'Sem1 Credited': 0,
      'Sem1 Enrolled': 6,
      'Sem1 Evaluations': 8,
      'Sem1 Approved': 2,
      'Sem1 Grade': 10.2,
      'Sem1 Without Evaluations': 0,
      'Sem2 Credited': 0,
      'Sem2 Enrolled': 6,
      'Sem2 Evaluations': 8,
      'Sem2 Approved': 1,
      'Sem2 Grade': 8.5,
      'Sem2 Without Evaluations': 0,
      'Unemployment Rate': 12.4,
      'Inflation Rate': 2.8,
      'GDP': -1.2
    }
  ];

  const worksheet = utils.json_to_sheet(headers);
  const workbook = utils.book_new();
  utils.book_append_sheet(workbook, worksheet, 'Template');
  writeFile(workbook, 'student_prediction_template.xlsx');
};
