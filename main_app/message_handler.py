"""
this file is used to handle the message from the user
and send it to the gpt model to get the response from the bot.
"""
from MessageGenerator.sending_data_from_user import send_message

# dictionary that contains the users id and history of the conversation with the bot.
USERS_HISTORY = {}


async def handle_user_message(user_message: str, id:str) -> str:
    """
    This function is used to handle the message from the user
    :param user_message: the message that the user provided to the bot.
    :param id: the id of the user.
    :return: the response from the bot.
    """
    if id not in USERS_HISTORY:
        USERS_HISTORY[id] = []
    USERS_HISTORY[id].append(user_message)
    bot_response = send_message(user_message)
    return bot_response
