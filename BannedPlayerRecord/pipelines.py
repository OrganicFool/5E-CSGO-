# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd


class BannedplayerrecordPipeline(object):
    def process_item(self, item, spider):
        return item


class BannedplayerCSVPipeline(object):
    def __init__(self):
        # 创建数据集
        self.dataframe = pd.DataFrame()

    def process_item(self,item,spider):
        # 将每一代得到的数据更新至数据集
        item = dict(item)
        keyset = item.keys()
        for key in keyset:
            item[key] = [item[key]]
        self.dataframe = pd.concat([self.dataframe,pd.DataFrame(item)])

        return item

    def close_spider(self,spider):
        # 以csv格式存储，并记录爬取的用户数
        self.dataframe.to_csv(('latest '+str(spider.player_number)+' banned players info.csv'), index=0, encoding='utf_8_sig')
        spider.f.close()
