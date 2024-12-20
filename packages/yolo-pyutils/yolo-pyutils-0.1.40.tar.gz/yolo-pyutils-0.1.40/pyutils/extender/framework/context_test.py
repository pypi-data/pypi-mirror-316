import logging
import time
import unittest
from pyutils.extender.framework.context import Context
from pyutils.scheduling.event_driven import Event, Dispatcher, Handler

logging.basicConfig(stream=None, level=logging.DEBUG,
                      format='%(asctime)s - %(levelname)s: %(message)s')

class TestHandler(Handler):

    def get_applicable_event_classes(self):
        return [TestEvent]

    def handle(self, event):
        logging.info("dispatching event: {}".format(event))
        sleep_time = event.get_data_value("sleep_time")
        time.sleep(sleep_time)
        logging.info("dispatching event done: {}".format(event))

class TestEvent(Event):
    def __init__(self, sleep_time):
        super().__init__(data={"sleep_time": sleep_time})

class TestContext(unittest.TestCase):

    def test_dispatch(self):
        test_handler = TestHandler()
        test_dispatcher = Dispatcher()
        test_dispatcher.register_handler(test_handler)
        test_dispatcher.start()
        context = Context(None, None, test_dispatcher)
        # test event
        event = TestEvent(sleep_time=1)
        context.sync_process_event(event, 2)
        self.assertFalse(event.is_canceled())
        logging.info(event.get_result())

        context.sync_process_event(event, 0.5)
        self.assertTrue(event.is_canceled())
        logging.info(event.get_result())
