import requests
from flask import Flask, Response, request
from script_to_join_to_bot import TOKEN


app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    message = request.get_json()['message']['text']
    print(message)
    chat_id = request.get_json()['message']['chat']['id']
    print(chat_id)
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, message))
    print(res)
    return Response("success")


# Run the server on an available port
if __name__ == '__main__':
    app.run(port=5002)