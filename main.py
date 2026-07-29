from Controllers.UserController import *
from Controllers.ApplicationController import *
user = UserController()
apl = ApplicationController()

def login():
    print("В первое поле введите логин")
    print("Во второе поле введите пароль")
    log = input("Первое поле")
    if log == 'exit':
        return
    elif log == '1':
        pass
    else:
        password = input("Введите свой пароль")
        if user.login(log, password):
            print("-----------------")
            page(log)
        else:
            print("-------------------------------")
            print("Вы ввели неверный логин или пароль")
            print("-------------------------------")
            print("Для выхода в первое поле введите - exit")
            print("-------------------------------")
            print("Для регистрации в системе НарушенийНет введите в первое поле - 1")
            print("-------------------------------")
            login()

def login_admin():
    print("В первое поле введите логин")
    print("Во второе поле введите пароль")
    log = input("Первое поле")
    if log == 'exit':
        return
    elif log == '2':
        pass
    else:
        password = input("Введите свой пароль")
        if user.login_adm(log, password):
            print("-----------------")
            print("Вы", log, "вошли в панель администратора")
            print("-----------------")
            print("ID | Имя подавшего | Описание заявления | Номер автомобиля | Статус заявления")
            for row in apl.show():
                print(row.id, row.user_id.fullname, row.discription, row.number_auto, row.status)
            print("-----------------")
        else:
            print("-------------------------------")
            print("Вы ввели неверный логин или пароль")
            print("-------------------------------")
            print("Для выхода в первое поле введите - exit")
            print("-------------------------------")
            print("Для регистрации в системе НарушенийНет введите в первое поле - 1")
            print("-------------------------------")
            login_admin()

# переход в кабинет пользователя
def page(user_login): # функция страница пользователя параметром является данные о пользователе
    stop_page = True
    while stop_page:


        print("Приветствую тебя пользователь", user_login)
        id_user = user.get_id_user(user_login)
        application = apl.show_one(id_user) # список словарей заявлений одного пользователя
        print("Описание заявления | Статус заявления | Номер автомобиля")
        for row in application:
            if row.status:
                stat = 'Подтверждено'
            else:
                stat = 'Отклонено'

            print(f"{row.discription} | {stat} | {row.number_auto}")

        print("----------------------------")
        print("Для добавления заявления Введите цифру - 2")
        command_page = input()
        if command_page == 'exit':
            stop_page = False
        elif command_page == '2':
            add_aplication(user_login)

def registration():
    print("В первое поле введите логин")
    print("Во второе поле введите пароль")
    print("В третье поле введите имя")
    print("В четвёртое поле введите email")
    print("В пятое поле введите телефон")
    log = input("Первое поле")
    if log == 'exit':
        return
    elif log == '0':
        pass
    else:
        password = input("Введите свой пароль")
        fullname = input("Введите своё имя")
        email = input("Введите свой email")
        phone = input("Введите свой телефон")
        user.registration(log, password, fullname, email, phone)
        print("-------------------------------")
        print('Вы', log, 'успешно зарегистрировались')
        print("-------------------------------")
        return


# Функция добавить заявление
def add_aplication(user_login):
    input_discription = input("Введите описание нарушения")
    input_number_auto = input("Введите номер автомобтля нарушителя")
    user_id = user.get_id_user(user_login)
    apl.create(input_discription, 0, input_number_auto, user_id)

def run():
    print("Информационная система НарушенийНет")
    stop = False
    while stop == False:
        print("Информационная система НарушенийНет")
        print("Для выхода из системы НарушенийНет введите в первое поле - exit")
        print("Для регистрации в системе НарушенийНет введите в первое поле - 0")
        print("Для авторизации в системе НарушенийНет введите в первое поле - 1")
        print("Для авторизации администратора в системе НарушенийНет введите в первое поле - 2")
        command = input()
        if command == 'exit':
            break
        if command == '0':
            registration()
        if command == '1':
            login()
        if command == '2':
            login_admin()


if __name__ == "__main__":
    run()