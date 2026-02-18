import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode

url = input("Enter URL: ").strip()

r = requests.get(url, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

for form in soup.find_all("form"):
    action = form.get("action")
    full_action = urljoin(url, action)

    data = {}
    for inp in form.find_all("input"):
        name = inp.get("name")
        value = inp.get("value", "")
        if name:
            data[name] = value

    query = urlencode(data)
    full_url = f"{full_action}?{query}"

    print("\n==============================")
    print("Action:", full_action)
    print("Parameters:", data)
    print("Full URL:", full_url)
    print("==============================\n")
