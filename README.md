# 教程
## 创建
> PyNcm提供了两种使用方式

1. 独立使用
项目的`ncm`文件夹提供了Python的NetCloudMusicApi接口,可以直接在Python程序中`import ncm`来使用接口操作,如果你决定独立使用ncm接口,那么可以不用看下面的内容.
2. 结合插件管理器和事件响应器启动
项目的`plugins`文件夹存放自定义插件,你可以编写自己的插件放入其中.运行主文件夹的`main.py`文件即可启动PyNcm.
## 插件
项目基于事件响应器和插件管理员运行.在`main.py`中,你需要管理响应器`matchers`和管理器`PluginManager`
### 加载插件
```python
from plugin import PluginManager
from matcher import matchers

ncm = PluginManager()

# load plugins

matchers.run()
```
插件管理器提供了`PluginManager.load_plugins()`的方法加载`plugins`文件夹下所有的插件.
### 插件配置
你发布的插件中必须含有配置项`__plugin__`和插件名字`__name__`,否则将会报错.
```python

__name__ = '...'
__plugin__ = Plugin(
    name='...',
    description='...',
    usage='..',
    config={
    }
)
```
### 事件响应器
事件响应器（`Matcher`）对接收到的事件进行响应，当检测匹配事件时触发响应器.
在$PyNcm$项目中内置了NetCloudMusic Nodejs作为插件,当项目启动后$NcmApi$插件运行.如果你的插件需要依赖Ncm接口(基本都需要),那么你需要等待$NcmApi$插件启动成功后,再对接口进行操作.
```python
from matcher import on_api

apiRun = on_api(mode=True)
```
上述操作实现了注册事件响应器的操作.你需要先对一个事件注册响应器,之后再添加响应函数(需要异步).
```python

@apiRun.handle(priority=1)
async def _(event):
	...
```
使用装饰器的方式添加响应函数,并且可以对函数添加优先级,高优先级的函数将被率先执行, 异步的执行函数同时需要参数`event`来接受事件传来的消息.
## Ncm接口
`ncm`文件夹对外提供了$CloudMusicApi$这一对象,你可以通过其使用$Api$,$CloudMusic.user$类封装了需要登陆才能使用的$api$方法,第一次使用需要调用`login()`函数通过二维码登陆.$CloudMusic.kit$类封装了不需要登陆的$Api$方法.
# 其他
本项目参照了$Nonebot2$,事件响应和插件管理都是仿照其实现.$plugins$文件夹中存放了范例$网易云自动刷歌$