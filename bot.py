import app


def send_money(src_key, dest_key, amount):
    src_id = app.USER_ID_TO_SMALL_ID[src_key]
    dest_id = app.USER_ID_TO_SMALL_ID[dest_key]
    src_name = app.USER_ID_TO_NAME[src_key]
    dest_name = app.USER_ID_TO_NAME[dest_key]
    # ^^^^^^^^^ наверху технический код, скука ^^^^^^^^^

    app.send_msg(src_key,  # Сообщение отправителю
        f'Получен запрос на перевод в {amount} монет.\n'
        f'От кого: {src_id} ({src_name})\n'
        f'Кому: {dest_id} ({dest_name})\n')

    yield  # Задержка 5 секунд

    app.USER_ID_TO_MONEY[src_key] -= amount  # Уменьшить баланс отправителя
    app.USER_ID_TO_MONEY[dest_key] += amount  # Увеличить баланс получателя

    app.send_msg(src_key,  # Сообщение отправителю
        f'Перевод выполнен!\n'
        f'Ваш баланс: {app.USER_ID_TO_MONEY[src_key]}')
    app.send_msg(dest_key,  # Сообщение получателю
        f'Вы получили {amount} монет.\n'
        f'От кого: {src_id} {src_name}\n'
        f'Ваш баланс: {app.USER_ID_TO_MONEY[dest_key]}')
