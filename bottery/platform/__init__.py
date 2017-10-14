import importlib
import logging
import os

from bottery.conf import settings
from bottery.exceptions import ImproperlyConfigured


logger = logging.getLogger('bottery.platforms')

def discover_and_run_view(message):
    if message is None:
        return None
    base = os.getcwd()
    patterns_path = os.path.join(base, 'patterns.py')
    if not os.path.isfile(patterns_path):
        raise ImproperlyConfigured('Could not find patterns module')

    patterns = importlib.import_module('patterns').patterns
    for pattern in patterns:
        if pattern.check(message):
            logger.debug('[%s] Pattern found', message.platform)
            print('Pattern found:', pattern)
            call_view = getattr(pattern, "call_view", None)
            if callable(call_view):
                response = pattern.call_view(message)
                return response
            if isinstance(pattern.view, str):
                view = importlib.import_module(pattern.view)
            else:
                view = pattern.view
            return view(message)

    # raise Exception('No Pattern found!')
    return None

def discover_view(message):
    base = os.getcwd()
    patterns_path = os.path.join(base, 'patterns.py')
    if not os.path.isfile(patterns_path):
        raise ImproperlyConfigured('Could not find patterns module')

    patterns = importlib.import_module('patterns').patterns
    for pattern in patterns:
        if pattern.check(message):
            logger.debug('[%s] Pattern found', message.platform)
            if isinstance(pattern.view, str):
                return importlib.import_module(pattern.view)
            return pattern.view

    # raise Exception('No Pattern found!')
    return None


class BasePlatform:

    def __init__(self, **kw):
        self.tasks = []

        for item, value in kw.items():
            setattr(self, item, value)

    @property
    def webhook_endpoint(self):
        return '/hook/{}'.format(self.platform)

    @property
    def webhook_url(self):
        return 'https://{}{}'.format(settings.HOSTNAME, self.webhook_endpoint)

    def build_message(self):
        raise NotImplementedError('create_message not implemented')
