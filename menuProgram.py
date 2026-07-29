import tkinter as tk
from tkinter import messagebox
import pymysql
from config import host, user, password, db_name


class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            port=3306,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.connection.close()

    def get_cursor(self):
        return self.connection.cursor()


class ApplicationManager:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.user_role = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        tk.Label(self.login_frame, text="Логин:").grid(row=0, column=0)
        tk.Label(self.login_frame, text="Пароль:").grid(row=1, column=0)

        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Авторизоваться", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.login_frame, text="Зарегистрироваться", command=self.create_register_screen).grid(row=3, column=0, columnspan=2)

    def create_register_screen(self):
        self.clear_screen()
        self.register_frame = tk.Frame(self.root)
        self.register_frame.pack(padx=20, pady=20)

        tk.Label(self.register_frame, text="Логин:").grid(row=0, column=0)
        tk.Label(self.register_frame, text="Пароль:").grid(row=1, column=0)
        tk.Label(self.register_frame, text="Имя:").grid(row=2, column=0)
        tk.Label(self.register_frame, text="Номер телефона:").grid(row=3, column=0)
        tk.Label(self.register_frame, text="Email:").grid(row=4, column=0)

        self.reg_login_entry = tk.Entry(self.register_frame)
        self.reg_login_entry.grid(row=0, column=1)
        self.reg_password_entry = tk.Entry(self.register_frame, show='*')
        self.reg_password_entry.grid(row=1, column=1)
        self.reg_full_name_entry = tk.Entry(self.register_frame)
        self.reg_full_name_entry.grid(row=2, column=1)
        self.reg_phone_number_entry = tk.Entry(self.register_frame)
        self.reg_phone_number_entry.grid(row=3, column=1)
        self.reg_email_entry = tk.Entry(self.register_frame)
        self.reg_email_entry.grid(row=4, column=1)

        tk.Button(self.register_frame, text="Регистрация", command=self.register).grid(row=5, column=0, columnspan=2)

    def create_main_screen(self):
        self.clear_screen()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        tk.Button(self.main_frame, text="Просмотр заявлений", command=self.view_applications).pack()
        tk.Button(self.main_frame, text="Добавить заявление", command=self.add_application).pack()
        if self.user_role == 1:  # Admin role
            tk.Button(self.main_frame, text="Изменить статусы", command=self.change_application_status).pack()
        tk.Button(self.main_frame, text="Выход", command=self.create_login_screen).pack()


    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        cursor = self.db.get_cursor()
        query = "SELECT * FROM users WHERE login = %s AND password = %s"
        cursor.execute(query, (login, password))
        user = cursor.fetchone()

        if user:
            self.user_role = user.get('role_id')
            self.create_main_screen()
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    def register(self):
        login = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        fullname = self.reg_full_name_entry.get()
        phone = self.reg_phone_number_entry.get()
        email = self.reg_email_entry.get()

        cursor = self.db.get_cursor()
        query = "SELECT * FROM users WHERE login = %s"
        cursor.execute(query, (login,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Ошибка", "Пользователь уже зарегистрирован")
        else:
            insert_query = "INSERT INTO users (login, password, fullname, phone, email, role_id) VALUES (%s, %s, %s, %s, %s, 1)"
            cursor.execute(insert_query, (login, password, fullname, phone, email))
            self.db.connection.commit()
            messagebox.showinfo("Успешно", "Регистрация прошла успешно")
            self.create_login_screen()

    def view_applications(self):
        self.clear_screen()
        self.applications_frame = tk.Frame(self.root)
        self.applications_frame.pack(padx=20, pady=20)

        cursor = self.db.get_cursor()
        query = "SELECT * FROM applications" if self.user_role == 2 else "SELECT * FROM applications WHERE user_id = %s"
        cursor.execute(query, (self.user_role,) if self.user_role != 2 else ())
        applications = cursor.fetchall()

        for i, app in enumerate(applications):
            tk.Label(self.applications_frame,
                     text=f"ID: {app['id']}, Car Number: {app['number_auto']}, Description: {app['discription']}, Status: {app['status']}").pack()

        tk.Button(self.applications_frame, text="Назад", command=self.create_main_screen).pack()

    def add_application(self):
        self.clear_screen()
        self.add_application_frame = tk.Frame(self.root)
        self.add_application_frame.pack(padx=20, pady=20)

        tk.Label(self.add_application_frame, text="Номер машины:").grid(row=0, column=0)
        tk.Label(self.add_application_frame, text="Описание:").grid(row=1, column=0)
        tk.Label(self.add_application_frame, text="Статус:").grid(row=2, column=0)

        self.car_number_entry = tk.Entry(self.add_application_frame)
        self.car_number_entry.grid(row=0, column=1)
        self.description_entry = tk.Entry(self.add_application_frame)
        self.description_entry.grid(row=1, column=1)
        self.status_entry = tk.Entry(self.add_application_frame)
        self.status_entry.grid(row=2, column=1)

        tk.Button(self.add_application_frame, text="Добавить", command=self.submit_application).grid(row=3, column=0,
                                                                                                   columnspan=2)
        tk.Button(self.add_application_frame, text="Назад", command=self.create_main_screen).grid(row=4, column=0,
                                                                                                 columnspan=2)

    def submit_application(self):
        number_auto = self.car_number_entry.get()
        discription = self.description_entry.get()
        status = self.status_entry.get()

        cursor = self.db.get_cursor()
        insert_query = "INSERT INTO applications (user_id, number_auto, discription, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (self.user_role, number_auto, discription, status))
        self.db.connection.commit()
        messagebox.showinfo("Успешно", "Заявление успешно зарегистрировано")
        self.create_main_screen()

    def change_application_status(self):
        self.clear_screen()
        self.change_status_frame = tk.Frame(self.root)
        self.change_status_frame.pack(padx=20, pady=20)

        tk.Label(self.change_status_frame, text="Заявление ID:").grid(row=0, column=0)
        tk.Label(self.change_status_frame, text="Новый статус (0=НЕИЗВЕСТНО, 1=ОДОБРЕНО, 2=ОТКЛОНЕНО):").grid(row=1, column=0)

        self.app_id_entry = tk.Entry(self.change_status_frame)
        self.app_id_entry.grid(row=0, column=1)
        self.status_entry = tk.Entry(self.change_status_frame)
        self.status_entry.grid(row=1, column=1)

        tk.Button(self.change_status_frame, text="Изменить статус", command=self.update_status).grid(row=2, column=0,
                                                                                                   columnspan=2)
        tk.Button(self.change_status_frame, text="Назад", command=self.create_main_screen).grid(row=3, column=0,
                                                                                               columnspan=2)

    def update_status(self):

        app_id = self.app_id_entry.get()
        status = self.status_entry.get()

        cursor = self.db.get_cursor()
        update_query = "UPDATE applications SET status = %s WHERE id = %s"
        cursor.execute(update_query, (status, app_id))
        self.db.connection.commit()
        messagebox.showinfo("Статус изменен", "Статус заявления успешно изменен")

        self.create_main_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    root.title("НарушенийНЕТ")
    app = ApplicationManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
