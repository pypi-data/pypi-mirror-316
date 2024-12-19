import requests

def scan(domain, wordlist_path, timeout=3):
    found_subdomains = []
    with open(wordlist_path, 'r') as file:
        subdomains = file.read().splitlines()

    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                found_subdomains.append(url)
        except requests.RequestException:
            pass

    return found_subdomains
