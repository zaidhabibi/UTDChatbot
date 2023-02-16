import requests
from bs4 import BeautifulSoup

url = "https://enroll.utdallas.edu/apply/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

text = soup.get_text()
text = " ".join(text.strip().split())

with open("utdallas_apply.txt", "w", encoding="utf-8") as file:
    file.write(text)