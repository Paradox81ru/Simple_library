import os


def clear_display():
    """ Очищает дисплей """
    os.system("cls")


def print_awaiting_message(msg):
    """ Вывод ожидающего сообщения """
    print(msg)
    input("press any key...")
