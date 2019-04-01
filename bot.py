import app


def send_money(user_id, recipient_id, money_amount):
    money_amount = int(money_amount)
    app.send_msg(user_id,
        f'Получен запрос на перевод в {money_amount} монет.\n'
        f'От кого: {app.USER_ID_TO_SMALL_ID[user_id]} ({app.USER_ID_TO_NAME[user_id]})\n'
        f'Кому: {app.USER_ID_TO_SMALL_ID[recipient_id]} ({app.USER_ID_TO_NAME[recipient_id]})\n')

    yield

    app.USER_ID_TO_MONEY[user_id] -= money_amount
    app.USER_ID_TO_MONEY[recipient_id] += money_amount

    app.send_msg(user_id,
        f'Перевод выполнен!\n'
        f'Ваш баланс: {app.USER_ID_TO_MONEY[user_id]}')
    app.send_msg(recipient_id,
        f'Вы получили {money_amount} монет.\n'
        f'От кого: {app.USER_ID_TO_SMALL_ID[user_id]} {app.USER_ID_TO_NAME[user_id]}')
