import pdfplumber
import re
import requests

# === STEP 1: Extract text from PDF ===
with pdfplumber.open("Sample_Utility_Bill.pdf") as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

# === STEP 2: Define extractor with fallback ===
def extract(pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else "NOT FOUND"

# === STEP 3: Extract fields from the bill ===
data_fields = {
    "ACCOUNT": extract(r"ACCOUNT:\s+(.+)"),
    "SERVICE_ADDRESS": extract(r"SERVICE ADDRESS:\s+(.+)"),
    "SERVICE_PERIOD": extract(r"SERVICE PERIOD:\s+(.+)"),
    "BILLING_DATE": extract(r"BILLING DATE:\s+(.+)"),
    "DUE_DATE": extract(r"DUE DATE:\s+(.+)"),
    "SEWER_SERVICE": extract(r"SEWER SERVICE\s+(\d+\.\d{2})")
}

print("📄 Extracted Data:", data_fields)

# === STEP 4: Prepare Google Form submission ===
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeLACc0EgQqHklE1NZ7RBXRqe-9vmFzqqt6caQ4DW4jnSvnrg/formResponse"

form_fields = {
    "entry.3179660648": data_fields["ACCOUNT"],
    "entry.524503780": data_fields["SERVICE_ADDRESS"],
    "entry.539231965": data_fields["SERVICE_PERIOD"],
    "entry.134375432": data_fields["BILLING_DATE"],
    "entry.504876639": data_fields["DUE_DATE"],
    "entry.1373350962": data_fields["SEWER_SERVICE"]
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

# === STEP 5: Submit to Google Form ===
response = requests.post(form_url, data=form_fields, headers=headers)

# === STEP 6: Confirm result ===
if response.status_code == 200:
    print("✅ Form submitted successfully!")
else:
    print(f"❌ Submission failed with status code: {response.status_code}")
