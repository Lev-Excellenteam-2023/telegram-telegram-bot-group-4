import re
import json

USER_DATA = '/Users/alex/PycharmProjects/Telegram_bot_project_group_4/MessageGenerator/UserData.json'


def getMissingParameters() -> list:
    """
     @summary:
        Get all the parameters that the user did not provide from the json file.
    @return:
        List of the names of the parameters that the user did not provide.
    """
    with open(USER_DATA , "r") as file:
        parameters = json.load(file)
    missing_parameters = []

    for key, value in parameters.items():
        if value is None:
            missing_parameters.append(key)
    return missing_parameters


def getExistingParameters() -> dict:
    """
    @summary:
        Get all the parameters and their values that the user provided from the json file.
    @return:
        The names of the parameters and their values that the user provided.
    """
    with open(USER_DATA, "r") as file:
        parameters = json.load(file)
    existing_parameters = {}

    for key, value in parameters.items():
        if value is not None:
            existing_parameters[key] = value
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


def updateUserData(user_data: dict) -> None:
    """
    @summary:
        Update the json file with the new data int the provided dictionary.
    @param user_data:
        A dictionary that contains the names of the parameters and their values that the user provided.
    """
    with open(USER_DATA, "r") as file:
        parameters = json.load(file)

    for key, value in user_data.items():
        if value is not None:
            parameters[key] = value

    with open(USER_DATA, "w") as file:
        json.dump(parameters, file, indent=4)


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


def getUserContentFormat() -> str:
    """
    @summary:
        Get the format of the user content that we want to send to the bot.
        the content contains the names of the parameters and their values that the user provided.
    @return:
        The format of the user content that we want to send to the bot.
    @example output:
        soilTemperature is 20.  soilMoisture is 30.  pressure is 40.  currentSpeed is 50.
    """
    existingParameters = getExistingParameters()
    userContentFormat = ""
    for key, value in existingParameters.items():
        userContentFormat += key + " is " + value + ".  "
    return userContentFormat

