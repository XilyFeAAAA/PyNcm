from ncm.drivers.reqDriver import RequestHandler

ws = RequestHandler()


class Musician:
    def __init__(self):
        self._id: int

    def getArtlist(self):
        # 歌手分类列表
        pass

    def topSong(self):
        # 歌手热门50首歌曲
        pass

    def allSong(self):
        # 歌手全部歌曲
        pass

    def artists(self):
        # 获取歌手单曲
        pass

    def MV(self):
        # 获取歌手 mv
        pass

    def album(self):
        # 获取歌手专辑
        pass

    def desc(self):
        # 获取歌手描述
        pass

    def detail(self):
        # 获取歌手详情
        pass

    def similar(self):
        # 获取相似歌手
        pass