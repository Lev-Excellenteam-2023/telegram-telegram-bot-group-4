import asyncio
from user_data_management import is_user_exists, create_new_user, is_user_data_empty, is_all_user_data_provided, is_user_data_confirmed, is_user_want_change_data


OPENING_STATEMENT = """
🌱 Welcome to CropLocatorBot! 🌾

Hello there, aspiring farmer! 🚜
Are you looking for the best areas to plant your crops?
You're at the right place!
Let me assist you in identifying the most suitable regions based on various environmental and soil parameters. Together, we'll ensure your crops thrive and yield bountifully.
"""


GENERAL_SYSTEM_CONTENT = "You are a Telegram bot that helps a user (who is a farmer) find areas for crops."

ASK_FOR_ALL_DATA = GENERAL_SYSTEM_CONTENT + "Tell the user to provide all the data that you need from him. the data tou need from the user are: soilTemperature, soilMoisture, pressure, currentSpeed."

ASK_FOR_DATA = GENERAL_SYSTEM_CONTENT + "So far the user has provided these data: "
# a function to get the data that the user provided so far.
# .. if the user provided in the last message a new data. thank him for providing the data, Tell him what data he has provided so far and ask him for providing the data he does not provided.

RESPONSE_TO_NONSENSE = GENERAL_SYSTEM_CONTENT + "The user start the message with a nonsense word. Respond according to his last message in a humorous way. next, ask him if he want we help him to find areas for crops. "

RESPONSE_TO_NO_DATA = GENERAL_SYSTEM_CONTENT + "The user didn't provided any data. Respond according to his last message in a humorous way. next, ask him for providing the data he does not provided." + "...פונקציה שתספק את מה שחסר..."

ASK_FOR_CONFIRMATION = GENERAL_SYSTEM_CONTENT + "the user provided all the data. " + "..." + "Show him all the data he provided with their value and ask him for confirmation."

ASK_FOR_CHANGE = GENERAL_SYSTEM_CONTENT + "the user provided all the data but he want to change some data. tell hit to provide the data he want to change and the new value of the data."

RESPONSE_TO_CHANGE = ASK_FOR_CONFIRMATION

RESPONSE_TO_CONFIRMATION = GENERAL_SYSTEM_CONTENT + "the user confirmed the data. there is the areas that are suitable for the user. show him the areas and ask him if he want to see the details of the areas and a humorous closing sentence."


async def get_system_content(user_id: str) -> str:
    """
    @summary:
        - Get the system content according to the user state.
    @param user_id:
        The ID of the user that we want to get his system content.
    @return:
        The system content according to the user state.
    """
    # case the user is new.
    if not await is_user_exists(user_id):
        await create_new_user(user_id)
        return OPENING_STATEMENT

    # case the user want the service - the user not provided any data.
    if await is_user_data_empty(user_id):
        return ASK_FOR_ALL_DATA

    # case the user not provided all the data.
    if not await is_all_user_data_provided(user_id):
        return ASK_FOR_DATA

    # case the user provided all the data.
    if await is_all_user_data_provided(user_id) and not await is_user_want_change_data(user_id):
        return ASK_FOR_CONFIRMATION

    # case the user provided all the data but he want to change some data.
    if await is_all_user_data_provided(user_id) and await is_user_want_change_data(user_id):
        return ASK_FOR_CHANGE

    # case the user confirmed the data.
    if await is_user_data_confirmed(user_id):
        return RESPONSE_TO_CONFIRMATION




