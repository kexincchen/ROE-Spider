import os
import re
import PyPDF2

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
    directory_path = "file"
    output_file = "output.txt"
    
    with open(output_file, "w") as output:
        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                pdf_file = os.path.join(directory_path, filename)
                roe_values = extract_roe_values(pdf_file)
                if roe_values:
                    output.write(f"ROE values from {filename}:\n")
                    for value in roe_values:
                        output.write(f"{value}\n")
                    output.write("\n")

if __name__ == "__main__":
    main()
