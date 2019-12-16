import json
import hashlib
import requests
from datetime import datetime


class Mask:

    def __init__(self, username, password, card_no = None):
        self.param_string = username + password                            # username + password
        self.username = username                                           # Username
        self.password = password                                           # Password
        self.access_token = ''                                             # Token
        self.str1 = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S') # Device Time
        self.str2 = '2.2.0'                                                # App Version
        self.str3 = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')      # Call time
        self.model_id = 'MIX 3'                                            # Model ID
        self.os_version = '9'                                              # Android OS Version
        self.platform = 'Android'                                          # platform
        self.device_uuid = 'device_uuid'                                   # Device Uuid
        self.order_no = self.device_uuid + self.str3                       # Order No
        self.card_no = card_no                                             # Card No

    def login(self):
        """ Mask = md5('Mc' + order_no + platform + os_version + model_id + device_uuid + str1 + str2 + param_string + 'Donalds') """
        data = 'Mc%s%s%s%s%s%s%s%sDonalds' % (
            self.order_no,
            self.platform,
            self.os_version,
            self.model_id,
            self.device_uuid,
            self.str1,
            self.str2,
            self.param_string
        )
        mask = hashlib.md5()
        mask.update(data.encode('utf-8'))

        # Form data
        __json = {
            "account"     : self.username,
            "password"    : self.password,
            "OrderNo"     : self.order_no,
            "mask"        : mask.hexdigest(),
            "source_info" : {
                "app_version" : self.str2,
                "device_time" : self.str1,
                "device_uuid" : self.device_uuid,
                "model_id"    : self.model_id,
                "os_version"  : self.os_version,
                "Platform"    : self.platform,
            }
        }

        response = json.loads(requests.post('https://api.mcddaily.com.tw/login_by_mobile', json = __json).text)
        self.access_token =  response['results']['member_info']['access_token']

        return response

    def get_card_query(self):
        """ Mask = md5('Mc' + order_no + access_token + card_no + callTime + 'Donalds') """
        data = 'Mc%s%s%s%sDonalds' % (
            self.order_no,
            self.access_token,
            self.card_no,
            self.str3,
        )
        mask = hashlib.md5()
        mask.update(data.encode('utf-8'))

        # From data
        __json = {
            "OrderNo"      : self.order_no,
            "access_token" : self.access_token,
            "callTime"     : self.str3,
            "cardNo"       : self.card_no,
            "mask"         : mask.hexdigest(),
        }

        return json.loads(requests.post('https://api.mcddaily.com.tw/queryBonus', json = __json).text)
