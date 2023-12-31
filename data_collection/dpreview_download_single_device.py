from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.request
from pathlib import Path
import time
import random

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-using")
    chrome_options.add_argument("start-maximized")

    return webdriver.Chrome(options=chrome_options, executable_path='/remote-home/xujunhao/noise_detect/data_collection/chromedriver-linux64/chromedriver')

def get_thumbnail_names(browser, url):
    """获得网页中所有缩略图的名字

    Args:
        browser (_type_): _description_
        url (_type_): _description_

    Returns:
        _type_: _description_
    """
    browser.get(url)
    grid_items = browser.find_elements(By.CSS_SELECTOR, 'div.gridItem')
    return [item.find_element(By.CSS_SELECTOR, 'img').get_attribute('src').split('/')[-1] for item in grid_items]

def random_user_agent():
    """随机一些agent, 防止被反爬

    Returns:
        _type_: _description_
    """
    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
    ]
    return random.choice(ua_list)

def download_images(browser, base_url, image_names, target_folder):
    """根据缩略图的名字推理对应原图所在的网站, 并去下载原图

    Args:
        browser (_type_): _description_
        base_url (_type_): _description_
        image_names (_type_): _description_
        target_folder (_type_): _description_
    """
    for image_name in image_names:
        image_name = image_name[:-4]
        start_t = time.time()
        web_url = f"{base_url}/{image_name}"
        browser.get(web_url)

        try:
            # 找到原图真实的url
            link_element = browser.find_element(By.CSS_SELECTOR, "td.content > a")

            img_url = link_element.get_attribute("href")

            image_path = Path(target_folder) / (image_name+".jpg")

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', random_user_agent())]
            urllib.request.install_opener(opener)

            urllib.request.urlretrieve(img_url, image_path)
            print(f"Downloaded {image_name} in {time.time() - start_t} seconds.")
        except Exception as e:
            print(f"Error downloading {image_name}: {e}")

def download_by_device(base_url):
    """通过给定的设备网页下载对应设备的图片"""
    browser = setup_browser()
    target_folder = '/remote-home/xujunhao/noise_detect/data_collection/temp'
    # 获取缩略图文件名
    image_names = get_thumbnail_names(browser, base_url)
    # 下载原图
    download_images(browser, base_url, image_names, target_folder)
    browser.quit()

def main():
    browser = setup_browser()
    base_url = 'https://www.dpreview.com/sample-galleries/7777453466/google-pixel-7a-sample-gallery'
    target_folder = '/remote-home/xujunhao/noise_detect/data_collection/temp'

    image_names = get_thumbnail_names(browser, base_url)
    download_images(browser, base_url, image_names, target_folder)
    browser.quit()

if __name__ == "__main__":
    print("进行测试")
    main()
