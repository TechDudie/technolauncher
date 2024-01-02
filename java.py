import os
import platform
import shutil
import subprocess
import warnings
import zipfile
warnings.filterwarnings("ignore")
import requests

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

if __name__ == "__main__":
    uname = platform.uname()
    operating_system = {"Windows": "win", "Darwin": "macosx", "Linux": "linux"}[uname[0]]
    processor_architecture = {"X86_64": "x64", "ARM64": "aarch64"}["".join([i if i in uname[3] else "" for i in ["X86_64", "ARM64"]])]
    url = f"https://cdn.azul.com/zulu/bin/zulu21.30.15-ca-{TYPE.lower()}21.0.1-{operating_system}_{processor_architecture}.zip"
    cache = f"{DIRECTORY}/cache/zulu21.30.15-ca-{TYPE.lower()}21.0.1-{operating_system}_{processor_architecture}.zip"
    path = f"{DIRECTORY}/java/"
    target = f"{path}{JAVA_VERSION}"
    executable = {
        "Windows": f"{target}/bin/java.exe",
        "Darwin": f"{target}/zulu-{JAVA_VERSION}.{TYPE.lower()}/Contents/Home/bin/java",
        "Linux": f"{target}/bin/java"
    }[uname[0]]


    print(f"Detected OS: {uname[0].replace('Darwin', 'MacOS')}")
    print(f"Detected Architecture: {''.join([i if i in uname[3] else '' for i in ['X86_64', 'ARM64']])}")
    print(f"Downloading Java {JAVA_VERSION} Azul Zulu {AZUL_VERSION} {TYPE.upper()} from {url}")

    r = requests.get(url, proxies={"http": f"socks5h://{PROXY}", "https": f"socks5h://{PROXY}", "socks5": f"socks5h://{PROXY}"})
    if r.status_code == 200:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(cache, "wb") as file: file.write(r.content)
    else:
        print("Unable to download Java. Please submit an issue with the following information:")
        print(f"Detected OS: {uname[0].replace('Darwin', 'MacOS')}")
        print(f"Detected Architecture: {''.join([i if i in uname[3] else '' for i in ['X86_64', 'ARM64']])}")
        print(f"Minecraft Version: {VERSION}")
        print(f"Java Version: {JAVA_VERSION}")
        print(f"Azul Version: {AZUL_VERSION}")
        print(f"Java Type: {TYPE}")
        exit(1)

    with zipfile.ZipFile(cache) as file:
        file.extractall(path)

    shutil.move(f"{DIRECTORY}/java/zulu21.30.15-ca-{TYPE.lower()}21.0.1-{operating_system}_{processor_architecture}", target)

    if uname[0] != "Windows":
        subprocess.run(["chmod", "+x", executable])
    
    if uname[0] == "Darwin":
        subprocess.run(["xattr", "-d", "com.apple.quarantine", executable])

    print(f"Testing Java {JAVA_VERSION} Azul Zulu {AZUL_VERSION} {TYPE.upper()}")

    subprocess.run([executable, "-version"])

    print("Java installed successfully!")