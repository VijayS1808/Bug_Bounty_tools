import sys

visited = set()
forms_found = []

def crawl(url):
    if url in visited:
        return
    visited.add(url)

    try:
        r = requests.get(url, timeout=10, verify=False)
    except:
        return

    soup = BeautifulSoup(r.text, "lxml")

    # ---- Extract forms ----
    for form in soup.find_all("form"):
        action = form.get("action")
        method = form.get("method", "GET").upper()

        action_url = urljoin(url, action)

        data = {}
        for inp in form.find_all("input"):
            name = inp.get("name")
            value = inp.get("value", "")
            if name:
                data[name] = value

        query = urlencode(data)
        full_url = action_url + ("?" + query if query else "")

        forms_found.append((method, action_url, data, full_url))

    # ---- Crawl links ----
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("/"):
            full = urljoin(url, href)
            if urlparse(full).netloc == urlparse(url).netloc:
                crawl(full)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 form_crawler.py https://target.com")
        sys.exit(1)

    crawl(sys.argv[1])

    with open("forms.txt", "w") as f1, open("full_urls.txt", "w") as f2:
        for m, a, d, fu in forms_found:
            f1.write(f"{m} | {a} | {d}\n")
            f2.write(fu + "\n")

    print(f"\n[+] Total Forms Found: {len(forms_found)}")
    print("[+] Saved: forms.txt")
    print("[+] Saved: full_urls.txt")
