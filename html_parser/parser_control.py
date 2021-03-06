# encoding=utf8
import sys
sys.path.append("..")

import threading
import time
import utils.tools as tools
import base.constance as Constance
from html_parser.parsers import *
from base.collector import Collector
from utils.log import log

db = tools.getConnectedDB()

class  PaserControl(threading.Thread):
    def __init__(self):
        super(PaserControl, self).__init__()
        self._collector = Collector()
        self._urlCount = int(tools.getConfValue("html_parser", "url_count"))
        self._interval = int(tools.getConfValue("html_parser", "sleep_time"))

    def run(self):
        while True:
            try:
                urls = self._collector.getUrls(self._urlCount)
                print("取到的url大小 %d"%len(urls))
                # 判断是否结束
                if self._collector.isFinished():
                    log.debug("-------------- 结束 --------------")
                    break

                for url in urls:
                    self.parseUrl(url)

                time.sleep(self._interval)
            except Exception as e:
                log.debug(urls)
                log.debug(e)

    def parseUrl(self, urlInfo):
        website_id = urlInfo['website_id']

        try:
            domain = list(db.website.find({'_id':website_id}))[0]['domain']

            if domain == Constance.IFENG:
                ifeng.parseUrl(urlInfo)

            elif domain == Constance.SOHU:
                sohu.parseUrl(urlInfo)

            elif domain == Constance.TENCENT:
                tencent.parseUrl(urlInfo)

            elif domain == Constance.SINA:
                #sina.parseUrl(urlInfo)
                pass
            elif domain == Constance.CCTV:
                cctv.parseUrl(urlInfo)

            elif domain == Constance.PEOPLE:
                people.parseUrl(urlInfo)

            elif domain == Constance.WANG_YI:
                wangyi.parseUrl(urlInfo)

            elif domain == Constance.XIN_HUA:
                xinhua.parseUrl(urlInfo)

        except Exception as e:
            log.debug(e)