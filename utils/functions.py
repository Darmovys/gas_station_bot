import pymysql

host = "Insert your host"
port = "Insert your port"
user = "Insert your user"
password = "Insert your password"
db_name = "Insert your db_name"


def check_latynka(symbols):
    for c in symbols:
        if not (97 <= ord(c) <= 122 or 65 <= ord(c) <= 90):
            return False
    return True


def check_double(nums):
    dot_count = 0
    for c in nums:
        if not (48 <= ord(c) <= 57):
            if c == '.':
                dot_count += 1
            else:
                return False
    if dot_count == 1 and nums[0] != '.' and nums[-1] != '.':
        return True
    return False


def check_lat_num(symbols):
    for c in symbols:
        if not (97 <= ord(c) <= 122 or 65 <= ord(c) <= 90 or 48 <= ord(c) <= 57):
            return False
    return True


def insert_user_data(client_data):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO `клієнти` (`id_клієнта`, `ім’я_користувача`, 
            `ПІБ`, `номер_телефону`, `електронна_пошта`, `пароль`)
            VALUES (NULL, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            client_data['login'],
            client_data['full_name'],
            None if client_data['number'] == '' else client_data['number'],
            None if client_data['e_mail'] == '' else client_data['e_mail'],
            client_data['password']
        ))

        connection.commit()
        cursor.close()
        connection.close()

    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def check_user_data(client_data):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        select_query = "SELECT * FROM `клієнти` WHERE `ім’я_користувача` = %s AND `пароль` = %s"
        cursor.execute(select_query, (
            client_data['login'],
            client_data['password']
        ))
        result = cursor.fetchone()
        if result['ім’я_користувача'] == client_data["login"] and result["пароль"] == client_data["password"]:
            return True
        else:
            return False
    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def check_exist_user_name(client_data):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        select_query = "SELECT * FROM `клієнти` WHERE `ім’я_користувача` = %s"
        cursor.execute(select_query, (
            client_data['login'],
        ))

        result = cursor.fetchone()

        if not result:
            return True
        else:
            return False
    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def select_all_fuel_type():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = "SELECT * FROM типи_пального;"
            cursor.execute(sql)
            records = cursor.fetchall()
            result_text = ""
            for record in records:
                result_text += f"Пальне {record['id_пального']}, Назва: {record['Назва']}, Залишок л: " \
                               f"{record['Залишок_л']}, Ціна за 1 л: {record['Ціна_за_1_л']}\n\n"
            return result_text

    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def select_all_goods_type():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = "SELECT * FROM товари;"
            cursor.execute(sql)
            records = cursor.fetchall()
            result_text = ""
            for record in records:
                result_text += f"Товар {record['id_товару']}, Назва: {record['Назва_товару']}, Кількість: " \
                               f"{record['Кількість']}, Ціна: {record['Ціна']}\n\n"
            return result_text

    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def get_available_liters_by_id(fuel_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        select_query = "SELECT `Залишок_л` FROM `типи_пального` WHERE `id_пального` = %s"
        cursor.execute(select_query, (fuel_id,))
        result = cursor.fetchone()
        available_liters = int(result['Залишок_л'])
        return available_liters

    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def get_available_quantity_by_id(goods_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        cursor = connection.cursor()

        select_query = "SELECT `Кількість` FROM `товари` WHERE `id_товару` = %s"
        cursor.execute(select_query, (goods_id,))
        result = cursor.fetchone()
        available_quantity = int(result['Кількість'])
        return available_quantity

    except Exception as ex:
        print("У з'єднанні відмовлено...")
        print(ex)


def insert_fuel_purchase_data(purchase_data, user_data):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        fuel_id_mapping = {
            "fuel1": 1,
            "fuel2": 2,
            "fuel3": 3,
            "fuel4": 4,
            "fuel5": 5,
            "fuel6": 6,
            "fuel7": 7,
            "fuel8": 8,
            "fuel9": 9,
            "fuel10": 10
        }
        with connection.cursor() as cursor:
            user_query = "SELECT id_клієнта FROM клієнти WHERE ім’я_користувача = %s"
            cursor.execute(user_query, (user_data["login"]))
            user_result = cursor.fetchone()

            user_id = user_result['id_клієнта']

            for fuel_code, liters in purchase_data.items():
                fuel_id = fuel_id_mapping[fuel_code]
                sql = "INSERT INTO керування_пальним (купив, id_пального, кількість_л) VALUES (%s, %s, %s)"
                cursor.execute(sql, (user_id, fuel_id, liters))

            connection.commit()

    except Exception as ex:
        print("Помилка при вставці даних в таблицю керування_пальним:")
        print(ex)


def get_goods_prices():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            sql = "SELECT id_товару, Ціна FROM товари"
            cursor.execute(sql)
            records = cursor.fetchall()
            goods_prices = {f'goods{record["id_товару"]}': float(record["Ціна"]) for record in records}
            return goods_prices

    except Exception as ex:
        print("Помилка при отриманні цін товарів з бази даних:")
        print(ex)
        return None


def get_fuel_prices():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            sql = "SELECT id_пального, Ціна_за_1_л FROM типи_пального"
            cursor.execute(sql)
            records = cursor.fetchall()
            fuel_prices = {f'fuel{record["id_пального"]}': float(record["Ціна_за_1_л"]) for record in records}
            return fuel_prices

    except Exception as ex:
        print("Помилка при отриманні цін товарів з бази даних:")
        print(ex)
        return None


def total_fuel_price(purchase_data):
    total_price = 0.0
    fuel_prices = get_fuel_prices().copy()
    for fuel_code, litres in purchase_data.items():
        fuel_price = fuel_prices[fuel_code]
        total_price += fuel_price * float(litres)
    formatted_price = "{:.2f}".format(total_price)
    return formatted_price


def insert_goods_purchase_data(purchase_data, user_data):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        goods_id_mapping = {
            "goods1": 1,
            "goods2": 2,
            "goods3": 3,
            "goods4": 4,
            "goods5": 5,
            "goods6": 6,
            "goods7": 7,
            "goods8": 8,
            "goods9": 9,
            "goods10": 10
        }
        with connection.cursor() as cursor:
            user_query = "SELECT id_клієнта FROM клієнти WHERE ім’я_користувача = %s"
            cursor.execute(user_query, (user_data["login"]))
            user_result = cursor.fetchone()

            user_id = user_result['id_клієнта']

            for goods_code, quantity in purchase_data.items():
                goods_id = goods_id_mapping[goods_code]
                sql = "INSERT INTO керування_товарами (купив, id_товару, кількість) VALUES (%s, %s, %s)"
                cursor.execute(sql, (user_id, goods_id, quantity))

            connection.commit()

    except Exception as ex:
        print("Помилка при вставці даних в таблицю керування_товарами:")
        print(ex)


def total_goods_price(purchase_data):
    total_price = 0.0
    goods_prices = get_goods_prices().copy()
    for goods_code, quantity in purchase_data.items():
        goods_price = goods_prices[goods_code]
        total_price += goods_price * float(quantity)
    formatted_price = "{:.2f}".format(total_price)
    return formatted_price


def check_employee_id(employee_id):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = "SELECT * FROM працівники WHERE ідентифікатор = %s"
            cursor.execute(sql, employee_id)
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False

    except Exception as ex:
        print("Помилка при перевірці ідентифікатора працівника:")
        print(ex)


def add_quantity(goods):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            user_query = "SELECT id_працівника FROM працівники WHERE ідентифікатор = %s"
            cursor.execute(user_query, (goods["identifier"]))
            user_result = cursor.fetchone()

            user_id = user_result['id_працівника']

            sql = "INSERT INTO керування_товарами (додав, id_товару, кількість) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, goods["goods_id"], goods["goods_quantity"]))

            connection.commit()

    except Exception as ex:
        print("Помилка при перевірці ідентифікатора працівника:")
        print(ex)


def change_goods_price(goods):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = "UPDATE товари SET Ціна = %s WHERE id_товару = %s"
            cursor.execute(sql, (goods["goods_price"], goods["goods_id"]))

            connection.commit()

    except Exception as ex:
        print("Помилка при перевірці ідентифікатора працівника:")
        print(ex)


def add_liters(fuel):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            user_query = "SELECT id_працівника FROM працівники WHERE ідентифікатор = %s"
            cursor.execute(user_query, (fuel["identifier"]))
            user_result = cursor.fetchone()

            user_id = user_result['id_працівника']

            sql = "INSERT INTO керування_пальним (додав, id_пального, кількість_л) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, fuel["fuel_id"], fuel["liters_quantity"]))

            connection.commit()

    except Exception as ex:
        print("Помилка при перевірці ідентифікатора працівника:")
        print(ex)


def change_fuel_price(fuel):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            sql = "UPDATE типи_пального SET Ціна_за_1_л = %s WHERE id_пального = %s"
            cursor.execute(sql, (fuel["fuel_price"], fuel["fuel_id"]))

            connection.commit()

    except Exception as ex:
        print("Помилка при перевірці ідентифікатора працівника:")
        print(ex)
