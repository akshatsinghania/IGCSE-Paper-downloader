from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import os
import random
import concurrent.futures
print("Example url format: https://papers.xtremepape.rs/CAIE/IGCSE/Mathematics%20-%20Additional%20(0606)/")
print("Enter url: ")
url = input()
print("""Example path format:"/Users/akshat/Documents/past-paper-downloader/extreme-add""")
print("Enter path: ")
pathnam = input()

# If there is no such folder, the script will create one automatically

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
files = []
for link in soup.select("a[href$='.pdf']"):
    # Name the pdf files using the last portion of each link which are unique in this case
    link_str = str(link)
    if (link_str.find('qp') == -1):
        continue
    filename = os.path.join(
        pathnam, link['href'].split('/')[-1])

    path = Path(filename)

    if (path.is_file()):
        ff = open(filename, "rb")
        if not (ff.read() == b''):
            continue

    files.append(
        {"filename": filename,
         "link": f"{url}/{link['href']}"})

    # print('doing', files[-1])


def download_files(fss):
    print(f"Downloading {len(fss)} files")
    for filename in fss:
        with open(filename["filename"], 'wb') as f:
            f.write(requests.get(filename["link"]).content)


def download_file(file):
    with requests.get(file["link"], stream=True) as r:
        r.raise_for_status()
        with open(file["filename"], 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_file, files)
