import json
import time

import bot_config

from basic.database_wrapper_redis import DatabaseWrapperRedis
from basic.module import Module
from modules.nalida_classic_second import emorec

class EmorecExtracter:
    def __init__(self):
        self.DB = DatabaseWrapperRedis( #pylint: disable=invalid-name
            host=bot_config.DB_HOST, port=bot_config.DB_PORT,
            db=bot_config.DB_NUM, namespace='modules.nalida_classic_third.module'
            )
        self.EMOREC_RESPONSES = 'key-emorec-response:%s'
        self.REGISTERED_USERS = 'user-registered-users'
        self.USER_NICKNAME = 'user-key-nickname:%s'

    @staticmethod
    def localtime_to_formatted(ct):
        formatted = "%d월 %d일 %s %d시 %d분"
        args = (
            ct.tm_mon,
            ct.tm_mday,
            '오후' if ct.tm_hour >= 12 else '오전',
            ct.tm_hour-12 if ct.tm_hour >= 12 else 12 if ct.tm_hour == 0 else ct.tm_hour,
            ct.tm_min
            )
        return formatted % args

    def extract_data(self):
        emorec_data = {}
        for serialized in self.DB.smembers(self.REGISTERED_USERS):
            records = list(map(json.loads, self.DB.lrange(self.EMOREC_RESPONSES % serialized, 0, -1)))
            if len(records) == 0:
                continue
            records.reverse()
            nickname = self.DB.get(self.USER_NICKNAME % serialized)
            context = Module.parse_context(serialized)
            identifier = '%s(%s)' % (nickname, context["chat_id"])
            emorec_data[identifier] = []

            for record in records:
                d_time = float(record[0])
                d_localtime = time.localtime(d_time)
                d_emotion = record[1]
                d_detail = ''
                if len(record) > 2:
                    d_detail = record[2].replace('\n', ' ')

                elem = {"date": d_time}
                elem["date_f"] = self.localtime_to_formatted(d_localtime)
                elem["cont"] = d_emotion
                elem["cont_i"] = emorec.EMOTIONS.index(d_emotion)
                elem["detail"] = d_detail

                emorec_data[identifier].append(elem)
        return emorec_data
