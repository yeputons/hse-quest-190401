import json
import random
import requests

from collections import defaultdict

from flask import Flask, request, make_response



app = Flask(__name__)

VK_ACCESS_TOKEN = 'dc1449199b76b349361569e33939d63c28a55bd5290afb85b0652599612965b492904ab880dec410aa1af'


SMALL_ID_TO_USER_ID = dict()

SMALL_ID_TO_USER_ID[0] = 85030597

USER_ID_TO_MONEY = defaultdict(lambda: 100)

#
# @app.route("/money", methods=["GET", "POST"])
# def hears2():
#     pass


def send_msg(user_id, msg):
    random_id = random.randrange(2 ** 32)
    res = requests.get('https://api.vk.com/method/messages.send',
                 params={'random_id': random_id,
                         'user_id': user_id,
                         'message': msg,
                         'access_token': VK_ACCESS_TOKEN,
                         'v': '5.90'})
    print(res.status_code, res.json())


@app.route("/", methods=["GET", "POST"])
def hears():
    event = json.loads(request.data)

    print(event)

    # verify this server's address
    if event['type'] == 'confirmation' and event['group_id'] == 180460328:
        # find the answer string ('8f05733a') at https://vk.com/club180460328?act=api&server=1
        return make_response('8f05733a', 200, {"content_type": "application/json"})

    if event['type'] == 'message_allow':
        user_id = event['object']['user_id']

        # if user has re-registered
        if user_id not in SMALL_ID_TO_USER_ID.values():
            small_id = random.randrange(100)
            while small_id in SMALL_ID_TO_USER_ID.keys():
                small_id = random.randrange(100)
            SMALL_ID_TO_USER_ID[small_id] = user_id

        send_msg(user_id, f'Привет! Отправь деньги командой: send ID amount, например: send 7 15')
        send_msg(user_id, f'Ваш ID {small_id}')
        return make_response('ok')

    if event['type'] == 'message_deny':
        return make_response('ok')

    if event['type'] == 'message_new':
        user_id = event['object']['user_id']
        message_content = event['object']['body']
        print(f'New message content: {message_content}')
        print(event['object'])

        chunks = message_content.split()
        if len(chunks) == 3 and chunks[0].lower() == 'send':
            try:
                recipient_small_id = int(chunks[1])
                recipient_id = SMALL_ID_TO_USER_ID[recipient_small_id]
                money_amount = int(chunks[2])
            except ValueError:
                send_msg(user_id, 'I\'m sorry, I don\'t understand your query')
                return make_response('ok')

        USER_ID_TO_MONEY[user_id] -= money_amount
        USER_ID_TO_MONEY[recipient_id] += money_amount

        user_small_id = list(filter(lambda x: x[1] == user_id, SMALL_ID_TO_USER_ID.items()))[0]

        send_msg(user_id, f'Done! Your new balance is {USER_ID_TO_MONEY[user_id]}')
        send_msg(recipient_id, f'You\'ve received {money_amount} money from user f{user_small_id}')

        return make_response('ok')

    print(event)


if __name__ == '__main__':
    app.run(debug=True)
