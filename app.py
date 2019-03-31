import json
from flask import Flask, request, make_response

app = Flask(__name__)


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
        return make_response('ok')

    print(event)


if __name__ == '__main__':
    app.run(debug=True)
