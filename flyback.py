from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

'''
СУПЕРТ ТУПАЯ ПРОГА для регистрации на форуме flyback.org.ru
Да, решить просто, но на тот момент я не знал методов расчёта, но умел в Python.
Ниже решение за 1 минуту.
Для условия типа: Даны резисторыR1=40ом R2=310ом R3=300ом.
все элементы схемы идеальны, падение напряжение на диоде равно нулю
Входное напряжение: синусоидальное 50гц, с действующим значением 54В. 
Найти до какого значения зарядится конденсатор.
Решение: 54В * (R2 / (R1 + R2)) = 47.83
ДА, всё максимально просто. Хотите сложнее? Запустите скрипт)))
'''


start = time.time()

link = 'http://flyback.org.ru/user.php?mode=register&agreed=true'

# Мне было лень думать над первым селектором
selector_0 : str = 'body > table:nth-child(6) > tbody > tr > td > form > table.forumline > tbody > tr:nth-child(7) > td:nth-child(2)'
selector_1 : str = 'username'
selector_2 : str = 'email'
selector_3 : str = 'bday_day'
selector_4 : str = 'bday_month'
selector_5 : str = '6'
selector_6 : str = 'bday_year'
selector_7 : str = 'new_password'
selector_8 : str = 'password_confirm'
selector_9 : str = 'answer'
selector_10 : str = 'apply'
selector_11: str = 'submit'

text = {
'username': 'you_login',
'email': 'you_email',
'bday_day': '1',
'bday_year': '1970',
'new_password': 'strongPassword',
'password_confirm': 'strongPassword',
}

# если нужно найти вольтаж, то начните с близкого к этому значению, если энергию, то с 0.01
volt = 40.00

# Ну так калечно
run = True

try:
    # Это с отключённым графическим режимом
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    #стандартная инициализация
    browser = webdriver.Chrome(options=chrome_options)
    # Это для графичес кого режима
    # browser = webdriver.Chrome()
    browser.get(link)

    # тут получаю текст задания что бы было
    task = browser.find_element_by_css_selector(selector_0)
    print(task.text)

    # вставляю текст в форму
    username = browser.find_element_by_name(selector_1)
    username.send_keys(text['username'])

    # вставляю текст в форму
    email = browser.find_element_by_name(selector_2)
    email.send_keys(text['email'])

    # вставляю текст в форму
    bday_day = browser.find_element_by_name(selector_3)
    bday_day.clear()
    bday_day.send_keys(text['bday_day'])

    # выбираем месяц
    bday_day = Select(browser.find_element_by_name(selector_4))
    bday_day.select_by_value(selector_5)


    # вставляю текст в форму
    bday_year = browser.find_element_by_name(selector_6)
    bday_year.clear()
    bday_year.send_keys(text['bday_year'])



    # выбираю параметр
    apply = browser.find_element_by_name(selector_10)
    apply.click()

    while run:
        # вставляю текст в форму
        new_password = browser.find_element_by_name(selector_7)
        new_password.send_keys(text['new_password'])

        # вставляю текст в форму
        password_confirm = browser.find_element_by_name(selector_8)
        password_confirm.send_keys(text['password_confirm'])

        # вставляю текст в форму
        answer = browser.find_element_by_name(selector_9)
        answer.clear()

        # что бы адекватно округляло
        imp_answer = "{0:0.2f}".format(volt)
        answer.send_keys(imp_answer)


        # клик по кнопке
        button = browser.find_element_by_name(selector_11)
        button.click()

        try:
            findText = browser.find_element_by_tag_name('h1')
            if findText.text == 'Неверный ответ':
                volt += 0.01
                browser.back()
            else:
                print(volt, imp_answer)
                run = False
        except NoSuchElementException:
            print(volt, imp_answer)

except NoSuchElementException:
    print('Finish!')


finally:

    # А тут чисто что бы глянуть результат
    # получаем исходный код
    html = browser.page_source

    # Пишим в файл. Не надо? Закомитить
    with open('page.html', 'w') as file:
        file.write(html)


    # закрываем браузер после всех манипуляций
    browser.quit()

fin = time.time()
rez_time = fin - start

# Просто оценить потраченное время
print(f'Finish!\n It took:\n second: {rez_time}\n minutes: {rez_time/60}\n hour: {rez_time/3600}')