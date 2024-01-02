import json
import os
import platform
import re
import sys
import warnings
warnings.filterwarnings("ignore")

DIRECTORY = "/Users/3124224/Library/Application Support/devnolauncher"
VERSION = "1.20.4"
PROXY = "192.168.86.68:1060"

JAVA = {
    "1.20.4": "21",
    "1.8.9": "8",
    "default": "21"
}

AZUL = {
    "21": "21.30.15",
    "8": "8.74.0.17",
    "default": "21.30.15"
}

try:
    JAVA_VERSION = JAVA[VERSION]
except:
    JAVA_VERSION = JAVA["default"]

try:
    AZUL_VERSION = AZUL[JAVA_VERSION]
except:
    AZUL_VERSION = AZUL["default"]

TYPE = "jre"

USERNAME = "TechnoDot"
UUID = "9a467ecf8eaf4d9cb44050eb9b60581a"
TOKEN = "eynevergonnagiveyouupnevergonnaletyoudownnevergonnarunaroundanddesertyou"

def parse_rule(rule, options) -> bool:
    if rule["action"] == "allow": value = False
    elif rule["action"] == "disallow": value = True

    for os_key, os_value in rule.get("os", {}).items():
        if os_key == "name":
            if os_value == "windows" and platform.system() != 'Windows': return value
            elif os_value == "osx" and platform.system() != 'Darwin': return value
            elif os_value == "linux" and platform.system() != 'Linux': return value
        elif os_key == "arch" and os_value == "x86" and platform.architecture()[0] != "32bit": return value
        elif os_key == "version" and not re.match(os_value, f"{sys.getwindowsversion().major}.{sys.getwindowsversion().minor}" if platform.system() == "Windows" else platform.uname().release): return value

    for features_key in rule.get("features", {}).keys():
        if features_key == "has_custom_resolution" and not options.get("customResolution", False): return value
        elif features_key == "is_demo_user" and not options.get("demo", False): return value
        elif features_key == "has_quick_plays_support" and options.get("quickPlayPath") is None: return value
        elif features_key == "is_quick_play_singleplayer" and options.get("quickPlaySingleplayer") is None: return value
        elif features_key == "is_quick_play_multiplayer" and options.get("quickPlayMultiplayer") is None: return value
        elif features_key == "is_quick_play_realms" and options.get("quickPlayRealms") is None: return value

    return not value

def classpath(data):
    sep = ";" if platform.system() == "Windows" else ":"
    libraries = ""

    for library in data["libraries"]:
        if "rules" in library and (False if any([parse_rule(i, {}) for i in library["rules"]]) else True): continue
        sections = library["name"].split(":")
        libraries += f"{DIRECTORY}/libraries/{'/'.join(sections[0].split('.'))}/{sections[1]}/{sections[2]}/{sections[1]}-{sections[2]}{'-' + sections[3] if 3 < len(sections) else ''}.jar{sep}"

    libraries += f"{DIRECTORY}/versions/{VERSION}/{VERSION}.jar"
    return libraries

def jvm_arguments(data):
    arguments = []
    
    for argument in data["arguments"]["jvm"]:
        if isinstance(argument, dict):
            if "rules" in argument and (False if any([parse_rule(i, {}) for i in argument["rules"]]) else True): continue
            arguments.append(argument["value"])
        else:
            if argument.find("${nativesDirectory}") != -1:
                arguments.append(argument.replace("${nativesDirectory}", f"{DIRECTORY}/versions/{VERSION}/natives"))
            elif argument.find("${launcher_name}") != -1:
                arguments.append(argument.replace("${launcher_name}", "technolauncher"))
            elif argument.find("${launcher_version}") != -1:
                arguments.append(argument.replace("${launcher_version}", "1.0"))
            elif argument.find("${classpath}") != -1:
                arguments.append(argument.replace("${classpath}", classpath(data)))
        

def game_arguments(data):
    arguments = []
    
    for argument in data["argumnets"]["game"]:
        if not isinstance(argument, dict):
            arguments.append(argument)
    
    for i, argument in enumerate(arguments):
        if argument == "${auth_player_name}":
            arguments[i] = USERNAME
        if argument == "${version_name}":
            arguments[i] = VERSION
        if argument == "${game_directory}":
            arguments[i] = f"{DIRECTORY}/game"
        if argument == "${assets_root}":
            arguments[i] = f"{DIRECTORY}/assets"
        if argument == "${assets_index_name}":
            arguments[i] = data["assetIndex"]["id"]
        if argument == "${auth_uuid}":
            arguments[i] = UUID
        # if argument == "${clientid}":
        #     arguments[i] = USERNAME
        # if argument == "${auth_xuid}":
        #     arguments[i] = USERNAME
        if argument == "${user_type}":
            arguments[i] = "msa"
        if argument == "${version_type}":
            arguments[i] = "release" if VERSION.find(".") != -1 else "snapshot"

    return arguments

if __name__ == "__main__":
    """
        options = {
            # This is needed
            "username": The Username,
            "uuid": uuid of the user,
            "token": the accessToken,
            # This is optional
            "executablePath": "java", # The path to the java executable
            "defaultExecutablePath": "java", # The path to the java executable if the version.json has none
            "jvmArguments": [], #The jvmArguments
            "launcherName": "minecraft-launcher-lib", # The name of your launcher
            "launcherVersion": "1.0", # The version of your launcher
            "gameDirectory": "/home/user/.minecraft", # The gameDirectory (default is the path given in arguments)
            "demo": False, # Run Minecraft in demo mode
            "customResolution": False, # Enable custom resolution
            "resolutionWidth": "854", # The resolution width
            "resolutionHeight": "480", # The resolution heigth
            "server": "example.com", # The IP of a server where Minecraft connect to after start
            "port": "123", # The port of a server where Minecraft connect to after start
            "nativesDirectory": "minecraft_directory/versions/version/natives", # The natives directory
            "enableLoggingConfig": False, # Enable use of the log4j configuration file
            "disableMultiplayer": False, # Disables the multiplayer
            "disableChat": False, # Disables the chat
            "quickPlayPath": None, # The Quick Play Path
            "quickPlaySingleplayer": None, # The Quick Play Singleplayer
            "quickPlayMultiplayer": None, # The Quick Play Multiplayer
            "quickPlayRealms": None, # The Quick Play Realms
        }
    """

    with open(f"{DIRECTORY}/versions/{VERSION}/{VERSION}.json") as file:
        data = json.load(file)

    command = [{
        "Windows": f"{DIRECTORY}/java/{JAVA_VERSION}/bin/java.exe",
        "Darwin": f"{DIRECTORY}/java/{JAVA_VERSION}/zulu-{JAVA_VERSION}.{TYPE.lower()}/Contents/Home/bin/java",
        "Linux": f"{DIRECTORY}/java/{JAVA_VERSION}/bin/java"
    }[platform.system()]]

    command += jvm_arguments(data)
    command.append(data["mainClass"])
    command += game_arguments(data)
    
    print(command)