# cache.py
class Cache:
    _instance = None

    def __init__(self):
        self.cookies = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cookies = None
        return cls._instance

    def set_cookies(self, cookies):
        self.cookies = cookies

    def get_cookies(self):
        return self.cookies
