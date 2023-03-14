from loguru import logger
from pathlib import Path
from ncm.account.cloud import Cloud
from ncm.account.login import *
from ncm.models.accountModel import *
from ncm.utils.tools import *
from ncm.drivers.reqDriver import RequestHandler


class UserBase:
    def __init__(self):
        self._ws = RequestHandler()
        self._info: Account = None
        self._cloud: Cloud = None
        self._isLog: bool = False
        self._loadCookie()

    def init(self):
        try:
            self._info = self.account()
        except:
            logger.warning('Can not connect to nodejs service')

    @property
    def isLogged(self):
        return self._isLog

    def _loadCookie(self, cookie=''):
        try:
            if cookie:
                self._cookie = cookie
            else:
                self._cookie = cookieReader(Path(__file__).parent / 'assets/cookies.txt')
            self._ws.set(self._cookie)
            self._isLog = True
        except Exception as e:
            logger.warning('Can not read the default cookie, Please Login')

    def login(self, method=loginMethod.CodeLogin, **kwargs):
        relation = {
            loginMethod.CodeLogin: codeLogin,
            loginMethod.EmailLogin: epLogin,
            loginMethod.PhoneLogin: ppLogin,
            loginMethod.AnonimousLogin: anonLogin
        }
        res = relation[method](self._ws).send(**kwargs)
        self._loadCookie(res)
        if not res:
            logger.error('Failed in login ncm')

    def logout(self):
        # 退出登录
        self._ws.get('/login/refresh')

    def refresh(self):
        # 刷新登陆
        self._ws.get('/login/refresh')

    @property
    def level(self):
        # 等级
        res = self._ws.get('/user/level')
        return res.json()['data']['level']

    def detail(self, uid):
        res = self._ws.get(f'/user/detail?uid={uid}')
        return res.json()

    def status(self):
        # 用户信息
        res = self._ws.get('/login/status')
        return Profile(res.json())

    def account(self):
        # 账户信息
        res = self._ws.get('/user/account')
        return Account(res.json())

    def updateUser(self, gender, birthday, nickname, provine, city, signature):
        # 更新信息
        param = {
            'gender': genderEnum[gender],
            'birthday': time.mktime(time.strptime(birthday, '%Y-%m-%d')),
            'nickname': nickname,
            'province': provine,
            'city': city,
            'signature': signature
        }
        self._ws.get('/user/update', params=param)

    @property
    def subcount(self):
        # 获取用户信息, 歌单，收藏，mv, dj
        res = self._ws.get('/user/subcount')
        return Subcount(res.json())

    def getRadioStation(self):
        # 获取用户电台
        pass

    def getHistoricalRemark(self):
        # 获取用户历史评论
        pass

    def getFollowList(self):
        # 获取用户关注列表
        pass

    def getFanList(self):
        # 获取用户粉丝列表
        pass

    def getSubscriberEvent(self):
        # 获取用户动态
        pass

    def getPlaylist(self, uid):
        # 获取用户歌单
        res = self._ws.get(f'/user/playlist?uid={uid}').json()
        return res

    def updatePlaylist(self):
        # 更新用户歌单
        pass

    def updatePlaylistDescription(self):
        # 更新歌单描述
        pass

    def updatePlaylistName(self):
        # 更新歌单名
        pass

    def updatePlaylistTag(self):
        # 更新歌单标签
        pass

    def adjustPlaylistOrder(self):
        # 调整歌曲顺序
        pass

    def forwardEvent(self):
        # 转发用户动态
        pass

    def delEvent(self):
        # 删除用户动态
        pass

    def share(self):
        # 分享文本、歌曲、歌单、mv、电台、电台节目到动态
        pass

    def getEventRemark(self):
        # 获取动态评论
        pass

    def follow(self):
        # 关注 / 取消关注用户
        pass

    def getRecord(self):
        # 获取用户播放记录
        pass

    def hotwall(self):
        # 云村热评(官方下架, 暂不能用)
        pass

    def typeArtist(self):
        # 歌手分类列表
        pass

    def subList(self):
        # 收藏的歌手列表
        pass

    def subTopic(self):
        # 收藏的专栏
        pass

    def subVideo(self):
        # 收藏视频
        pass

    def subMV(self):
        # 收藏 / 取消收藏MV
        pass

    def subMVlist(self):
        # 收藏的MV列表
        pass

    def getPlaylistDetail(self):
        # 获取歌单详情
        pass

    def createPlaylist(self):
        # 新建歌单
        pass

    def delPlaylist(self):
        # 删除歌单
        pass

    def subscribePlaylist(self):
        # 收藏 / 取消收藏歌单
        pass

    def operatePlaylist(self):
        # 对歌单添加或删除歌曲
        pass

    def addPlaylistTrack(self):
        # 收藏视频到视频歌单
        pass

    def delPlaylistTrack(self):
        # 删除视频歌单视频
        pass

    def recentVideo(self):
        # 最近播放的视频
        pass

    def likeComment(self):
        # 给评论点赞
        pass

    def hugComment(self):
        # 抱一抱评论
        pass

    def operateComment(self):
        # 发送 / 删除评论
        pass

    def recmSong(self):
        res = self._ws.get('/recommend/songs').json()
        print(res)

    def recmResource(self):
        # 日推歌单
        res = self._ws.get('/recommend/resource').json()
        return res['recommend']

    def historyRecommendList(self):
        # 获取历史日推可用日期列表
        pass

    def historyRecommend(self):
        # 获取历史日推详情数据
        pass

    def personalFM(self):
        # 私人fm
        pass

    def signin(self, type=0):
        # 签到
        # type 签到类型 , 默认 0, 其中 0 为安卓端签到 ,1 为 web/PC 签到
        res = self._ws.get(f"/daily_signin?type={type}").json()
        return res['code'] == 200

    def like(self):
        # 喜欢音乐
        pass

    def likeList(self):
        # 喜欢音乐列表
        res = self._ws.get('/likelist').json()
        return res['ids']

    def trashFM(self):
        # 垃圾桶
        pass

    def newAlbum(self):
        # 全部新碟
        pass

    def scrobble(self, id, pid, time):
        # 听歌打卡
        res = self._ws.get(f'/scrobble?id={id}&sourceid={pid}&time={time}').json()
        return res['data'] == 'success'

    def recmMV(self):
        # 推荐mv
        pass

    def recmPlaylist(self):
        # 推荐歌单
        pass

    def recmNewsong(self):
        # 推荐新音乐
        pass

    def recmDJ(self):
        # 推荐电台
        pass

    def recmProgram(self):
        # 推荐节目
        pass

    def recmVideo(self):
        # 推荐视频
        pass

    def precmDJ(self):
        # 电台个性推荐
        pass

    # 电台

    def privateMsg(self):
        # 通知 - 私信
        pass

    def sendMsg(self):
        # 发送私信
        pass

    def sendMusicmsg(self):
        # 发送私信(带歌曲)
        pass

    def sendAlbummsg(self):
        # 发送私信(带专辑)
        pass

    def sendPlaylistmsg(self):
        # 发送私信(带歌单)
        pass

    def recentcontact(self):
        # 最近联系人
        pass

    def msgContent(self):
        # 私信内容
        pass

    def msgComment(self):
        # 通知 - 评论
        pass

    def msg4me(self):
        # 通知 -@我
        pass

    def msgNotice(self):
        # 通知 - 通知
        pass

    def setting(self):
        # 设置
        pass

    def digitalAlbum(self):
        # 我的数字专辑
        pass

    def orderAlbum(self):
        # 购买数字专辑
        pass

    def calendar(self):
        # 音乐日历
        pass

    # 云贝

    def heartPlay(self, id, pid):
        res = self._ws.get(f'/playmode/intelligence/list?id={id}&pid={pid}').json()
        return res['data']
