# -*- coding: utf-8 -*-
import scrapy
import re

class BannedplayerSpider(scrapy.Spider):
    name = 'BannedPlayer'
    start_urls = ['https://www.5ewin.com/banned/']

    def __init__(self, playernumber = 200, *args, **kwargs):
        # 创建错误日志
        self.f = open('path_error.log','w',encoding='utf-8')

        # 初始化爬取人数
        print("the latest " + str(playernumber) + " banned player will be recorded")
        self.player_number = int(playernumber)
        super(BannedplayerSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for i in range(self.player_number):

            # 开始页面核心信息对应的xpath
            table_data_xpath = '/html/body/div[5]/div/table/tbody/tr[%d]/td[1]'%(i+2, )
            name_path = table_data_xpath+'/a'
            icon_xpath = table_data_xpath+'/i'
            steam_id_xpath = '/html/body/div[5]/div/table/tbody/tr[%d]/td[2]/a'%(i+2, )
            reason_xpath = '/html/body/div[5]/div/table/tbody/tr[%d]/td[3]'%(i+2, )
            banned_time_xpath = '/html/body/div[5]/div/table/tbody/tr[%d]/td[4]' % (i+2,)
            release_time_xpath = '/html/body/div[5]/div/table/tbody/tr[%d]/td[5]' % (i+2,)

            # 用户ID
            name = response.xpath(name_path+'/text()').extract()[0]

            # 用户个人页面url（不作为属性出现在数据集中，仅爬虫使用）
            player_link = response.xpath(name_path+'/@href').extract()[0]

            # 用户身份，包含None，Vip和Svip
            player_type = 'None'
            if response.xpath(icon_xpath):
                if response.xpath(icon_xpath+'/@class').extract()[0].strip() == 'icons icon-svip':
                    player_type = 'Svip'
                else:
                    player_type = 'Vip'

            # 用户关联的steam ID
            steam_id = response.xpath(steam_id_xpath+'/text()').extract()[0]

            # 用户被封禁的理由
            reason = response.xpath(reason_xpath+'/text()').extract()[0]

            # 用户被封禁的时间
            banned_time = response.xpath(banned_time_xpath + '/text()').extract()[0]

            # 用户被解封的时间，无限封禁为Inf
            release = response.xpath(release_time_xpath + '/text()').extract()[0]
            if release == '永久封禁':
                release = 'Inf'

            yield scrapy.Request(url=player_link, callback=self.parse_player ,meta={"name":name,
                                                                                    'player_type':player_type,
                                                                                    'steam_id':steam_id,
                                                                                    'reason':reason,
                                                                                    'banned_time':banned_time,
                                                                                    'release':release})

    def parse_player(self,response):
        try:
            # 判断用户类型
            # 由于Svip用户会获得独有的页面设计，因此需要抓取不同的xpath，设计不同的爬虫模式
            if response.meta['player_type'] == 'Svip':

                # 判断封禁类型
                # 最近一场的天梯对战记录
                # latest_match = \
                # response.xpath('/html/body/div[6]/div[2]/div[2]/div[4]/div[2]/div[2]/div[2]/table/t'
                #                'body[2]/tr[1]/td[10]/a[1]/@href').extract()[0]
                # 不同的封禁原因会导致html页面的细微差异，只能根据封禁原因抓取不同的xpath
                if response.meta['reason'] == '作弊封禁':

                    # 被投诉次数
                    complaint_times = \
                    response.xpath('/html/body/div[6]/div[1]/div/div[7]/div[1]/div[4]/span/text()').extract()[0].split( )[1]

                    # 注册日期
                    register_days = \
                    response.xpath('/html/body/div[6]/div[1]/div/div[7]/div[2]/div[2]/p[1]/text()').extract()[0][:-1]

                    # 游戏时长
                    playing_hours = \
                    response.xpath('/html/body/div[6]/div[1]/div/div[7]/div[2]/div[1]/p[1]/text()').extract()[0][:-2]

                    # 最擅长武器
                    best_weapon = 'None'

                    # 最擅长武器爆头率
                    best_weapon_heatshot = 'None'

                    # 最擅长武器爆头率
                    best_map = 'None'
                else:
                    # 被投诉次数
                    complaint_times = \
                    response.xpath('/html/body/div[6]/div[1]/div/div[6]/div[1]/div[4]/span/text()').extract()[0].split()[1]

                    # 注册日期
                    register_days = \
                    response.xpath('/html/body/div[6]/div[1]/div/div[6]/div[2]/div[2]/p[1]/text()').extract()[0][:-1]

                    # 游戏时长
                    playing_hours = \
                    response.xpath('/html/body/div[6]/div[1]/div/div[6]/div[2]/div[1]/p[1]/text()').extract()[0][:-2]

                    # 最擅长武器
                    best_weapon = \
                    response.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[3]/p[1]/text()').extract()[0]

                    # 最擅长武器爆头率
                    best_weapon_heatshot = \
                    response.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div[2]/div[2]/p[1]/text()').extract()[0]

                    # 最擅长地图
                    best_map = \
                    response.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[3]/p[1]/text()').extract()[0]



            else:
                # 非svip用户的界面设计更加混乱，甚至不能用分支来完成，因此我将错误的xpath在异常中处理

                # latest_match = \
                # response.xpath('/html/body/div[8]/div/div[2]/table/tbody/tr[2]/td[12]/a[1]/@href').extract()[0]
                if response.xpath('/html/body/div[5]/div/div[6]/div[2]/span/text()'):
                    complaint_times = \
                        response.xpath('/html/body/div[5]/div/div[6]/div[2]/span/text()').extract()[1].split()[1]
                else:
                    complaint_times = \
                        response.xpath('/html/body/div[5]/div/div[5]/div[2]/span/text()').extract()[1].split()[1]

                register_days = 'None'

                playing_hours = 'None'

                best_weapon = 'None'
                if response.xpath('/html/body/div[7]/div/div[2]/div/ul/li[1]/p/span[1]/text()').extract():
                    best_weapon = \
                    response.xpath('/html/body/div[7]/div/div[2]/div/ul/li[1]/p/span[1]/text()').extract()[0]

                best_weapon_heatshot = 'None'
                if response.xpath('/html/body/div[7]/div/div[2]/div/ul/li[1]/p/span[2]/em[3]/text()').extract():
                    best_weapon_heatshot = \
                    response.xpath('/html/body/div[7]/div/div[2]/div/ul/li[1]/p/span[2]/em[3]/text()').extract()[0][:-4]

                best_map = 'None'
                if response.xpath('/html/body/div[7]/div/div[1]/div/ul/li[1]/div/p[1]/text()'):
                    best_map = \
                    response.xpath('/html/body/div[7]/div/div[1]/div/ul/li[1]/div/p[1]/text()').extract()[0]

            # 创建用户item
            player_dict = {}
            player_dict['name'] = response.meta['name']
            player_dict['player_type'] = response.meta['player_type']
            player_dict['steam_id'] = response.meta['steam_id']
            player_dict['reason'] = response.meta['reason']
            player_dict['banned_time'] = response.meta['banned_time']
            player_dict['release'] = response.meta['release']

            # 将上级页面的信息加入到item
            player_dict.update({
                'complaint_times':complaint_times,
                'register_days':register_days,
                'playing_hours':playing_hours,
                'best_weapon':best_weapon,
                'best_weapon_heatshot':best_weapon_heatshot,
                'best_map':best_map
            })

        except :
            # 对于没有找到正确xpath的用户，其个人页面的url会将被记录在日志当中
            player_dict = {}
            print('***************CAN"T CATCH THE INFORMATION!*****************')
            self.f.write(str(response.url)+'\n')

        yield player_dict

    @staticmethod
    def parse_score(self,response,name):


        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")

        try:
            score = ''
            # 在上面5个玩家数据里面查找该玩家的名字
            for i in range(5):
                name_xpath_side_1 = '/html/body/div[4]/div/div[1]/div[3]/div[2]/table[1]/tr[%d]/td[2]/a/span/text()'%(i+2)
                player_name = response.xpath(name_xpath_side_1).extract()[0]
                if player_name == name:
                    score_xpath = '/html/body/div[4]/div/div[1]/div[3]/div[2]/table[1]/tr[%d]/td[13]//text()'%(i+2)

                    score = cop.sub("", response.xpath(score_xpath).extract()[0])

            # 在上面5个玩家数据里面查找该玩家的名字
            for i in range(5):
                name_xpath_side_2 = '/html/body/div[4]/div/div[1]/div[3]/div[2]/table[2]/tr[%d]/td[2]/a/span/text()'%(i+1)
                player_name = response.xpath(name_xpath_side_2).extract()[0]
                if player_name == name:
                    score_xpath = '/html/body/div[4]/div/div[1]/div[3]/div[2]/table[2]/tr[%d]/td[13]/text()'%(i+1)

                    score = cop.sub("", response.xpath(score_xpath).extract()[0])


        except:
            score = ''

        return score