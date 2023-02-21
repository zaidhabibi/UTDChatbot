import os
import requests
from bs4 import BeautifulSoup

website_urls = {
    "apply": "https://enroll.utdallas.edu/apply/",
    "apply-other": "https://enroll.utdallas.edu/apply/#other",
    "graduate": "https://graduate-admissions.utdallas.edu/",
    "transfer_criteria": "https://enroll.utdallas.edu/transfer/criteria/",
    "transfer_app_proc": "https://enroll.utdallas.edu/transfer/application-process/",
    "status": "https://www.utdallas.edu/status/",
    "transfer_steps_after": "https://enroll.utdallas.edu/transfer/steps-after-admission/",
    "freshman_criteria": "https://enroll.utdallas.edu/freshman/criteria/",
    "fresh_app_proc": "https://enroll.utdallas.edu/freshman/application-process/",
    "fresh_step_after": "https://enroll.utdallas.edu/freshman/steps-after-admission/",
    "costs_schol_aid": "https://www.utdallas.edu/costs-scholarships-aid/",
    "orientation": "https://transition.utdallas.edu/orientations/",
    "housing": "https://housing.utdallas.edu/",
    "international_app": "https://enroll.utdallas.edu/apply/international-applicants/",
    "timeline": "https://enroll.utdallas.edu/transfer/timeline/",
    "veterans": "https://veterans.utdallas.edu/attend-ut-dallas/",
    "counselors": "https://enroll.utdallas.edu/contact/counselor-locator/",
    "vaccines": "https://registrar.utdallas.edu/legislative-policies/vaccine/",
    "tsi": "https://oue.utdallas.edu/undergraduate-advising/the-texas-success-initiative/",
    "aleks": "https://oue.utdallas.edu/aleks-exam",
    "catalog": "https://catalog.utdallas.edu/",
    "official_docs": "https://enroll.utdallas.edu/apply/submitting-official-documents-2/",
    "parking": "https://services.utdallas.edu/transit/",
    "fresh_schol": "https://enroll.utdallas.edu/affordability/freshman-scholarships/",
    "transfer_schol": "https://enroll.utdallas.edu/affordability/transfer-scholarships/",
    "schol_list": "https://www.utdallas.edu/costs-scholarships-aid/scholarships/listings/",
    "cost_calc": "https://www.utdallas.edu/costs-scholarships-aid/costs/calculator/",
    "fresh_orient": "https://fye.utdallas.edu/orientation/",
    "transfer_services": "https://transferservices.utdallas.edu/orientation/",
    "international_student_org": "https://icp.utdallas.edu/students/international-student-orientation/",
    "off-campus_housing": "https://www.dallasoffcampus.com/",
}

if not os.path.exists("website data"):
    os.mkdir("website data")

for key, url in website_urls.items():
    file_path = os.path.join("website data", key + ".txt")
    if os.path.exists(file_path):
        print(f"{key}.txt already exists. Skipping...")
    else:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.get_text()

        with open(file_path, "w", encoding="utf-8") as file:
            for line in text.split("\n"):
                line = " ".join(line.strip().split())
                if line:
                    file.write(line + "\n")
            print(f"{key}.txt saved.")