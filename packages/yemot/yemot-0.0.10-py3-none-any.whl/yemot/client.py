import requests

class Client:

    def __init__(self, username, password):
        """
        Initialize the client with the username and password
        """
        self.username = username
        self.password = password
        self.token = None
        self.base_url = "https://www.call2all.co.il/ym/api/"
        self.login()

    def login(self, username=None, password=None):
        """
        Login to the yemot
        """
        if username != None:
            self.username = username
        if password != None:
            self.password = password
        url = f"https://www.call2all.co.il/ym/api/Login?username={self.username}&password={self.password}"
        r = requests.get(url)
        if 'token' in r.json():
            self.token = r.json()['token']
            return r.json()["responseStatus"]
        if self.token == None:
            return 'username or password is incorrect'
        
    def logout(self):
        """
        Logout from the yemot
        """
        web_service = "Logout"
        r = requests.get(f"https://www.call2all.co.il/ym/api/{web_service}/?token={self.token}")
        return r.json()['message']
    
    def get(self, web_service, params=None):
        """
        Get request to the yemot
        """
        if self.token == None:
            self.login()
        r = requests.get(f"{self.base_url}{web_service}/?token={self.token}", params=params)
        if 'message' in r.json():
            self.login()
            r = requests.get(f"{self.base_url}{web_service}/?token={self.token}", params=params)
        return r.json()
    
    def post(self, web_service, data=None):
        """
        Post request to the yemot
        """
        if self.token == None:
            self.login()
        r = requests.post(f"{self.base_url}{web_service}/?token={self.token}", data=data)
        if 'message' in r.json():
            self.login()
            r = requests.post(f"{self.base_url}{web_service}/?token={self.token}", data=data)
        return r.json()
    

        
    
    