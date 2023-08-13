import os
import re
import PyPDF2
import openpyxl

def extract_roe_values_from_pdf(pdf_file):
    roe_values = []
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            roe_matches = re.findall(r"加权平均净资产收益率\s*([\d.]+)", text)
            roe_values.extend(roe_matches)
    return roe_values

def extract_roe_values_from_txt(txt_file):
    roe_values = []
    with open(txt_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "加权平均净资产收益率" in line.decode("utf-8"):
                roe_match = re.search(r"加权平均净资产收益率\s*([\d.]+)", line.decode("utf-8"))
                if roe_match:
                    roe_values.append(roe_match.group(1))
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
            roe_values = extract_roe_values_from_pdf(pdf_file)
        elif filename.endswith(".txt"):
            txt_file = os.path.join(directory_path, filename)
            roe_values = extract_roe_values_from_txt(txt_file)
        else:
            continue
        
        print(f"Extracted ROE values from {filename}: {roe_values}")
        for value in roe_values:
            ws.append([filename, value])

    wb.save(output_file)
    print(f"Excel file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()
