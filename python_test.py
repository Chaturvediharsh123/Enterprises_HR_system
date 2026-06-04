from pypdf import PdfReader

reader = PdfReader("documents/HR_Policy.pdf")

print("Pages:", len(reader.pages))

for page in reader.pages:
    print(page.extract_text())