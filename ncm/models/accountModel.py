import json
from enum import Enum

class Profile:
    def __init__(self, data:json):
        self.userId = data['data']['profile']['userId']
        self.userType = data['data']['profile']['userType']
        self.nickname = data['data']['profile']['nickname']
        self.avatarImgId = data['data']['profile']['avatarImgId']
        self.avatarUrl = data['data']['profile']['avatarUrl']
        self.backgroundImgId = data['data']['profile']['backgroundImgId']
        self.backgroundUrl = data['data']['profile']['backgroundUrl']
        self.signature = data['data']['profile']['signature']
        self.createTime = data['data']['profile']['createTime']
        self.userName = data['data']['profile']['userName']
        self.accountType = data['data']['profile']['accountType']
        self.shortUserName = data['data']['profile']['shortUserName']
        self.birthday = data['data']['profile']['birthday']
        self.authority = data['data']['profile']['authority']
        self.gender = data['data']['profile']['gender']
        self.accountStatus = data['data']['profile']['accountStatus']
        self.province = data['data']['profile']['province']
        self.city = data['data']['profile']['city']
        self.authStatus = data['data']['profile']['authStatus']
        self.description = data['data']['profile']['description']

class Account:
    def __init__(self, data:json):
        self.id = data['account']['id']
        self.userName = data['account']['userName']
        self.type = data['account']['type']
        self.status = data['account']['status']
        self.whitelistAuthority = data['account']['whitelistAuthority']
        self.createTime = data['account']['createTime']
        self.tokenVersion = data['account']['tokenVersion']
        self.ban = data['account']['ban']
        self.baoyueVersion = data['account']['baoyueVersion']
        self.donateVersion = data['account']['donateVersion']
        self.vipType = data['account']['vipType']
        self.anonimousUser = data['account']['anonimousUser']
        self.paidFee = data['account']['paidFee']

class Subcount:
    def __init__(self, data:json):
        self.programCount = data['programCount']
        self.djRadioCount = data['djRadioCount']
        self.mvCount = data['mvCount']
        self.artistCount = data['artistCount']
        self.newProgramCount = data['newProgramCount']
        self.createDjRadioCount = data['createDjRadioCount']
        self.createdPlaylistCount = data['createdPlaylistCoun']
        self.subPlaylistCount = data['subPlaylistCount']
        self.code = data['code']


class loginMethod(int, Enum):
    PhoneLogin = 0
    EmailLogin = 1
    CodeLogin = 2
    AnonimousLogin = 3


class genderEnum(int, Enum):
    secret = 0
    male = 1
    female = 2

class requestEnum(str, Enum):
    post = 'post'
    get = 'get'
    put = 'put'