from tkinter import *
import sys
import datetime
import tkinter.ttk as ttk
import urllib.request
import xml.dom.minidom
import matplotlib
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


'''Приводит дату к нужному формату'''
def get_normal_date(now = datetime.datetime.now()):
    # Получаем день, месяц, год
    day = now.day
    month = now.month
    year = now.year

    # Проверка длины строки и добавление "0"
    if len(str(day)) != 2:
        day = "0" + str(day)
    if len(str(month)) != 2:
        month = "0" + str(month)

    # Возвращаем список
    return [day, month, year]

'''Возвращает курс в рублях по абривиатуре'''
def get_course(char_code, date=get_normal_date()):
    if (char_code == "Российский рубль"):
        return "1"
    # Делаем запрос по форматированной ссылке
    response = urllib.request.urlopen(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date[0]}/{date[1]}/{date[2]}")

    # Создаем объект парсера
    dom = xml.dom.minidom.parse(response)
    dom.normalize()

    # Собираем все ячейки с тегом "Valute" в список
    node_list = dom.getElementsByTagName("Valute")

    # Проходим циклом по списку и подэлементам списка
    for node in node_list:
        # Создаем список подэлементов и проходимся по нему циклом
        children = node.childNodes
        for i in range(len(children)):
            # Проверка тэга
            if children[i].nodeName == "Name":
                # Проверка названия валюты
                if children[i].childNodes[0].nodeValue == char_code:
                    # Возвращаем курс валюты в строковом формате
                    return children[i + 1].childNodes[0].nodeValue


def get_nominal(char_code, date=get_normal_date()):
    if (char_code == "Российский рубль"):
        return "1"
    # Делаем запрос по форматированной ссылке
    response = urllib.request.urlopen(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date[0]}/{date[1]}/{date[2]}")

    # Создаем объект парсера
    dom = xml.dom.minidom.parse(response)
    dom.normalize()

    # Собираем все ячейки с тегом "Valute" в список
    node_list = dom.getElementsByTagName("Valute")

    # Проходим циклом по списку и подэлементам списка
    for node in node_list:
        # Создаем список подэлементов и проходимся по нему циклом
        children = node.childNodes
        for i in range(len(children)):
            # Проверка тэга
            if children[i].nodeName == "Name":
                # Проверка названия валюты
                if children[i].childNodes[0].nodeValue == char_code:
                    # Возвращаем курс валюты в строковом формате
                    return children[i - 1].childNodes[0].nodeValue


'''Получение списка всех валют'''
def get_vals(date=get_normal_date()):
    response = urllib.request.urlopen(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date[0]}/{date[1]}/{date[2]}")
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    vals_list = []
    node_list = dom.getElementsByTagName("Valute")
    for node in node_list:
        children = node.childNodes
        for child in children:
            if child.nodeName == "Name":
                vals_list.append(child.childNodes[0].nodeValue)
                if "Польский" in child.childNodes[0].nodeValue:
                    vals_list.append("Российский рубль")
    return vals_list

'''Конвертирование валют'''
def convert_clicked():
    first_val = get_course(combo1_txt.get())
    second_val = get_course(combo2_txt.get())

    first_nom =  get_nominal(combo1_txt.get())
    second_nom = get_nominal(combo2_txt.get())

    first_val = first_val.replace(",", ".")
    second_val = second_val.replace(",", ".")

    count_txt = count_input_txt.get()

    res = (float(first_val) * float(count_txt) * float(second_nom)) / (float(second_val) * float(first_nom))
    lbl_result["text"] = res

'''Преобразование месяца'''
def month_to_str(arg):
    if arg <=0:
        arg += 12

    if arg == 1:
        return 'Декабрь'
    elif arg == 2:
        return 'Февраль'
    elif arg == 3:
        return 'Март'
    elif arg == 4:
        return 'Апрель'
    elif arg == 5:
        return 'Май'
    elif arg == 6:
        return 'Июнь'
    elif arg == 7:
        return 'Июль'
    elif arg == 8:
        return 'Август'
    elif arg == 9:
        return 'Сентябрь'
    elif arg == 10:
        return 'Октябрь'
    elif arg == 11:
        return 'Ноябрь'
    elif arg == 12:
        return 'Декабрь'

def str_to_month(arg):
    if arg == 'Январь':
        return "01"
    elif arg == 'Февраль':
        return "02"
    elif arg == 'Март':
        return '03'
    elif arg == 'Апрель':
        return '04'
    elif arg == 'Май':
        return '05'
    elif arg == 'Июнь':
        return '06'
    elif arg == 'Июль':
        return '07'
    elif arg == 'Август':
        return '08'
    elif arg == 'Сентябрь':
        return '09'
    elif arg == 'Октябрь':
        return '10'
    elif arg == 'Ноябрь':
        return '11'
    elif arg == 'Декабрь':
        return '12'

'''Преобразование квартала'''
def kv_to_str(arg):
    if arg <= 5 and arg >= 3:
        return "Весна"
    elif arg == 12 or arg == 1 or arg == 2:
        return "Зима"
    elif arg <= 11 and arg >= 9:
        return "Осень"
    elif arg <= 8 and arg >= 6:
        return "Лето"

'''Обратное преобразование квартала'''
def str_to_kv(arg):
    if arg == "Лето":
        return [6, 7, 8]
    elif arg == "Зима":
        return [12, 1, 2]
    elif arg == "Весна":
        return [3, 4, 5]
    elif arg == "Осень":
        return [9, 10, 11]

'''Задать период'''
def make_periods():
    res_list = []
    if bool_var.get() == 0:
        first_date = datetime.date.today()
        last_date = datetime.date.today() - relativedelta(weeks=1)
        for i in range(4):
            temp_fd = str(first_date).replace("-", ".")
            temp_ld = str(last_date).replace("-", ".")
            res_list.append(f"{temp_ld}-{temp_fd}")
            first_date = last_date
            last_date -= relativedelta(weeks=1)
    elif bool_var.get() == 1:
        date = datetime.date.today()
        for i in range(4):
            res_list.append(f"{month_to_str(date.month)} {date.year}")
            date -= relativedelta(months=1)
    elif bool_var.get() == 2:
        date = datetime.date.today()
        for i in range(4):
            res_list.append(f"{kv_to_str(date.month)} {date.year}")
            date -= relativedelta(months=3)
    elif bool_var.get() == 3:
        date = datetime.date.today()
        for i in range(4):
            res_list.append(f"{date.year} год")
            date -= relativedelta(years=1)
    combo4["values"] = res_list

'''Отрисовка графика'''
def do_plot():
    val = combo3_txt.get()
    data_x = []
    data_y = []
    if bool_var.get() == 0:
        first_day, last_day = combo4_txt.get().split("-")
        first_day = first_day.replace(".", "-")
        last_day = last_day.replace(".", "-")
        year, month, day = map(int, first_day.split("-"))
        first_day = datetime.date(year, month, day)
        year, month, day = map(int, last_day.split("-"))
        last_day = datetime.date(year, month, day)
        while first_day <= last_day:
            data_x.append(f"{first_day.day} {month_to_str(first_day.month)}")
            money = float(get_course(date=get_normal_date(first_day), char_code=val).replace(",", "."))
            data_y.append(money / float(get_nominal(val)))
            first_day += relativedelta(days=1)
    elif bool_var.get() == 1:
        day = 1
        month, year = combo4_txt.get().split(" ")
        month = str_to_month(month)
        first_day = datetime.date(int(year), int(month), day)
        MNTH = first_day.month
        while first_day.month == MNTH:
            data_x.append(f"{first_day.day} {month_to_str(first_day.month)}")
            money = float(get_course(date=get_normal_date(first_day), char_code=val).replace(",", "."))
            data_y.append(money / float(get_nominal(val)))
            first_day += relativedelta(days=3)
    elif bool_var.get() == 2:
        day = 1
        month, year = combo4_txt.get().split(" ")
        if month == "Зима" and year == "2022":
            year = 2021
        month = str_to_kv(month)
        last_month = month[2] + 1
        first_day = datetime.date(int(year), int(month[0]), day)
        while first_day.month != last_month:
            data_x.append(f"{first_day.day} {month_to_str(first_day.month)}")
            money = float(get_course(date=get_normal_date(first_day), char_code=val).replace(",", "."))
            data_y.append(money / float(get_nominal(val)))
            first_day += relativedelta(days=14)
    elif bool_var.get() == 3:
        year = int(combo4_txt.get().split(" ")[0])
        first_day = datetime.date(year, 1, 1)
        YR = first_day.year
        if first_day.year == datetime.date.today().year:
            while first_day <= datetime.date.today() - relativedelta(days=2):
                data_x.append(f"{first_day.day} {month_to_str(first_day.month)}")
                money = float(get_course(date=get_normal_date(first_day), char_code=val).replace(",", "."))
                data_y.append(money / float(get_nominal(val)))
                first_day += relativedelta(days=20)
        else:
            while first_day.year == YR:
                data_x.append(f"{first_day.day} {month_to_str(first_day.month)}")
                money = float(get_course(date=get_normal_date(first_day), char_code=val).replace(",", "."))
                data_y.append(money / float(get_nominal(val)))
                first_day += relativedelta(days=50)
    ax.clear()
    ax.plot(data_x, data_y)
    canvas.draw()

'''Завершение работы'''
def exit(event):
    sys.exit()


'''Основная функция'''
def main():
    '''----------Окно--------------'''
    window = Tk()                       # Создаем объект класса tkinter
    window.title("Конвертер валют")     # Задаем название окна
    window.geometry("700x200")          # Задаем разрешение окна

    '''---------Вкладки-------------'''
    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)                      # Создаем 1 вкладку
    global tab2                                        # Делаем 2 вкладку глобальной
    tab2 = ttk.Frame(tab_control)                      # Создаем 2 вкладку
    tab_control.add(tab1, text="Калькулятор валют")    # Добавляем вкладки в окно
    tab_control.add(tab2, text="Динамика курса")

    '''----------Виджеты------------'''
    global combo1_txt                                           # Получаем данные
    combo1_txt = StringVar()                                    # из выпадающего списка
    combo1 = ttk.Combobox(tab1, textvariable=combo1_txt)        # с перавой валютой
    combo1["values"] = get_vals()
    combo1.grid(column=0, row=0, pady=10, padx=10)

    global combo2_txt                                           # Получаем данные
    combo2_txt = StringVar()                                    # из выпадающего списка
    combo2 = ttk.Combobox(tab1, textvariable=combo2_txt)        # со 2 валютой
    combo2["values"] = get_vals()
    combo2.grid(column=0, row=1, pady=5, padx=10)

    global count_input_txt                                                             # Получаем количество
    count_input_txt = StringVar()                                                      # валюты и сохраняем в
    count_input = Entry(tab1, bd=2, relief=GROOVE, textvariable=count_input_txt)       # переменную count_input_txt
    count_input.grid(column=1, row=0, pady=25, padx=10)

    global lbl_result
    lbl_result = Label(tab1, bd=2, relief=GROOVE, width=17)                            # Создаем окно вывода
    lbl_result.grid(column=1, row=1, pady=25, padx=10)                                 # конвертации

    convert_btn = Button(tab1, text="Конвертировать", command=convert_clicked)         # Создаем кнопку
    convert_btn.grid(column=2, row=0, pady=25, padx=10)                                # конвертации

    '''2 вкладка'''
    lbl_val = Label(tab2, width=17, text="Валюта")                  # Создаем надпись валюта
    lbl_val.grid(column=0, row=0, pady=2, padx=10)

    global combo3_txt                                               # Создаем выпадающий
    combo3_txt = StringVar()                                        # список с выбором валют
    combo3 = ttk.Combobox(tab2, textvariable=combo3_txt)            # и сохраняем результат
    combo3["values"] = get_vals()                                   # выбора в переменную combo3_txt
    combo3.grid(column=0, row=1, pady=10, padx=10)

    lbl_period = Label(tab2, width=17, text="Период")               # Вывод текста "Период"
    lbl_period.grid(column=1, row=0, pady=2, padx=10)

    global bool_var     # Создаем радио кнопки с выбором периода
    bool_var = IntVar()
    bool_var.set(0)
    week_box = Radiobutton(tab2, text="Неделя", variable=bool_var, value=0, command=make_periods)
    week_box.grid(column=1, row=1, pady=0, padx=10)
    month_box = Radiobutton(tab2, text="Месяц",variable=bool_var, value=1, command=make_periods)
    month_box.grid(column=1, row=2, pady=0, padx=10)
    kvart_box = Radiobutton(tab2, text="Квартал",variable=bool_var, value=2, command=make_periods)
    kvart_box.grid(column=1, row=3, pady=0, padx=10)
    year_box = Radiobutton(tab2, text="Год",variable=bool_var, value=3, command=make_periods)
    year_box.grid(column=1, row=4, pady=0, padx=10)

    global combo4                                                       # Создаем выпадающий
    global combo4_txt                                                   # список с выбором
    combo4_txt = StringVar()                                            # периода и сохраняем
    combo4 = ttk.Combobox(tab2, textvariable=combo4_txt)                # результат выбора в
    combo4["values"] = make_periods()                                   # переменную combo4_txt
    combo4.grid(column=2, row=1, pady=2, padx=10)

    lbl_choose_period = Label(tab2, width=17, text="Выбор периода")     # Создаем надпись
    lbl_choose_period.grid(column=2, row=0, pady=2, padx=10)            # выбор периода

    global canvas                                                                   # Созаем виджет
    global ax                                                                       # на котором
    frame1 = Frame(tab2); frame1.place(x=500, y=10, width=1200, height=500)         # отображаем
    figure = plt.Figure(figsize=(5,5))                                              # график
    canvas = FigureCanvasTkAgg(figure, frame1)
    canvas.get_tk_widget().place(x=0,y=0,width=1100,height=400)
    ax = figure.add_subplot(111)

    # Создаем кнопку прорисовки графика
    build_btn = Button(tab2, text="Построить график", command= lambda: do_plot())
    build_btn.grid(column=0, row=3, pady=5, padx=10)


    '''Запуск приложения'''
    tab_control.pack(expand=1, fill="both")
    window.bind('<Escape>', exit)               # Биндим esc на выход
    window.mainloop()                           # Запускаем основной
                                                # цикл приложения

if __name__ == "__main__":
    main()
