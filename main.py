from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import re
import consts




def Get_data():
    chrome_options = webdriver.ChromeOptions()

    prefs = {'download.default_directory' : os.getcwd()}
    
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=chrome_options)
    chrome_options = webdriver.ChromeOptions()
    
    driver.delete_all_cookies()
    graylog_filter_url= 'http://grlog-prod.esphere.local/search?rangetype=relative&fields=message%2Csource&width=1366&highlightMessage=&relative=86400&q=%22document%20missing%22%20AND%20facility%3Acourier.search.indexer%20'
    driver.get(graylog_filter_url)

    time.sleep(consts.waiting_time)
    #input('авторизация?')

    username_field = driver.find_element(By.ID, 'username')
    username_field.send_keys(consts.username)
    #input('ввод пароля?')
    password_field = driver.find_element(By.ID, 'password') 
    password_field.send_keys(consts.password)
    password_field.send_keys(Keys.RETURN)

    #input('экспорт?')
    time.sleep(consts.waiting_time)
    moreactions_button = driver.find_element(By.ID, 'search-more-actions-dropdown').click()
    export_div = driver.find_element(By.XPATH, '//*[@id="sidebar"]/div/div[2]/div[1]/div/div[3]/div/ul/li[1]').click()
    download_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[2]/p[2]/a').click()

    time.sleep(consts.waiting_time)
    driver.quit()

def Use_reg():
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
print("Скачивание файла")
Get_data()
print("Использование регулярок")
Use_reg()
print("Вывод done файла")











