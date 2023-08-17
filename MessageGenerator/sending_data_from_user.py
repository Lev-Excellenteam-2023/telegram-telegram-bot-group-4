import os
import openai
import asyncio
from dotenv import load_dotenv
from user_data_management import getUserContentFormat, extractingData, updateUserData, is_user_exists, delete_user, \
    is_user_data_confirmed, is_user_want_change_data, is_user_data_empty, is_all_user_data_provided, \
    getMissingParameters, create_new_user, getExistingParameters, reset_user_data, check_user_answer_for_confirm_data, \
    generateRegex, change_the_confirmation_to_true

import asyncio
from user_data_management import is_user_exists, create_new_user, is_user_data_empty, is_all_user_data_provided, is_user_data_confirmed, is_user_want_change_data, getUserContentFormat, getMissingParameters


OPENING_STATEMENT = """
🌱 Welcome to CropLocatorBot! 🌾

Hello there, aspiring farmer! 🚜
Are you looking for the best areas to plant your crops?
You're at the right place!
Let me assist you in identifying the most suitable regions based on various environmental and soil parameters. Together, we'll ensure your crops thrive and yield bountifully.
"""


GENERAL_SYSTEM_CONTENT = "You are a Telegram bot that helps a user (who is a farmer) find areas for crops. dont introduce you (You introduced you in the past)."

ASK_FOR_ALL_DATA = GENERAL_SYSTEM_CONTENT + "dont introduce you (You introduced you in the past). Tell the user to provide these parameters. the data tou need from the user are: soilTemperature ,soilMoisture, pressure and currentSpeed "

ASK_FOR_DATA = GENERAL_SYSTEM_CONTENT + "So far the user has provided these data: "

RESPONSE_TO_NONSENSE = GENERAL_SYSTEM_CONTENT + "The user start the message with a nonsense word. Respond according to his last message in a humorous way. next, ask him if he want we help him to find areas for crops. "

RESPONSE_TO_NO_DATA = GENERAL_SYSTEM_CONTENT + "The user didn't provided any data. Respond according to his last message in a humorous way. next, ask him for providing the data he does not provided."

ASK_FOR_CONFIRMATION = GENERAL_SYSTEM_CONTENT + "the user provided all the data. Show him all the data he provided with their value and ask him for confirmation."

ASK_FOR_CHANGE = GENERAL_SYSTEM_CONTENT + "the user provided all the data but he want to change some data. tell hit to provide the data he want to change and the new value of the data."

RESPONSE_TO_CHANGE = ASK_FOR_CONFIRMATION

RESPONSE_TO_CONFIRMATION = GENERAL_SYSTEM_CONTENT + "the user confirmed the data. there is the areas that are suitable for the user. show him the areas and ask him if he want to see the details of the areas and a humorous closing sentence."


def configure() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


configure()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def send_message(user_message: str, user_id: str) -> str:
    """
    @summary:
        - Sending a message to the bot.
        - Updating/adding the user data with the new data that the user provided.
        - Generate the format of the user content that we want to send to the bot.
        - Applying the GPT-turbo-3.5 model.
        - Get the response from the bot.
    @param user_message:
        The message that the user provided to the bot.
    @param user_id:
        The ID of the user that we want to update his data.
    @return:
        The response from the bot.
    """
    # case the user is new.
    if not await is_user_exists(user_id):
        await create_new_user(user_id)
        return OPENING_STATEMENT

    user_content = user_message

    # case the user want the service - the user not provided any data.
    if await is_user_data_empty(user_id):
        SYSTEM_CONTENT = ASK_FOR_ALL_DATA

    # case the user not provided all the data.
    elif not await is_all_user_data_provided(user_id):
        SYSTEM_CONTENT = ASK_FOR_DATA + await getUserContentFormat(user_id) + "Tell the user to provide these data: " + ', '.join(
            await getMissingParameters(
                user_id)) + ". If the last message of the user includes one of the data he has not provided, don't ask him to provide this data but thank him for providing this data."

    # case the user provided all the data.
    elif await is_all_user_data_provided(user_id) and not await is_user_data_confirmed(user_id):
        await change_the_confirmation_to_true(user_id)
        SYSTEM_CONTENT = ASK_FOR_CONFIRMATION + "the data: " + await getUserContentFormat(user_id)

    # # case the user provided all the data but he want to change some data.
    # elif await is_all_user_data_provided(user_id) and await is_user_want_change_data(user_id):
    #     return ASK_FOR_CHANGE

    # case the user confirmed the data.
    elif await is_user_data_confirmed(user_id):
        SYSTEM_CONTENT = RESPONSE_TO_CONFIRMATION

    user_content = user_message + await getUserContentFormat(user_id)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_CONTENT
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    )

    # update the user data.
    userData = await extractingData(user_message)
    await updateUserData(userData, user_id)

    bot_response = completion.choices[0]["message"]["content"]
    return bot_response






