from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
import urllib.request
import os

def SetFolderPath(key_search):
    key_search_process = unidecode(key_search.lower().replace(' ', '_'))
    current_path = os.path.abspath(os.getcwd())
    return os.path.join(current_path,'Dataset', key_search_process)

def CreateFolder(key_search):
    create_path = SetFolderPath(key_search)
    try:
        os.mkdir(create_path)
    except:
        print('Folder can not create!')
    
def ConverBase64toImage(path_save, base64_code, index):
    fileName = path_save + '/' + str(index) +'.jpg'
    URLImage = base64_code
    urllib.request.urlretrieve(URLImage, fileName)
    img = Image.open(fileName)

def CrawImageData(key_search, max_image):
    chorme_option = Options()
    chorme_option.add_argument('headless')
    chorme_option.add_argument('incognito')

    prefs = {'profile.managed_default_content_settings.images': 2}
    chorme_option.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(
        chrome_options=chorme_option,
        executable_path='chromedriver.exe'
    )
    
    google_image_url = 'https://images.google.com/'
    browser.implicitly_wait(30)
    browser.get(google_image_url)

    input_keyword = browser.find_element(By.NAME, 'q')
    input_keyword.send_keys(key_search)
    input_keyword.send_keys(Keys.ENTER)
    
    img_count = 0
    while img_count < max_image:
        browser.implicitly_wait(30)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        encode_image_urls = browser.find_elements(By.CSS_SELECTOR, 'div[class="bRMDJf islir"]')
        
        for i in encode_image_urls:
            try:
                image_encode = i.find_element(By.TAG_NAME, 'img').get_attribute('src')
                ConverBase64toImage(SetFolderPath(key_search), image_encode, img_count)
                img_count += 1
            except:
                print('No save image!')
        
    browser.quit()

if __name__ == '__main__':
    key_search = [
        'fresh banana',
        'fresh apple',
        'fresh mango',
        'fresh dragonfruit',
        'fresh orange',
        'fresh pear',
        'fresh guava',
        'fresh peach',
        'fresh avocado',
        'fresh tomato'
    ]
    
    for i in key_search:
        CreateFolder(i)
        CrawImageData(i, 1000)
    
    