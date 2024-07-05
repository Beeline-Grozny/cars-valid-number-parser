import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_image(url, folder, headers, img_name):
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            filename = os.path.join(folder, img_name)
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Изображение {filename} успешно скачано.")
        else:
            print(f"Не удалось скачать изображение по URL: {url}, статус код: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения по URL: {url}, ошибка: {e}")


def parse_and_download_images(base_url, folder, page_num):
    if not os.path.exists(folder):
        os.makedirs(folder)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': base_url,
    }

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            panels = soup.find_all('div', class_='panel-body')
            counter = page_num * 100
            for panel in panels:
                rows = panel.find_all('div', class_='row')
                if len(rows) >= 2:
                    img1 = rows[0].find('img')
                    img2 = rows[1].find('img')

                    if img1 and img2:
                        img1_url = img1.get('src')
                        img2_url = img2.get('src')

                        if img1_url and img1_url.startswith('http'):
                            img1_filename = f"{str(counter + 1).zfill(2)}_photo.jpg"
                            img1_url = urljoin(base_url, img1_url)
                            download_image(img1_url, folder, headers, img1_filename)

                        if img2_url and img2_url.startswith('http'):
                            img2_filename = f"{str(counter + 1).zfill(2)}_number.jpg"
                            img2_url = urljoin(base_url, img2_url)
                            download_image(img2_url, folder, headers, img2_filename)

                        counter += 1
        else:
            print(f"Не удалось получить доступ к странице: {base_url}, статус код: {response.status_code}")
            return False
    except Exception as e:
        print(f"Ошибка при запросе к странице: {base_url}, ошибка: {e}")
        return False

    return True

base_url = 'https://platesmania.com/ru/gallery'
download_folder = 'downloaded_images'

page_num = 0
while True:
    if page_num == 0:
        url = base_url
    else:
        url = f"{base_url}-{page_num}"

    success = parse_and_download_images(url, download_folder, page_num)
    if not success:
        break

    page_num += 1