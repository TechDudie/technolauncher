from hashlib import sha1
from json import loads
from multiprocessing import cpu_count, freeze_support, Pool
from os import get_terminal_size, makedirs, path, sep
from platform import architecture, system, uname, version
from re import finditer, match
from shutil import move
from sys import getwindowsversion
from warnings import filterwarnings
from zipfile import ZipFile
filterwarnings("ignore")
from requests import get

ARCH = {"X86_64": "x64", "ARM64": "arm64"}["".join([i if i in version() else "" for i in ["X86_64", "ARM64"]])]
WIDTH = get_terminal_size().columns

def parse_rule(rule, options) -> bool:
    if rule["action"] == "allow": value = False
    elif rule["action"] == "disallow": value = True

    for os_key, os_value in rule.get("os", {}).items():
        if os_key == "name":
            if os_value == "windows" and system() != 'Windows': return value
            elif os_value == "osx" and system() != 'Darwin': return value
            elif os_value == "linux" and system() != 'Linux': return value
        elif os_key == "arch" and os_value == "x86" and architecture()[0] != "32bit": return value
        elif os_key == "version" and not match(os_value, f"{getwindowsversion().major}.{getwindowsversion().minor}" if system() == "Windows" else uname().release): return value

    return not value

def download(data):
    if path.exists(data[1]): return (2, data)
    
    r = get(data[0], proxies=data[2])
    if r.status_code == 200:
        makedirs(path.dirname(data[1]), exist_ok=True)
        with open(data[1], "wb") as file: file.write(r.content)
    else: return (1, data)
    return (0, data)

def verify(data):
    try: open(data[1], "rb")
    except FileNotFoundError: return (2, data)
    
    with open(data[1], "rb") as file: return (int(not sha1(file.read()).hexdigest() == data[3]), data)

def extract(data):
    try: 
        with ZipFile(data[0]) as file:
            for f in file.namelist():
                if ARCH not in f: continue
                if len([i for i in finditer("\.", f)]) > 1: continue

                if f.endswith(sep): continue
                if f.endswith("MF"): continue
                if f.endswith("LIST"): continue
                if f.endswith("class"): continue

                file.extract(f, f"{data[1]}/cache/natives/")
                move(path.join(f"{data[1]}/cache/natives/", f), f"{data[1]}/versions/{data[2]}/natives/{f.split(sep)[-1]}")
    except FileNotFoundError: return (1, data[0])
    return (0, data)

def download_callback(status):
    global i, j, delta
    i += 1
    j += delta

    print("\033[1A\x1b[2K")
    print(f"Downloading libraries {str(round(j * 100)).rjust(2, ' ')}% [{('█' * int(j * (WIDTH - 29))).ljust(WIDTH - 30, ' ')}]", end="")

def verify_callback(status):
    global i, j, delta
    i += 1
    j += delta

    if status[0] != 0:
        download(status[1])

    print("\033[1A\x1b[2K")
    print(f"Verifying libraries {str(round(j * 100)).rjust(2, ' ')}% [{('█' * int(j * (WIDTH - 27))).ljust(WIDTH - 28, ' ')}]", end="")

def extract_callback(status):
    global i, j, delta
    i += 1
    j += delta

    print("\033[1A\x1b[2K")
    print(f"Extracting natives {str(round(j * 100)).rjust(2, ' ')}% [{('█' * int(j * (WIDTH - 26))).ljust(WIDTH - 27, ' ')}]", end="")

def run(directory, version, proxy):
    library_data = loads(open(f"{directory}/versions/{version}/{version}.json").read())["libraries"]
    
    freeze_support()

    data = []
    natives = []
    for library in library_data:
        if "rules" in library and (False if any([parse_rule(i, {}) for i in library["rules"]]) else True): continue
        sections = library["name"].split(":")
        data.append((library["downloads"]["artifact"]["url"], f"{directory}/libraries/{'/'.join(sections[0].split('.'))}/{sections[1]}/{sections[2]}/{sections[1]}-{sections[2]}{'-' + sections[3] if 3 < len(sections) else ''}.jar", {"http": f"socks5h://{proxy}", "https": f"socks5h://{proxy}", "socks5": f"socks5h://{proxy}"}, library["downloads"]["artifact"]["sha1"]))
        if "native" in library["name"]: natives.append((f"{directory}/libraries/{'/'.join(sections[0].split('.'))}/{sections[1]}/{sections[2]}/{sections[1]}-{sections[2]}{'-' + sections[3] if 3 < len(sections) else ''}.jar"))

    delta = 1 / len(data)
    
    pool = Pool(cpu_count())

    print("")
    i, j = 0, 0
    for asset in data:
        pool.apply_async(download, args=(asset, ), callback=download_callback)
    
    pool.close()
    pool.join()

    print("\n")
    pool = Pool(cpu_count())

    i, j = 0, 0
    for asset in data:
        pool.apply_async(verify, args=(asset, ), callback=verify_callback)
    
    pool.close()
    pool.join()
    
    makedirs(path.dirname(f"{directory}/versions/{version}/natives/"), exist_ok=True)
    delta = 1 / len(natives)

    print(natives)

    print("\n")
    pool = Pool(cpu_count())

    i, j = 0, 0
    for path in natives:
        pool.apply_async(extract, args=((path, directory, version), ), callback=extract_callback)
    
    pool.close()
    pool.join()

    print(f"\n\nMinecraft libraries for {version} installed successfully!")
