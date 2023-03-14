from ncm.account.userBase import UserBase
from ncm.models.exceptions import NoPlaylistError

class User(UserBase):
    def __init__(self):
        super().__init__()

    @property
    def uid(self):
        if self._info is None:
            self._info = self.account()
        return self._info.id

    @property
    def lovedPlaylist(self):
        sid = 0
        res = self.getPlaylist(self._info.id)['playlist']
        if not len(res) or '喜欢的音乐' not in res[0]['name']:
            return -1
        return res[0]['id']