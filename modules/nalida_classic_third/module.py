"""
Module for Nalida Classic: 2nd
This module contains
    - registration routine
    - interface to the emotion recording module
        & sharing public responses
    - team notification
"""

import logging
import json
import datetime
import random
import time


from modules.nalida_classic_third import string_resources as sr
from modules.nalida_classic_third import emorec
from modules.nalida_classic_third.user import User
from modules.nalida_classic_third.session import Session
from basic.module import Module

import bot_config

class ModuleNalidaClassicThird(Module):
    "Module description above"
    def __init__(self):
        super().__init__(__name__)
        self.user = User(self)
        self.session = Session(self)
        self.key = {
            "list_emorec_response": 'key-emorec-response:%s',
            }

    def send_text(self, context, text):
        for subtext in text.split('$$$'):
            super().send_text(context, subtext)

    def send_to_monitoring(self, text):
        "send the text to monitoring room"
        self.send_text({"chat_id": bot_config.NALIDA_CLASSIC_THIRD_MONITORING}, text)

    def filter(self, message):
        context = message["context"]
        return any((
            context["chat_id"] == bot_config.NALIDA_CLASSIC_THIRD_ADMIN,
            message["type"] == 'text' and \
                message["data"]["text"].startswith(sr.COMMAND_PREFIX_REGISTER_BROADCASTING_ROOM),
            self.user.membership_test(context),
            message["type"] == 'text' and self.user.is_registration_key(message["data"]["text"]),
            message["type"] == 'timer',
            ))

    def state_asked_nick(self, message):
        "response should be their wanted nickname"
        context = message["context"]
        if message["type"] == 'text':
            text = message["data"]["text"]
            self.send_text(context, sr.CONFIRM_NICKNAME % text)
            serialized = self.serialize_context(context)
            self.db.set('candidate-nickname:%s' % serialized, text)
            self.user.state(context, 'asked_nick_confirmation')
        else:
            self.send_text(context, sr.WRONG_RESPONSE_FORMAT)

    def state_asked_nick_confirmation(self, message):
        """response should be YES or NO depending on whether the nickname is
           submitted correctly"""
        context = message["context"]
        if message["type"] == 'text':
            text = message["data"]["text"]
            if text == sr.RESPONSE_NICKNAME_YES:
                serialized = self.serialize_context(context)
                nickname = self.db.get('candidate-nickname:%s' % serialized)
                self.user.nick(context, nickname)
                self.send_to_monitoring(sr.REPORT_NICKNAME % (serialized, nickname))
                self.send_to_monitoring(sr.HELP_MESSAGE_BROADCASTING_ROOM_REGKEY %
                                        (nickname, serialized))
                self.send_text(context, sr.NICKNAME_SUBMITTED % nickname)
                self.send_text(context, sr.ASK_EXPLANATION_FOR_NICKNAME)
                self.user.state(context, 'asked_nick_explanation')
            elif text == sr.RESPONSE_NICKNAME_NO:
                self.send_text(context, sr.ASK_NICKNAME_AGAIN)
                self.user.state(context, 'asked_nick')
            else:
                self.send_text(context, sr.WRONG_RESPONSE_FORMAT)
        else:
            self.send_text(context, sr.WRONG_RESPONSE_FORMAT)

    def state_asked_nick_explanation(self, message):
        "response should be the explanation in one message"
        context = message["context"]
        if message["type"] == 'text':
            text = message["data"]["text"]
            self.user.explanation(context, text)
            nickname = self.user.nick(context)
            self.send_to_monitoring(sr.REPORT_EXPLANATION % (nickname, text))
            self.send_text(context, sr.EXPLANATION_SUBMITTED)
            self.send_text(context, sr.INSTRUCTIONS_FOR_EMOREC)
            self.user.emorec_time(context, True)
            self.user.state(context, '')
        else:
            self.send_text(context, sr.WRONG_RESPONSE_FORMAT)

    def record_emorec_response(self, message):
        "record emorec response and share it"
        context = message["context"]
        key = self.key["list_emorec_response"] % self.serialize_context(context)
        text = message["data"]["text"]
        self.db.lpush(key, json.dumps([time.time(), text, '']))
        reactive_sentence = emorec.REPLYS[emorec.EMOTIONS.index(text)]
        self.send_text(context, reactive_sentence)

        nickname = self.user.nick(context)
        self.send_to_monitoring(sr.REPORT_EMOREC_SHARING % (nickname, text))

    def emorec_get_associated_records(self, context, current_time): #TODO O(N)
        key = self.key["list_emorec_response"] % self.serialize_context(context)
        records = self.db.lrange(key, 0, -1)
        records = [json.loads(record) for record in records if record != "None" and record is not None]
        records.reverse()
        associated_records = [record[1] for record in records if
            current_time - record[0] <= 24 * 3600]
        return associated_records

    def state_asked_emotion_detail(self, message):
        "record emotion response detail"
        context = message["context"]
        if message["type"] == 'text':
            key = self.key["list_emorec_response"] % self.serialize_context(context)
            text = message["data"]["text"]
            share = True
            if text.startswith(sr.COMMAND_NOT_TO_SHARE_EMOTION):
                text = text[len(sr.COMMAND_NOT_TO_SHARE_EMOTION):].strip()
                share = False
            recent_response = self.db.lpop(key)
            if recent_response is None: # this if-clause exists for the bug during beta-testing
                return
            recent_response = json.loads(recent_response)
            recent_response[2] = text
            self.db.lpush(key, json.dumps(recent_response))
            nickname = self.user.nick(context)
            self.send_to_monitoring(sr.REPORT_EMOREC_DETAIL % (nickname, text))
            if share and self.user.session(context) is not None:
                associated_records = self.emorec_get_associated_records(context, time.time())
                associated_record_message = '\n'.join(associated_records)
                message_to_share = {
                    "type": 'text',
                    "context": None,
                    "data": {
                        "text": sr.EMOREC_SHARING_DETAILED_MESSAGE % (associated_record_message, text)
                        }
                    }
                self.session.share_user_response(context, message_to_share)
                self.send_text(context, sr.EMOREC_RESPONSE_RECORDED_AND_SHARED)
            else:
                self.send_text(context, sr.EMOREC_RESPONSE_RECORDED_BUT_NOT_SHARED)

        self.user.state(context, '')

    def emorec_routine(self, message):
        "check if it has to ask emotions for some user"
        current = json.loads(message["data"]["time"])
        hour, minute = map(int, current[3:5])
        datetime_now = datetime.datetime(100, 1, 1, hour, minute, 0)
        for context in self.user.list_of_users():
            when, b_hour, b_minute = self.user.emorec_time(context)
            if b_hour == -1:
                continue
            datetime_baseline = datetime.datetime(100, 1, 1, b_hour, b_minute, 0)
            elapsed_time = (datetime_now - datetime_baseline).seconds
            if datetime_baseline <= datetime_now and elapsed_time <= 180:
                if when != 'night':
                    self.user.state(context, '')
                    self.send({
                        "type": 'markup_text',
                        "context": context,
                        "data": {
                            "text": sr.ASK_EMOTION,
                            "reply_markup": emorec.KEYBOARD,
                            }
                        })
                else:
                    self.send_text(context, sr.ASK_EMOTION_DETAIL)
                    self.user.state(context, 'asked_emotion_detail')
                self.user.emorec_time(context, True)

    def execute_admin_command(self, message):
        "executes commands entered in the admin room"
        try:
            context = message["context"]
            if message["type"] == 'text':
                text = message["data"]["text"]
                args = text.split()
                if text == sr.COMMAND_PUBLISH_REGISTRATION_KEY:
                    self.send_text(context, self.user.generate_new_registration_key())
                elif args[0] == sr.COMMAND_MAKE_SESSION:
                    nicks = args[1:]
                    target_contexts = []
                    for nick in nicks:
                        for target_context in self.user.list_of_users():
                            if self.user.nick(target_context) == nick:
                                target_contexts.append(target_context)
                    if len(target_contexts) != len(nicks):
                        self.send_text(context, sr.ERROR_MAKE_SESSION_INVALID_CONTEXT)
                        return
                    if not all(map(self.user.membership_test, target_contexts)):
                        self.send_text(context, sr.ERROR_MAKE_SESSION_INVALID_CONTEXT)
                        return
                    for target_context in target_contexts:
                        if self.user.target_chat(target_context) is None:
                            self.send_text(context, sr.ERROR_MAKE_SESSION_NO_TARGET_CHAT %
                                           self.user.nick(target_context))
                            return
                    session_name = self.session.create(target_contexts)
                    self.send_text(context, 'created session: %s' % session_name)
                elif args[0] == sr.COMMAND_NOTICE:
                    ind = text.find(':')
                    nicks = text[:ind].split()[1:]
                    content = text[ind+1:].strip()
                    target_contexts = []
                    for nick in nicks:
                        for target_context in self.user.list_of_users():
                            if self.user.nick(target_context) == nick:
                                target_contexts.append(target_context)
                                break
                    if len(nicks) != len(target_contexts):
                        self.send_text(context, sr.ERROR_NOTICE_INVALID_CONTEXT)
                        return
                    for target_context in target_contexts:
                        self.send_text(target_context, content)
                    self.send_text(context, sr.REPORT_NOTICE_COMPLETE)
                elif args[0] == sr.COMMAND_GET_EMOREC_TIME:
                    for target_context in self.user.list_of_users():
                        if self.user.nick(target_context) == args[1]:
                            self.send_text(context, '%r' % self.user.emorec_time(target_context))
                elif args[0] == sr.COMMAND_NEXT_EMOREC_TIME:
                    for target_context in self.user.list_of_users():
                        if self.user.nick(target_context) == args[1]:
                            self.user.emorec_time(target_context, True)
                            self.send_text(context, '%r' % self.user.emorec_time(target_context))
                elif args[0] == sr.COMMAND_FAKE_TIMER:
                    year, month, day, hour, minute, second = map(int, args[1:7])
                    fake_time = datetime.datetime(year, month, day, hour, minute, second).timetuple()
                    fake_message = {
                        "type": "timer",
                        "context": {"chat_id": -1, "author_id": -1},
                        "data": {"time": json.dumps(fake_time)}
                    }
                    self.operator(fake_message)
                elif args[0] == sr.COMMAND_LIST_USERS:
                    self.send_text(context, '\n'.join(
                        ['[%s] %s' % (self.user.nick(target_context), self.serialize_context(target_context))
                            for target_context in self.user.list_of_users()]
                        )
                    )
                elif args[0] == sr.COMMAND_DELETE_USER:
                    serialized = args[1]
                    self.user.delete_user(self.parse_context(serialized))
                    

        except Exception as exception: #pylint: disable=broad-except
            self.send_text({"chat_id": bot_config.NALIDA_CLASSIC_THIRD_ADMIN},
                           '에러가 발생했습니다: %s' % str(exception))

    def execute_user_command(self, message):
        "executes commands entered in user's chat"
        context = message["context"]
        state = self.user.state(context)
        if emorec.is_emorec_response(message):
            self.record_emorec_response(message)
        elif state is not None:
            getattr(self, 'state_' + state)(message)
        else:
            self.send_text(context, random.choice(sr.CAT_MEOWS))

    def operator(self, message):
        context = message["context"]
        if context["chat_id"] == bot_config.NALIDA_CLASSIC_THIRD_ADMIN:
            self.execute_admin_command(message)
        elif message["type"] == 'text' and \
                message["data"]["text"].startswith(sr.COMMAND_PREFIX_REGISTER_BROADCASTING_ROOM):
            text = message["data"]["text"]
            comm = sr.COMMAND_PREFIX_REGISTER_BROADCASTING_ROOM
            text = text[len(comm):].strip()
            context = self.parse_context(text)
            self.user.target_chat(context, self.serialize_context(message["context"]))
            self.send_text(message["context"],
                           sr.REGISTERED_AS_BROADCASTING_ROOM % self.user.nick(context))

        elif self.user.membership_test(context):
            self.execute_user_command(message)

        elif message["type"] == 'text' and self.user.is_registration_key(message["data"]["text"]):
            self.user.register_user(context, message["data"]["text"])
            self.send_text(context, sr.REGISTER_COMPLETE)
            self.send_text(context, sr.ASK_NICKNAME)
            self.user.state(context, 'asked_nick')
        elif message["type"] == 'timer':
            self.emorec_routine(message)

        else:
            logging.error('This clause should never be executed!')
