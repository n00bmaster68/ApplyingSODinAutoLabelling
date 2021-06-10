import os
import time
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
# url = 'https://www.google.com/search?q=cat&sxsrf=ALeKk02bB3G_AaIHhkJoKDIQRIAOcKeIDg:1622983651870&source=lnms&tbm=isch&sa=X&ved=2ahUKEwikx66ghYPxAhUPQd4KHfvaBRgQ_AUoAXoECAIQAw'

def get_html_source_by_selenium(url):
    driver_chrome = webdriver.Chrome("chromedriver.exe")
    driver_chrome.get(url)
    i = 0
    while i < 10:
        driver_chrome.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        driver_chrome.execute_script('var btn = document.getElementsByClassName("mye4qd");if (btn.length == 1);btn[0].click()')
        time.sleep(2)
        i += 1
    return driver_chrome.page_source

def download_image(folder_name, url):
    page = get_html_source_by_selenium(url)
    soup = BeautifulSoup(page, 'html.parser')

    img_tags = soup.find_all("img", class_="rg_i")

    imagelinks = []
    for img_tag in img_tags:
        try:
            imagelinks.append(img_tag['src'])
        except:
            imagelinks.append(img_tag['data-src'])
    print(f"Found {len(imagelinks)} images")

    try:
        os.mkdir('result/{}'.format(folder_name))
        path = './' + folder_name + '/'
        count = 0
        for imagelink in imagelinks:
            try:
                urllib.request.urlretrieve(imagelink, path + str(count) + ".jpg")
                count += 1
                print("Image no." + str(count) + " downloaded successfully",end='\r')
            except Exception:
                pass
            if count == 1000:
              break
    except Exception:
        print("This object's images have already been collected.")
    print("Done.")
