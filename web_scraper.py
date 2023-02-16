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
    "timeline": "https://enroll.utdallas.edu/transfer/timeline/"
}

for key, url in website_urls.items():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    text = soup.get_text()
    text = " ".join(text.strip().split())

    with open(key + ".txt", "w", encoding="utf-8") as file:
        file.write(text)
