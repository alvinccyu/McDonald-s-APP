import re
import json
import requests
from datetime import datetime, timedelta


class Coupon:

    def __init__(self, name, redeem_end_datetime):
        self.name = name
        self.redeem_end_datetime = redeem_end_datetime
        self.redeem_end_timecode = (redeem_end_datetime - datetime.now()).days
        self.beautify()

    def __repr__(self):
        return "%sE:%d" % (self.name, self.redeem_end_timecode)

    def beautify(self):
        self.name = re.sub(r'鷄', '雞', self.name)
        self.name = re.sub(r'\(G.*\)|\(S.*\)|_.*|\(新.*', '', self.name)


class McDailyAccount:

    def __init__(self, token):
        self.__json = {
            "access_token" : token,
            "source_info"  : {
                "app_version" : "2.2.0",
                "device_time" : "2019/01/01 00:00:00",
                "device_uuid" : "device_uuid",
                "model_id"    : "Pixel XL",
                "os_version"  : "7.1.1",
                "platform"    : "Android",
            }
        }

    def lottery_get_item(self):
        """ Get lottery """
        respones = json.loads(requests.post('https://api1.mcddailyapp.com/lottery/get_item', json = self.__json).text)
        if respones['rc'] != 1:
            print('rc : %d , rm : %s' % (respones['rc'], respones['rm']))

    def coupon_get_list(self):
        """ Get coupon list """
        coupon_list = []
        respones = json.loads(requests.post('https://api1.mcddailyapp.com/coupon/get_list', json = self.__json).text)

        # Make sure the coupons are not used and expired
        for coupon in respones['results']['coupons']:
            coupon_name = coupon['object_info']['title']
            status = coupon['status']
            redeem_end_datetime = datetime.strptime(coupon['object_info']['redeem_end_datetime'], '%Y/%m/%d %H:%M:%S')

            # status equal to 1 means not used
            if status == 1 and redeem_end_datetime - datetime.now() > timedelta():
                coupon_list.append(Coupon(coupon_name, redeem_end_datetime))

        return coupon_list

    def sticker_get_list(self):
        """ Get sticker list but return number of stickers """
        stickers = 0
        expire_this_month_stickers = 0
        respones = json.loads(requests.post('https://api1.mcddailyapp.com/sticker/get_list', json = self.__json).text)

        # Make sure the stickers are not expired
        for sticker in respones['results']['stickers']:
            stickers += 1
            expire_datetime = datetime.strptime(sticker['object_info']['expire_datetime'], '%Y/%m/%d %H:%M:%S')
            if expire_datetime.month == datetime.now().month:
                expire_this_month_stickers += 1

        return stickers, expire_this_month_stickers

    def sticker_redeem(self):
        """ Pay by six stickers to get a coupon lottery """
        respones = json.loads(requests.post('https://api1.mcddailyapp.com/sticker/get_list', json = self.__json).text)
        if len(respones['results']['stickers']) < 6:
            return 'Just %d stickers' % len(respones['results']['stickers'])

        sticker_id_list = []
        for i in range(6):
            sticker_id_list.append(respones['results']['stickers'][i]['sticker_id'])

        self.__json['sticker_ids'] = sticker_id_list
        respones = json.loads(requests.post('https://api1.mcddailyapp.com/sticker/redeem', json = self.__json).text)
        return respones['results']['coupon']['object_info']['title']
