from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.errors import *
import threading, time, random, statistics
import numpy as np
from lxml import html

class DPTool:
    print('本脚本基于DrissionPage提供API运行\n喜欢本功能请给DrissionPage作者g1879买杯咖啡，支持原作者\nDrissionPage Github: https://github.com/g1879/DrissionPage')
    def __init__(self, data, proxy: str=None, num_threads: int=1, retry_times: int=1, waiting_time: float=2):
        # thread lock
        self.lock = threading.Lock()

        # retry_times
        self.retry_times = retry_times

        # waiting_time
        self.waiting_time = waiting_time

        # proxy
        self.co = ChromiumOptions()
        if proxy:
            self.co.set_proxy(f'http://{proxy}')
        else:
            pass
        
        # browser settings
        self.browser = Chromium(addr_or_opts=self.co)
        
        # create tabs as many as threads
        count = 1
        while count < num_threads:
            self.browser.new_tab()
            count += 1

        # split data into chunks
        self.chunks = np.array_split(np.array(data), num_threads)

        self.results=[]
        self.failed=[]

    def baidu_rank_checker(self, tab, url:str, search_word:str):
        ## 不可用
        fail_count = 0
        page = 0
        trees = []
        while fail_count <= self.retry_times:
            while page <= 5:
                try:
                    ele = tab.ele('@@id=kw')
                    ele.input(search_word+'\n', clear = True)
                    tab.wait.title_change(search_word, raise_err = True)
                    tab.wait.eles_loaded('tag:div@id=wrapper_wrapper', raise_err = True)
                    trees.append(html.fromstring(tab.html))
                    break
                except:
                    fail_count += 1
                    self.browser.clear_cache(cookies=False)
                    tab.get('https://www.baidu.com')

        # if fail_count <= self.retry_times:
        #     ranklist = tree.xpath("//div[@id='content_left' and @tabindex='0']")[0].getchildren()
        #     for item in ranklist:
        #         try:
        #             rank_url = item.attrib['mu']
        #             if url == rank_url:
        #                 return (search_word, url, item.attrib['id'])
        #         except:
        #             pass
        #     return (search_word, url, '前50无匹配')
        # else:
        #     return (search_word, url, '查询失败')

    def baidu_index_checker(self, tab, url: str):
        fail_count = 0
        while fail_count <= self.retry_times:
            try:
                ele = tab.ele('@@id=kw')
                ele.input(url+'\n', clear = True)
                tab.wait.title_change(url, raise_err = True)
                tab.wait.eles_loaded('tag:div@id=wrapper_wrapper', raise_err = True)
                tree = html.fromstring(tab.html)
                break
            except:
                fail_count += 1
                self.browser.clear_cache()
                tab.get('https://www.baidu.com')

        if fail_count <=self.retry_times:
            # all_ranked_urls = tree.xpath("//div[@id='content_left' and @tabindex='0']/div/@mu")
            all_ranked_urls = tree.xpath("//div[@id='content_left' and @tabindex='0']/div")
            for i in all_ranked_urls:
                try:
                    i_url = i.attrib['mu']
                    image = i.xpath(".//img/@src")
                    if url == i_url:
                        if image:
                            return (url, '已收录', '已出图')
                        else:
                            return (url, '已收录', '未出图')
                except:
                    pass
            return (url, '未收录', '未出图')
        else:
            return None
        
    def distributor(self, tab_id: str, chunk):
        tab = self.browser.get_tab(tab_id)
        waiting_times = statistics.NormalDist(self.waiting_time, 0.125).samples(len(chunk))
        waiting_times = [x+random.uniform(0,0.5) for x in waiting_times]
        successed = list()
        failed = list()
        if len(chunk[0]) != 2:
            for index, item in enumerate(chunk):
                temp = self.baidu_index_checker(tab, url=item)
                if temp == None:
                    failed.append(item)
                else:
                    successed.append(temp)
                time.sleep(waiting_times[index])
        else:
            for index, item in enumerate(chunk):
                temp = self.baidu_rank_checker(tab, url=item[1], search_word=item[0])
                if temp[2] == '查询失败':
                    failed.append(item)
                else:
                    successed.append(temp)
                time.sleep(waiting_times[index])
        with self.lock:
            self.results.append(successed)
            self.failed.append(failed)
            print(f"网页{tab_id}: 已完成")

    def threads_processor(self):
        threads = []

        for index, tab in enumerate(self.browser.get_tabs()):
            if self.chunks[index].size != 0:
                tab.get('https://www.baidu.com')
                threads.append(threading.Thread(target=self.distributor, args=(tab.tab_id, self.chunks[index])))
                threads[-1].start()

        for thread in threads:
            thread.join()
        