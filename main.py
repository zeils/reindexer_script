from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import re
import consts
import requests




def Get_data():
    print("Скачивание файла")
    #Выбор директории для скачивания файла
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.getcwd()}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('headless')
    #Запуск драйвера
    driver = webdriver.Chrome(options=chrome_options)

    
    #На всякий чистим куки
    driver.delete_all_cookies()

    graylog_filter_url= 'http://grlog-prod.esphere.local/search?rangetype=relative&fields=message%2Csource&width=1366&highlightMessage=&relative=86400&q=%22document%20missing%22%20AND%20facility%3Acourier.search.indexer%20'
    driver.get(graylog_filter_url)
    #ждем пока прогрузится страница авторизации грейлога
    time.sleep(consts.waiting_time)

    #ввода логина/пароля
    username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys(consts.username_graylog)
    password_field = driver.find_element(By.ID, 'password') 
    password_field.send_keys(consts.password_graylog)
    password_field.send_keys(Keys.RETURN)

    
    #ждем пока загрузится выборка грейлога
    time.sleep(consts.waiting_time)

    #Нажатие кнопочек для скачивания
    #input('экспорт?')
    moreactions_button = driver.find_element(By.ID, 'search-more-actions-dropdown').click()
    export_div = driver.find_element(By.XPATH, '//*[@id="sidebar"]/div/div[2]/div[1]/div/div[3]/div/ul/li[1]').click()
    download_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[2]/p[2]/a').click()

    #Ждем пока скачается файл
    time.sleep(consts.waiting_time)
    driver.quit()

def Use_reg():
    print("Использование регулярок")
    # Путь к файлу CSV
    csv_file_path = 'graylog-search-result-relative-86400.csv'  # Укажите свой путь

    # Путь для сохранения файла TXT
    txt_file_path = 'done.txt'  # Укажите свой путь

    # Открываем исходный файл CSV для чтения
    with open(csv_file_path, 'r') as csv_file:
        # Читаем строки из файла CSV
        csv_lines = csv_file.readlines()

    # Обработка каждой строки CSV с использованием регулярных выражений
    processed_lines = []
    for line in csv_lines:
        # Пример применения регулярного выражения (удаление чисел)
        processed_line = re.sub(r'^(.*)\[document\]\[', '', line)
        processed_line = re.sub(r'^(.*)\[document_lite\]\[', '', processed_line)
        processed_line = re.sub(r']: document missing"', '', processed_line)
        processed_line = re.sub(r'_In', '', processed_line)
        processed_line = re.sub(r'_Out', '', processed_line)
        processed_line = re.sub(r'"timestamp","source","message"', '', processed_line)
        processed_lines.append(processed_line)


    # Записываем обработанные строки в файл TXT
    processed_lines.pop(0)
    result_lines = list(set(processed_lines))    
    with open(txt_file_path, 'w') as txt_file:
        txt_file.writelines(result_lines)

    os.remove('graylog-search-result-relative-86400.csv')
    print("Вывод done файла")

def Get_courier_cookie():
    print('Получение кук для реиндексации')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    courier_url= 'https://courier.esphere.ru/auth/UI/Login?realm=lkk_sfera&goto=https%3A%2F%2Fcourier.esphere.ru%3A443%2F'
    driver.get(courier_url)
    time.sleep(consts.waiting_time)
    

    username_field = driver.find_element(By.ID, 'IDToken1')
    username_field.send_keys(consts.username_courier)

    password_field = driver.find_element(By.ID, 'IDToken2') 
    password_field.send_keys(consts.password_courier)

    submit_button = driver.find_element(By.NAME, 'Login.Submit').click()
    time.sleep(consts.waiting_time) 

    cookie = driver.get_cookies()
    #print(cookie)
    
    eSphereAuth = ''
    clinetID = ''
    
    for element in cookie:
        if element['name'] == 'eSphereAuth': eSphereAuth = element['value']
        if element['name'] == 'clientId': clinetID = element['value']


    driver.quit()
    return eSphereAuth, clinetID 
    
def Reindexer():
    eSphereAuth, clinetID = Get_courier_cookie()

    done_file = open("done.txt", "r")
    while True:

        doc = done_file.readline().strip()

        if not doc:
            break
        
        url = f'https://courier.esphere.ru/webapi/monitoring/{doc}/reindex'
        response = requests.post(url, headers={"Content-Length": "0"}, cookies = {"eSphereAuth": eSphereAuth, "clientid": clinetID})
        print (f'{doc} - {response}')



Get_data()
Use_reg()
Reindexer()
















