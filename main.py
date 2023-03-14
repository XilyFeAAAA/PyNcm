# 入口
from matcher import matchers
from plugin import *
from pathlib import Path

ncm = PluginManager()
ncm.init()
ncm.load_plugins()


if __name__ == "__main__":
    matchers.run()