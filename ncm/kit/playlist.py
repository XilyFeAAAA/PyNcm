from ncm.drivers.reqDriver import RequestHandler

ws = RequestHandler()

class Playlist:
    def __init__(self, sid):
        self._sid = sid

    def similar(self):
        # 获取相似歌单
        pass

    def relatedPlaylist(self):
        # 相关歌单推荐
        pass

    def getTrack(self, limit):
        # 获取歌单所有歌曲
        res = ws.get(f'/playlist/track/all?id={self._sid}&limit={limit}').json()
        return res

    def dynamic(self):
        # 歌单详情动态
        pass

    def getPlaylistSuber(self):
        # 歌单收藏者
        pass

    def playlistComment(self):
        # 歌单评论
        pass