import json
import random
import requests
import bot
from collections import defaultdict, namedtuple

from flask import Flask, request, make_response, render_template

app = Flask(__name__)

VK_ACCESS_TOKEN = 'dc1449199b76b349361569e33939d63c28a55bd5290afb85b0652599612965b492904ab880dec410aa1af'


SMALL_ID_TO_USER_ID = {
    0: 85030597,
}
USER_ID_TO_SMALL_ID = {
    85030597: 0,
}

USER_ID_TO_MONEY = defaultdict(lambda: 100)

USER_ID_TO_NAME = {
    85030597: 'Наташа Мурашкина'
}


def send_msg(user_id, msg):
    random_id = random.randrange(2 ** 32)
    res = requests.get('https://api.vk.com/method/messages.send',
                 params={'random_id': random_id,
                         'user_id': user_id,
                         'message': msg,
                         'access_token': VK_ACCESS_TOKEN,
                         'v': '5.90'})
    print(res.status_code, res.json())


def get_user_name(user_id):
    res = requests.get('https://api.vk.com/method/users.get',
                 params={'user_ids': user_id,
                         'access_token': VK_ACCESS_TOKEN,
                         'v': '5.90'})
    print(res.status_code, res.json())
    udata = res.json()['response'][0]
    return udata['first_name'] + ' ' + udata['last_name']


def ensure_user(user_id):
    # if user has re-registered
    if user_id not in SMALL_ID_TO_USER_ID.values():
        small_id = random.randrange(100)
        while small_id in SMALL_ID_TO_USER_ID.keys():
            small_id = random.randrange(100)
        SMALL_ID_TO_USER_ID[small_id] = user_id
        USER_ID_TO_SMALL_ID[user_id] = small_id
        USER_ID_TO_NAME[user_id] = get_user_name(user_id)


def send_help(user_id):
    small_id = USER_ID_TO_SMALL_ID[user_id]
    send_msg(user_id,
        'Привет! Отправляйте деньги командой:\n'
        'отправить <номер> <количество монет>\n'
        'Например: отправить 0 100\n'
        f'Ваш номер: {small_id}')


@app.route("/vk-callback", methods=["GET", "POST"])
def vk_callback():
    event = json.loads(request.data)

    print(event)

    # verify this server's address
    if event['type'] == 'confirmation' and event['group_id'] == 180460328:
        # find the answer string https://vk.com/club180460328?act=api&server=1
        return make_response('7edcad6c', 200, {"content_type": "application/json"})

    if event['type'] == 'message_allow':
        ensure_user(event['object']['user_id'])
        send_help(event['object']['user_id'])
        return make_response('ok')

    if event['type'] == 'message_deny':
        return make_response('ok')

    if event['type'] == 'message_new':
        user_id = event['object']['user_id']
        message_content = event['object']['body']
        print(f'New message content: {message_content}')
        print(event['object'])

        ensure_user(event['object']['user_id'])

        chunks = message_content.split()

        if len(chunks) == 3 and chunks[0].lower() == 'отправить':
            try:
                recipient_small_id = int(chunks[1])
                recipient_id = SMALL_ID_TO_USER_ID[recipient_small_id]
                money_amount = int(chunks[2])
                bot.send_money(user_id, recipient_id, money_amount)
            except ValueError:
                send_msg(user_id, 'Извините, я не понимаю ваш запрос.')
                send_help(user_id)
                return make_response('ok')
        else:
            send_msg(user_id, 'Извините, я не понимаю ваш запрос.')
            send_help(user_id)

        return make_response('ok')

    print(event)


DisplayAccount = namedtuple('DisplayAccount', ['small_id', 'name', 'balance'])


@app.route("/")
def dashboard():
    accounts = [
        DisplayAccount(small_id, USER_ID_TO_NAME[uid], USER_ID_TO_MONEY[uid])
        for small_id, uid in sorted(SMALL_ID_TO_USER_ID.items())
    ]
    return render_template('dashboard.html', accounts=accounts)


if __name__ == '__main__':
    app.run(debug=True)
