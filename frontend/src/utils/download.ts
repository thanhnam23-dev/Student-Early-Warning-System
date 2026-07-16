/**
 * Helper to download raw text or CSV content as a file in the browser.
 */
export const downloadRawFile = (content: string, fileName: string, contentType = 'text/csv;charset=utf-8;') => {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', fileName);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};
