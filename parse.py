from tkinter import *
import sys
import tkinter.ttk as ttk
import urllib.request
import xml.dom.minidom




'''Получение списка всех валют'''
def get_vals(date, region):
    print(date, region)
    response = urllib.request.urlopen(f"https://cbr.ru/scripts/XML_ostat.asp?date_req1={date}&date_req2={date}")
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    if region == "Russia":
        res = dom.getElementsByTagName("InRussia")
    elif region == "Moscow":
        res = dom.getElementsByTagName("InMoscow")
    result = res[0].childNodes[0].nodeValue
    return result


def convert_clicked():
    r = get_vals(count_input_txt.get(), combo1_txt.get(),)
    lbl_result["text"] = r

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
    tab_control.add(tab1, text="Окно")    # Добавляем вкладки в окно

    '''----------Виджеты------------'''
    global combo1_txt                                           # Получаем данные
    combo1_txt = StringVar()                                    # из выпадающего списка
    combo1 = ttk.Combobox(tab1, textvariable=combo1_txt)        # с перавой валютой
    combo1["values"] = ["Moscow", "Russia"]
    combo1.grid(column=0, row=0, pady=10, padx=10)

    global count_input_txt                                                             # Получаем количество
    count_input_txt = StringVar()                                                      # валюты и сохраняем в
    count_input = Entry(tab1, bd=2, relief=GROOVE, textvariable=count_input_txt)       # переменную count_input_txt
    count_input.grid(column=1, row=0, pady=25, padx=10)

    global lbl_result
    lbl_result = Label(tab1, bd=2, relief=GROOVE, width=17)                            # Создаем окно вывода
    lbl_result.grid(column=2, row=0, pady=25, padx=10)    

    convert_btn = Button(tab1, text="Пуск", command=convert_clicked)         # Создаем кнопку
    convert_btn.grid(column=3, row=0, pady=25, padx=10) 

    '''Запуск приложения'''
    tab_control.pack(expand=1, fill="both")
    window.bind('<Escape>', exit)               # Биндим esc на выход
    window.mainloop()                           # Запускаем основной
                                                # цикл приложения

if __name__ == "__main__":
    #print(get_vals("24/05/2022", "Moscow"))
    main()
