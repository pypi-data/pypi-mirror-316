import json
from collections import OrderedDict
import threading
import logging

from pyutils.scheduling.event_driven import Event


# sync event to signal the event is done
class SyncEvent(Event):

    def __init__(self, event, condition):
        super().__init__(event=event)
        self._condition = condition

    # set the done_condition to signal the event is done
    def set_result(self, result):
        super().set_result(result)
        self._condition.set()


class Context:

    def __init__(self, conf, executing_path, dispatcher):
        self.__conf = conf
        self.__executing_path = executing_path
        self.__components = OrderedDict()
        self.__services = OrderedDict()
        self.__commands = OrderedDict()
        self.__dispatcher = dispatcher
        self.__env = dict()

    def get_conf(self):
        return self.__conf

    def get_executing_path(self):
        return self.__executing_path

    def add_component(self, key, value):
        self.__components[key] = value

    def add_service(self, key, value):
        self.__services[key] = value

    def add_command(self, key, value):
        self.__commands[key] = value

    def get_components(self):
        return self.__components

    def get_services(self):
        return self.__services

    def get_commands(self):
        return self.__commands

    def dispatch(self, event):
        self.__dispatcher.dispatch(event)

    def add_env_entry(self, env_key, env_value):
        self.__env[env_key] = env_value

    def get_env_value(self, env_key):
        return self.__env.get(env_key)

    def sync_process_event(self, event, timeout=0):
        condition = threading.Event()
        event.set_done_condition(condition)
        self.dispatch(event)
        done = condition.wait(timeout)
        if not done:
            event.cancel()
        logging.info(f"sync_processed event {type(event)}, done={done}")
