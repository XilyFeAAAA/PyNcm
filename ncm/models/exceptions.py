class NoPlaylistError(Exception):
    """未找到的歌单"""
    def __str__(self):
        print("playlist can not be found")