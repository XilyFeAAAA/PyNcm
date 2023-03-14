from ncm import account
from ncm import kit
from ncm import models


class CloudMusicApi:
    def __init__(self):
        self.user = account.User()
        self.kit = kit
