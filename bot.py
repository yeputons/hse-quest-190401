import app


def send_money(user_id, recipient_id, money_amount):
    money_amount = int(money_amount)
    app.USER_ID_TO_MONEY[user_id] -= money_amount
    app.USER_ID_TO_MONEY[recipient_id] += money_amount

    app.send_msg(user_id, f'Выполнено! Ваш баланс: {app.USER_ID_TO_MONEY[user_id]}')
    app.send_msg(recipient_id, f'Вы получили {money_amount} денег от пользователя {app.id_to_small_id(user_id)}'
                           f'\nВаш баланс: {app.USER_ID_TO_MONEY[recipient_id]}')
