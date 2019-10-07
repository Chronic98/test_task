# тут используется хром драйвер 78, и так как у меня не очень хороший интернет используются такие тайминги что бы вдруг
# исключения не вылетали, с более быстрым интернетом тайминги можно уменьшить.
# нужно установить pip install selenium

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import locale


path_chromedriver = os.path.abspath(os.curdir)
path_chromedriver += '\chromedriver.exe'

chrome_opt = Options()
chrome_opt.add_argument("--mute-audio")
# chrome_opt.add_argument("--headless")
driver = webdriver.Chrome(executable_path=path_chromedriver, chrome_options=chrome_opt)
driver.maximize_window()


list_task = []
# этот словарь я решил использовать для правильной замены, так как некоторые месяцы не правильно сокращены
dictionary_replacements_m = {'янв': '01',
                             'февр': '02',
                             'мар': '03',
                             'апр': '04',
                             'мая': '05',
                             'июн': '06',
                             'июл': '07',
                             'авг': '08',
                             'сент': '09',
                             'окт': '10',
                             'нояб': '11',
                             'дек': '12',
                             }

driver.get('https://www.youtube.com/')

search = driver.find_element_by_id("search")
time.sleep(5)
search.send_keys("python + javascript\n")


def function_task():
    # ii для правильного соотношения названия к ссылке
    ii = 0
    # n кол. эл. в финальном листе
    n = 0
    for i in range(15):
        time.sleep(2)
        # для открытия большого количества видео
        driver.find_element_by_id("continuations").click()
    # все названия видео которые доступны
    name = driver.find_elements_by_id('title-wrapper')
    # все ссылки на доступные видео
    elems = driver.find_elements_by_xpath("//a[@id='video-title']")
    time_period = driver.find_elements_by_xpath("//div[@id='metadata-line']//span[2]")

    for name_v in name:

        driver.switch_to.window(driver.window_handles[0])
        name_video = name_v.text
        # iii для правильного соотношения названия к ссылке
        iii = 0
        iiii = 0
        # проверка есть ли в названии нужные слова
        if name_video.lower().find('python') != -1 or name_video.lower().find('javascript') != -1 \
                and name_video.lower().find('basics') == -1:
            for tp in time_period:
                iiii += 1
                if ii == iiii:
                    if not (tp.text.find('год') != -1 or tp.text.find('года') != -1 or tp.text.find('месяцев') != -1
                            or tp.text.find('лет') != -1):
                        print("--------------------------------------------------------")
                        print(tp.text)
                        print(name_video)
                        for o in elems:
                            iii += 1
                            if ii == iii:
                                print(o.get_attribute("href"))
                                # ссылки нужны для открытия нужного видео в новой вкладке для того, что бы взять дату
                                driver.execute_script("window.open('" + o.get_attribute('href') + "', 'new_window')")
                                driver.switch_to.window(driver.window_handles[1])
                                time.sleep(5)
                                name_vi = driver.find_element_by_xpath("//div[@id='container']//h1").text
                                # нвзвание ролика
                                name_vid = name_vi.split('\n')[0]
                                # дата публикации ролика
                                time_date = driver.find_element_by_id("date").text
                                locale.setlocale(locale.LC_ALL, "")
                                # привожу дату к нужному виду
                                if time_date.find('•Прямой эфир: ') != -1:
                                    d = time_date.split(":")[1]
                                    dd = d.replace(".", "")
                                    ddd = dd[1:-2]
                                else:
                                    dd = time_date.replace(".", "")
                                    ddd = dd[1:-2]

                                for i, values in dictionary_replacements_m.items():
                                    list_date = ddd.split(" ")
                                    if list_date[1] == i:
                                        data = list_date[0] + "-" + values + "-" + list_date[2]

                                time_conditions = "04-08-2019"
                                # привожу дату к типу datetime для сравнения
                                date_publication = datetime.date(datetime.strptime(data, "%d-%m-%Y"))
                                time_condition = datetime.date(datetime.strptime(time_conditions, "%d-%m-%Y"))

                                if date_publication > time_condition:
                                    d = {"name video": name_vid, "date": str(date_publication)}
                                    list_task.append(d)
                                    n += 1

                                if n == 15:
                                    # сортировка даты
                                    list_task.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
                                    li = []
                                    for i in list_task:
                                        # значение ключа name video
                                        name_video_add_list = i.get("name video")
                                        # значение ключа date
                                        date_publication_add_list = i.get("date")
                                        # добавление в конечный список название видео - дата
                                        li.append(name_video_add_list + " - " + date_publication_add_list)
                                    return print('\n' + '\n' + 'RESULT:' + '\n' + '\n' + str(li))
        ii += 1


function_task()
driver.close()
driver.quit()


#  Примерный результат работы:
# [
# 'У нас есть python, django, vue.js и еще много интересного� - 2019-08-07',
# 'Why Python is beating Javascript in Google Trends - 2019-08-12',
# 'Делаем сайт, чат и игру на python 3, django и vue.js � - 2019-08-12',
# 'Делаем сайт, чат и игру на python 3, django и vue.js � - 2019-08-13',
# 'Делаем онлайн игру на python 3 и javaScript. Создание движка murr - 2019-08-19',
# "Python vs JavaScript | An Innovative Perspective based o# n a company's database | - 2019-08-19",
# 'Программирование на python 3 и javaScript. Меняем HTML/CSS движка murr - 2019-08-25',
# 'Программирование на python 3 и javaScript. Меняем HTML/CSS движка murr - 2019-08-26',
# 'The BEST Programming Languages For FREELANCING In 2020 � (Js, Machine Learning, PYTHON?) - 2019-09-04',
# '5 Ways to Know if you Have a Good Project | Javascript Python Ruby Java C# - 2019-09-04',
# 'Программирование на python и javascript! - 2019-09-05',
# 'JavaScript and Python Code in the Database with GraalVM and Multilingual Engine - 2019-09-18',
# 'JavaScript Object Notation (JSON) | Python for Beginners [38 of 44] - 2019-09-19',
# 'Какой язык программирования учить в России (JAVA, C#, Python, JavaScript, ABAP, PHP) - 2019-09-29',
# 'У нас есть python 3, javaScript и еще много интересного // HTML программист 2.0 // Как сделать сайт - 2019-10-02'
# ]

