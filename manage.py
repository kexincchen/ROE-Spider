import os
import re
import PyPDF2
import openpyxl

def extract_roe_values(pdf_file):
    roe_values = []
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            roe_matches = re.findall(r"加权平均净资产收益率\s*([\d.]+)", text)
            roe_values.extend(roe_matches)
    return roe_values

def main():
    directory_path = "files"
    output_file = "output.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Filename", "ROE Value"])

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_file = os.path.join(directory_path, filename)
            roe_values = extract_roe_values(pdf_file)
            print(f"Extracted ROE values from {pdf_file}: {roe_values}")
            for value in roe_values:
                ws.append([filename, value])

    wb.save(output_file)
    print(f"Excel file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()
