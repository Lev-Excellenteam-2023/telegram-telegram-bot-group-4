import requests

TOKEN = '6463124467:AAFtqwsJ-yIiM0ZTsEv48l9Pl9XcqDv5JoM'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://1b26-80-246-130-131.ngrok-free.app/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)