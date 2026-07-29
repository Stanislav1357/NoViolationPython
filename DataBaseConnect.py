import pymysql
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        port=3306,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('succesfully connect to db')


    def view_all():
        try:
            with connection.cursor() as cursor:
                table = input('Введите название таблицы: ')
                select_all_rows = f"SELECT * FROM {table}"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

        finally:
            connection.close()


    def add():
        try:
            with connection.cursor() as cursor:
                table = input('Введите имя таблицы куда хотите добавить: ')

                if table == 'users':

                    value_login = input('Введите значение для LOGIN поля: ')
                    value_password = input('Введите значение для PASSWORD поля: ')
                    value_full_name = input('Введите значение для FULL_NAME поля: ')
                    value_phone_num = input('Введите значение для PHONE_NUM поля: ')
                    value_email = input('Введите значение для EMAIL поля: ')
                    value_role_id = input('Введите значение для ROLE_ID поля: ')

                    insert_rows = (
                        f"INSERT INTO {table} (login, password, full_name, phone_num, email, role_id) VALUES "
                        "(%s, %s, %s, %s, %s, %s)"
                    )

                    cursor.execute(insert_rows, (
                    value_login, value_password, value_full_name, value_phone_num, value_email,
                    value_role_id))

                    connection.commit()
                    print(f"Добавлены значения в таблицу {table}.")

                elif table == 'roles':

                    value_role_name = input('Введите значение для ROLE_NAME поля: ')

                    insert_rows = (
                        f"INSERT INTO {table} (role) VALUES "
                        "(%s)"
                    )

                    cursor.execute(insert_rows, (
                        value_role_name))
                    connection.commit()
                    print(f"Добавлены значения в таблицу {table}.")


                elif table == 'applications':

                    value_user_id = input('Введите значение для USER_ID поля: ')
                    value_car_num = input('Введите значение для CAR_NUM поля: ')
                    value_description = input('Введите значение для DESCRIPTION поля: ')
                    value_status = input('Введите значение для STATUS поля: ')

                    insert_rows = (
                        f"INSERT INTO {table} (user_id, car_num, description, status) VALUES "
                        "(%s, %s, %s, %s)"
                    )

                    cursor.execute(insert_rows, (
                        value_user_id, value_car_num, value_description, value_status))
                    connection.commit()
                    print(f"Добавлены значения в таблицу {table}.")

                else:
                    print("Введите правильное название таблицы! (users/roles/applications)")


        finally:
            connection.close()


    def delete():
        try:
            with connection.cursor() as cursor:
                table = input('Введите имя таблицы: ')
                row_id = input('Введите ID поля для удаления: ')
                delete_row = f"DELETE FROM {table} WHERE id = %s"
                cursor.execute(delete_row, (row_id,))
                connection.commit()
            print(f"Удалено поле с ID {row_id} из таблицы {table}.")

        finally:
            connection.close()


    def update():
        try:
            with connection.cursor() as cursor:
                table = input('Введите имя таблицы: ')
                column = input('Введите имя колонки для обновления: ')
                value = input('Введите новое значение для этого поля: ')
                row_id = input('введите ID поля для изменения: ')
                update_row = f"UPDATE {table} SET {column} = %s WHERE id = %s"
                cursor.execute(update_row, (value, row_id))
                connection.commit()

                print(f"Изменено поле с ID {row_id} в таблице {table}.")

        finally:
            connection.close()

except Exception as ex:
    print("failed")
    print(ex)
