import os
import openai
from dotenv import load_dotenv
from retrying import retry
from user_data_management import getUserContentFormat, extractingData, updateUserData


SYSTEM_CONTENT = "You are a bot on telegram that extracts 4 data from a user. the data you need from the user are: soilTemperature, soilMoisture, pressure, currentSpeed." \
                 "Ask the user for providing the data he does not provided."


def configure() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


configure()
openai.api_key = os.getenv("OPENAI_API_KEY")


def send_message(user_message: str, user_id: str) -> str:
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
    userData = extractingData(user_message)
    updateUserData(userData, user_id)

    user_content = getUserContentFormat(user_id)

    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
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
    bot_response = completion.choices[0]["message"]["content"]
    return bot_response


