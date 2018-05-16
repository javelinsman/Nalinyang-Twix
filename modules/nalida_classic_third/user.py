"manages user informations for nalida classic 2nd"

import logging
import json
import random
import string
import time

from basic.module import Module

class User:
    "mainly about getters and setters"
    def __init__(self, parent):
        self.db = parent.db #pylint: disable=invalid-name
        self.key = {
            "nickname": 'user-key-nickname:%s',
            "goal_name": 'user-goal-name:%s',
            "goal_description": 'user-goal-description:%s',
            "explanation": 'user-explanation:%s',
            "session": 'user-session:%s',
            "state": 'user-state:%s',
            "emorec_time": 'user-emorec-time:%s',
            "registered_users": 'user-registered-users',
            "registration_keys": 'user-registration-keys',
            "target_chat": 'user-target-chat:%s',
            }

    def membership_test(self, context):
        "check if the context is registered for this module"
        return self.db.sismember(self.key["registered_users"], Module.serialize_context(context))

    def register_user(self, context, registration_key):
        "register the context as a user of this module"
        self.db.sadd(self.key["registered_users"], Module.serialize_context(context))
        self.db.srem(self.key["registration_keys"], registration_key)

    def delete_user(self, context):
        self.db.srem(self.key["registered_users"], Module.serialize_context(context))

    def list_of_users(self):
        "returns the list of registrated users"
        users = self.db.smembers(self.key["registered_users"])
        return list(map(Module.parse_context, users))

    def generate_new_registration_key(self):
        "make new key, insert to db, and return it"
        while True:
            new_key = '%s:%s' % (
                'Nalida-Classic-Third',
                ''.join([random.choice(string.ascii_letters) for _ in range(25)])
                )
            if not self.is_registration_key(new_key):
                break
        self.db.sadd(self.key["registration_keys"], new_key)
        return new_key

    def is_registration_key(self, key):
        "check if the key is the registration key"
        return '안녕' in key
        return self.db.sismember(self.key["registration_keys"], key)

    def state(self, context, value=None):
        "set user(context)'s state"
        serialized = Module.serialize_context(context)
        state_key = self.key["state"] % serialized
        if value is None:
            result = self.db.get(state_key)
            return None if result == '' else result
        else:
            self.db.set(state_key, value)

    def nick(self, context, value=None):
        "getset of nick"
        serialized = Module.serialize_context(context)
        key = self.key["nickname"] % serialized
        if value is None:
            return self.db.get(key)
        else:
            self.db.set(key, value)

    def goal_name(self, context, value=None):
        "getset of goal"
        serialized = Module.serialize_context(context)
        key = self.key["goal_name"] % serialized
        if value is None:
            return self.db.get(key)
        else:
            self.db.set(key, value)

    def goal_description(self, context, value=None):
        "getset of goal"
        serialized = Module.serialize_context(context)
        key = self.key["goal_description"] % serialized
        if value is None:
            return self.db.get(key)
        else:
            self.db.set(key, value)

    def explanation(self, context, value=None):
        "getset of explanation"
        serialized = Module.serialize_context(context)
        key = self.key["explanation"] % serialized
        if value is None:
            return self.db.get(key)
        else:
            self.db.set(key, value)

    def session(self, context, value=None):
        "getset of session"
        serialized = Module.serialize_context(context)
        key = self.key["session"] % serialized
        if value is None:
            logging.debug('context is %s, session get returns %s',
                          serialized, self.db.get(key))
            return self.db.get(key)
        else:
            logging.debug('context is %s, session set to %s', serialized, value)
            self.db.set(key, value)

    def emorec_time(self, context, set_next=False):
        "get/set of current/next emorec time"
        serialized = Module.serialize_context(context)
        key = self.key["emorec_time"] % serialized
        result = self.db.get(key)
        result = json.loads(result) if result is not None else result
        if set_next:
            minute = random.randint(0, 59)
            if result is None:
                current = time.localtime()
                hour = current.tm_hour
                minute = current.tm_min
                if hour <= 9:
                    when = 'morning'
                elif hour <= 15:
                    when = 'noon'
                else:
                    when = 'evening'
                self.db.set(key, json.dumps([when, hour, minute]))
            elif result[0] == 'morning':
                hour = random.randint(13, 14)
                when = 'noon'
            elif result[0] == 'noon':
                hour = random.randint(19, 20)
                when = 'evening'
            elif result[0] == 'evening':
                hour = 22
                minute = 0
                when = 'night'
            elif result[0] == 'night':
                hour = random.randint(8, 9)
                when = 'morning'
            self.db.set(key, json.dumps([when, hour, minute]))
        else:
            if result is None:
                return [-1, -1, -1]
            return result

    def target_chat(self, context, value=None):
        "getset for target chat"
        serialized = Module.serialize_context(context)
        key = self.key["target_chat"] % serialized
        if value is None:
            return self.db.get(key)
        else:
            self.db.set(key, value)
