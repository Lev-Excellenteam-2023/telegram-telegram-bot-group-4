import re
import json


def getMissingParameters(user_id: str) -> list:
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
    with open("UserData.json", "r") as file:
        users_data = json.load(file)

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    missing_parameters = [key for key, value in user_entry["data"].items() if value is None]
    return missing_parameters


def getExistingParameters(user_id: str) -> dict:
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
    with open("UserData.json", "r") as file:
        users_data = json.load(file)

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


def updateUserData(user_data: dict, user_id: str) -> None:
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
    with open("UserData.json", "r") as file:
        users_data = json.load(file)

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    for key, value in user_data.items():
        if key in user_entry["data"] and value is not None:
            user_entry["data"][key] = value

    # Save the modified data back to the JSON file
    with open("UserData.json", "w") as file:
        json.dump(users_data, file, indent=4)


def extractingData(user_response: str) -> dict:
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


def getUserContentFormat(user_id: str) -> str:
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
    existingParameters = getExistingParameters(user_id)
    userContentFormat = ""
    for key, value in existingParameters.items():
        userContentFormat += key + " is " + value + ".  "
    return userContentFormat


def reset_user_data(user_id: str) -> None:
    """
    @summary:
        Reset the user data in the json file.
    @param user_id:
        The ID of the user that we want to reset his data.
    @raise ValueError:
            If no user found with the provided ID.
    """
    with open("UserData.json", "r") as file:
        users_data = json.load(file)

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    for key, value in user_entry["data"].items():
        user_entry["data"][key] = None

    # Save the modified data back to the JSON file
    with open("UserData.json", "w") as file:
        json.dump(users_data, file, indent=4)


def create_new_user(new_user_id: str):
    """
    @summary:
        Create new user in the json file.
    @param new_user_id:
        The ID of the new user that we want to create.
    """
    with open("UserData.json", "r") as file:
        users_data = json.load(file)

        # check if the user already exists:
        user_entry = next((entry for entry in users_data if entry["id"] == new_user_id), None)
        if user_entry is not None:
            return
        # create new user:
        new_user = {"id": new_user_id, "data": {
            "soilTemperature": None,
            "soilMoisture": None,
            "pressure": None,
            "currentSpeed": None
        }}
        users_data.append(new_user)

        # Save the modified data back to the JSON file
        with open("UserData.json", "w") as file:
            json.dump(users_data, file, indent=4)


def delete_user(user_id: str) -> None:
    """
    @summary:
        Delete the user from the users data file.
    @param user_id:
        The ID of the user that we want to delete.
    """
    with open("UserData.json", "r") as file:
        users_data = json.load(file)

    user_entry = next((entry for entry in users_data if entry["id"] == user_id), None)

    if user_entry is None:
        raise ValueError(f"No user found with ID {user_id}")

    users_data.remove(user_entry)

    # Save the modified data back to the JSON file
    with open("UserData.json", "w") as file:
        json.dump(users_data, file, indent=4)

