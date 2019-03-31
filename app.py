import json
import random
import urllib.request

from flask import Flask, request, make_response

app = Flask(__name__)

VK_ACCESS_TOKEN = 'dc1449199b76b349361569e33939d63c28a55bd5290afb85b0652599612965b492904ab880dec410aa1af'


@app.route("/", methods=["GET", "POST"])
def hears():
    event = json.loads(request.data)

    # verify this server's address
    if event['type'] == 'confirmation' and event['group_id'] == 180460328:
        # find the answer string ('8f05733a') at https://vk.com/club180460328?act=api&server=1
        return make_response('8f05733a', 200, {"content_type": "application/json"})

    if event['type'] == 'message_new':
        print('New message content: ', end='')
        print(event['object']['body'])
        print(event['object'])

        random_id = random.randrange(2 ** 32)
        user_id = event['object']['user_id']
        answer = "Приветик!"
        reply_to_user_response = urllib.request.urlopen(
            f'https://api.vk.com/method/messages.send?random_id={random_id}&user_id={user_id}&message={answer}&access_token={VK_ACCESS_TOKEN}&v=5.90').read()
        response_object = json.loads(reply_to_user_response)
        if 'error' in response_object:
            print('error: we didn\'t answer the user')
        print(response_object)

        return make_response('ok')

    print(event)


if __name__ == '__main__':
    app.run(debug=True)
