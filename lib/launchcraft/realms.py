import json
import requests

class RealmsAPI:
    def __init__(self, version, proxy=None):
        self.username = "TechnoDot"
        self.uuid = ""
        self.token = ""
        self.version = version

        self.session = requests.Session()
        self.cookies = {}

        if proxy:
            self.session.proxies.update({"http": f"socks5h://{proxy}", "https": f"socks5h://{proxy}", "socks5": f"socks5h://{proxy}"})

    def create_session(self, token):
        self.token = token

        r = self.session.get("https://api.minecraftservices.com/minecraft/profile", headers={"Authorization": f"Bearer {self.token}"})

        if r.status_code == 401: return "Invalid token"
        if r.status_code != 200: return "Error"
        if r.json()["name"] != self.username: "Invalid token"

        self.uuid = r.json()["id"]

        self.cookies = {
            "sid": f"token:{self.token}:{self.uuid}",
            "user": self.username,
            "version": self.version
        }

        print(self.uuid)
        print(self.cookies)

        return self.uuid
    
    def _get(self, endpoint):
        r = self.session.get(f"https://pc.realms.minecraft.net/{endpoint}", cookies=self.cookies)

        if r.status_code != 200: return "Error"

        try:
            content = json.loads(r.text)
        except ValueError:
            content = r.content
        
        return content
    
    def _post(self, endpoint, payload={}):
        r = self.session.get(f"https://pc.realms.minecraft.net/{endpoint}", cookies=self.cookies, json=payload)

        if r.status_code != 200: return "Error"

        try:
            content = json.loads(r.text)
        except ValueError:
            content = r.content
        
        return content
    
    def get_realms(self):
        self.realms = self._get("worlds")
        return self.realms
