import re
import json
import aiofiles
import asyncio
import os

USER_DATA = 'UserData.json'


async def getMissingParameters(user_id: str) -> list:
    """
    @summary:
        Get all the parameters that the user with the given ID did not provide from the json file.
    @param user_id:
        The ID of the user that we want to get the missing parameters for.
    @return:
        List of the names of the parameters that the user did not provide.
    @raise ValueError:
            If no user found with the provided ID.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)
    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    missing_parameters = [key for key, value in user_entry["data"].items() if value is None]
    return missing_parameters


async def getExistingParameters(user_id: str) -> dict:
    """
    @summary:
        Get all the parameters and their values that the user with the given ID provided from the json file.
    @param user_id:
        The ID of the user that we want to get the existing parameters for.
    @return:
        Dictionary of the parameters and their values that the user provided.
    @raise ValueError:
            If no user found with the provided ID.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    existing_parameters = {key: value for key, value in user_entry["data"].items() if value is not None}
    return existing_parameters


def generateRegex(parameter: str) -> str:
    """
    @summary:
        Generate regex for a parameter that matching the first number after the parameter name.
    @param parameter:
        The name of the parameter that we want to generate regex for.
    @return:
        The regex that we generated for matching the number after the parameter name.
    """
    return parameter + "\s(\d+)"


async def updateUserData(user_data: dict, user_id: str) -> None:
    """
    @summary:
        Update the json file with the new data in the provided dictionary and the provided user ID.
    @param user_data:
        A dictionary that contains the names of the parameters and their values that the user provided.
    @param user_id:
        The ID of the user that we want to update his data.
    @raise ValueError:
            If no user found with the provided ID.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")


    for key, value in user_data.items():
        if key in user_entry["data"] and value is not None:
            user_entry["data"][key] = value

    async with aiofiles.open("UserData.json", "w") as file:
        await file.write(json.dumps(users_data, indent=4))



async def extractingData(user_response: str) -> dict:
    """
    @summary:
        Extract the data from the user response and return a dictionary that contains the names 
        of the parameters and their values that the user provided.
    @param user_response:
        The response that the user provided to the bot.
    @return:
        A dictionary that contains the names of the parameters and their
        values that the user provided in this user response.
    """""
    soilTemperatureRegex = generateRegex("soilTemperature")
    soilTemperatureMatch = re.search(soilTemperatureRegex, user_response)

    soilMoistureRegex = generateRegex("soilMoisture")
    soilMoistureMatch = re.search(soilMoistureRegex, user_response)

    pressureRegex = generateRegex("pressure")
    pressureMatch = re.search(pressureRegex, user_response)

    currentSpeedRegex = generateRegex("currentSpeed")
    currentSpeedMatch = re.search(currentSpeedRegex, user_response)

    updatedUserData = {"soilTemperature": soilTemperatureMatch.group(1) if soilTemperatureMatch else None,
                       "soilMoisture": soilMoistureMatch.group(1) if soilMoistureMatch else None,
                       "pressure": pressureMatch.group(1) if pressureMatch else None,
                       "currentSpeed": currentSpeedMatch.group(1) if currentSpeedMatch else None}
    return updatedUserData


async def getUserContentFormat(user_id: str) -> str:
    """
    @summary:
        Get the format of the user content that we want to send to the bot.
        the content contains the names of the parameters and their values that the user provided.
    @param user_id:
        The ID of the user that we want to get the format of his content.
    @return:
        The format of the user content that we want to send to the bot.
    @example output:
        soilTemperature is 20.  soilMoisture is 30.  pressure is 40.  currentSpeed is 50.
    """
    existingParameters = await getExistingParameters(user_id)
    userContentFormat = ""
    for key, value in existingParameters.items():
        userContentFormat += key + " is " + value + ".  "
    return userContentFormat


async def reset_user_data(user_id: str) -> None:
    """
    @summary:
        Reset the user data in the json file.
    @param user_id:
        The ID of the user that we want to reset his data.
    @raise ValueError:
            If no user found with the provided ID.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    for key in user_entry["data"].keys():
        user_entry["data"][key] = None

    async with aiofiles.open("UserData.json", "w") as file:
        await file.write(json.dumps(users_data, indent=4))


async def create_new_user(new_user_id: str):
    """
    @summary:
        Create new user in the json file.
    @param new_user_id:
        The ID of the new user that we want to create.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == new_user_id), None)
    if user_entry is not None:
        return

    new_user = {
        "id": new_user_id,
        "data": {
            "soilTemperature": None,
            "soilMoisture": None,
            "pressure": None,
            "currentSpeed": None
        },
        "isDataConfirmed": False,
        "userAskToChange": False
    }
    users_data.append(new_user)

    async with aiofiles.open("UserData.json", "w") as file:
        await file.write(json.dumps(users_data, indent=4))


async def delete_user(user_id: str) -> None:
    """
    @summary:
        Delete the user from the users data file.
    @param user_id:
        The ID of the user that we want to delete.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    users_data.remove(user_entry)

    async with aiofiles.open("UserData.json", "w") as file:
        await file.write(json.dumps(users_data, indent=4))


async def is_user_exists(user_id: str) -> bool:
    """
    @summary:
        Check if the user exists in the users data file.
    @param user_id:
        The ID of the user that we want to check.
    @return:
        True if the user exists in the users data file, False otherwise.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    return user_entry is not None


async def is_user_data_empty(user_id: str) -> bool:
    """
    @summary:
        Check if the user data is empty.
    @param user_id:
        The ID of the user that we want to check.
    @return:
        True if the user data is empty, False otherwise.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    for value in user_entry["data"].values():
        if value is not None:
            return False

    return True


async def is_all_user_data_provided(user_id: str) -> bool:
    """
    @summary:
        Check if the user provided all the data.
    @param user_id:
        The ID of the user that we want to check.
    @return:
        True if the user provided all the data, False otherwise.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    for value in user_entry["data"].values():
        if value is None:
            return False

    return True


async def is_user_data_confirmed(user_id: str) -> bool:
    """
    @summary:
        Check if the user confirmed his data.
    @param user_id:
        The ID of the user that we want to check.
    @return:
        True if the user confirmed his data, False otherwise.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    return user_entry["isDataConfirmed"]


async def check_user_answer_for_confirm_data(user_id: str, user_message: str) -> bool:
    """
    @summary:
        Check if the user confirm his data.
    @param user_id:
        The ID of the user that we want to check.
    @param user_message:
        The message that the user sent.
    @return:
        True if the user confirm his data, False otherwise.
    """
    affirmative_pattern = re.compile(r'^(yes|y|yeah|yep|affirmative|sure|ok|okay)$', re.I)
    if affirmative_pattern.match(user_message.strip()):
        return True
    return False


async def change_the_confirmation_to_true(user_id: str) -> None:
    """
    @summary:
        Change the confirmation of the user to True.
    @param user_id:
        The ID of the user that we want to change.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    user_entry["isDataConfirmed"] = True

    async with aiofiles.open("UserData.json", "w") as file:
        await file.write(json.dumps(users_data, indent=4))



async def is_user_want_change_data(user_id: str) -> bool:
    """
    @summary:
        Check if the user want to change his data.
    @param user_id:
        The ID of the user that we want to check.
    @return:
        True if the user want to change his data, False otherwise.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    return user_entry["userAskToChange"]


async def return_user_data(user_id: str) -> dict:
    """
    @summary:
        Return the user data.
    @param user_id:
        The ID of the user that we want to return his data.
    @return:
        The user data.
    """
    async with aiofiles.open("UserData.json", "r") as file:
        users_data = json.loads(await file.read())

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    return user_entry["data"]


# print(asyncio.run(return_user_data("2")))
