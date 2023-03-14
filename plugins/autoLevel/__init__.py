import random
import time
import asyncio
from threading import Thread
from ncm import CloudMusicApi
from ncm.models.accountModel import *
from plugin import Plugin
from matcher import *

__name__ = "网易云自动刷歌"
__plugin__ = Plugin(
    name='Ncm automatic listen',
    description='',
    usage='',
    config=None
)

# 实例化ncm对象
ncm = CloudMusicApi()
# 注册事件

apiRun = on_api(mode=True, plugin=__plugin__)

# 没有cookie则登陆
if not ncm.user.isLogged:
    ncm.user.login()


# ===========配置========================
p = 25
UID = ''  # 网易云uid
count = 0
number = 300  # 听歌次数
playMode = 0  # 日推、心动模式
delay = 0.1
sid = -1
tlist = []

# =======================================
def Play(id):
    global count, sid
    if count != number:
        try:
            count += 1
            playTime = random.randint(90, 120)
            ncm.user.scrobble(id, sid, playTime)
            print(f"ID->{id} -- OK!")
            print(f"count->{count}")
        except:
            pass
    else:
        return


def startPlay(data):
    global delay, tlist
    try:
        for id in data:
            id = id["id"]
            t = Thread(target=Play, args=(id,))
            t.start()
            tlist.append(t)
            time.sleep(delay)
        for t in tlist:
            t.join()
    except:
        print("[ERR]账号可能被封控，请重试")


def startPlay2():
    sidList = []  # 歌单id
    source_ids = ncm.user.recmResource()
    for ids in source_ids:
        sid = ids["id"]
        sidList.append(
            ncm.kit.playlist.Playlist(sid))
        print("推荐歌单->", sid, "已加入播放列表!")
    limit = number / len(sidList)
    musicIdsList = []
    for sid in sidList:
        try:
            musicList = sid.getTrack(limit)
            for id in musicList["privileges"]:
                print(f"获取到音乐: {id['id']}")
                musicIdsList.append(id["id"])
        except:
            print("[ERR] 忽略了一个歌单数据 : 无法解析")
    print("总歌曲数量:", len(musicIdsList), "开始播放(mode2)")
    tlist = []
    for id in musicIdsList:
        t1 = Thread(target=Play, args=(id,))
        t1.start()
        tlist.append(t1)
        time.sleep(0.1)
    for t in tlist:
        t.join()

"""注册api打开事件"""
@apiRun.handle(priority=1)
async def start(event):
    global sid, p, playMode, ncm
    uid = ''
    count = 0  # 记录听歌量
    ThreadList = []  # 储存所有线程
    ncm.user.init()
    if not UID:
        try:
            res: Account = ncm.user.account()
            uid = res.id
        except Exception as e:
            print("[ERR] 未能正确获取到UID，请重新登陆")
            return
    else:
        uid = UID
    print(f"用户UID: {uid}")
    try:
        res = ncm.user.detail(uid)
        nickname = res['profile']['nickname']
    except:
        print("[ERR] 未能正确获取到用户名，请重新登陆")
        return
    print("用户昵称:", nickname)
    ncm.user.signin()
    if playMode == 0:
        data_ids = ncm.user.likeList()
        sid = ncm.user.lovedPlaylist
        if sid == -1:
            print('[ERR]歌单获取错误')
            return
        for i in range(p):
            try:
                playlist = ncm.user.heartPlay(data_ids[i], sid)
                startPlay(playlist)
                time.sleep(0.1)
            except:
                print("[ERR] 数据获取失败，正在重新请求并解析数据")
                continue
    elif playMode == 1:
        startPlay2()
    else:
        print("[ERR] 请检查PlayMode是否正确")
        exit()
    print("本次任务已完成!")
