from pathlib import Path
import os

class CommonConfig():
    ID2LABEL = {
        0: 'dokujo-tsushin', 
        1: 'it-life-hack', 
        2: 'smax', 
        3: 'sports-watch', 
        4: 'kaden-channel', 
        5: 'movie-enter', 
        6: 'topic-news', 
        7: 'livedoor-homme', 
        8: 'peachy'
    }

class DevConfig(CommonConfig):
    DEBUG = True

class ProdConfig(CommonConfig):
    DEBUG = False