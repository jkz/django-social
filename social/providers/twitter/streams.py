import json

#from functools import wraps

import callm

#from utils.decorators import default_kwargs

from .parser import import_status, import_data

class Listener(callm.Listener):
    def on_data(self, data):
        if data:
            print data
            try:
                import_data(json.loads(data))
            except ValueError as e:
                print 'Noes, dis data! :( | data:', data
                print 'Cuz', e

    def on_error(self, code, error_count):
        print code
        if code < 200:
            return

class StatusStreamListener(Listener):
    def on_data(self, data):
        print data
        try:
            import_status(json.loads(data))
        except TypeError as e:
            print e

'''
class Stream(callm.Stream):
    secure = True
    snooze_time = 5.0

    _delimiter = 'length'

    def __init__(self, auth):
        self.auth = auth

    def read_loop_iter(self):
        # Note: keep-alive newlines might be inserted before each length value.
        # read the delimiter string
        delimited_string = self.readline()

        # return the next payload
        if delimited_string.isdigit():
            byte_count = int(delimited_string)
            ret = self.read(byte_count)
            return ret
        #XXX we actually don't want this to happen
        else:
            return delimited_string
        return None

    def retry_time(self, error_count):
        return {
            0: 0.0, # Should not occur
            1: 10.0,
            2: 20.0,
            3: 40.0,
            4: 80.0,
            5: 160.0
        }.get(error_count, 240.0)


def encode_list_params(*list_names):
    """',' joins all params lists whose key is present in given name_list"""
    def decorator(func):
        @wraps(func)
        def funk(*args, **params):
            for key in list_names:
                val = params.get(key, None)
                if val is not None:
                    params[key] = ','.join(map(str, val))
                    print 'ENCODE', val, 'to', params[key]
            return func(*args, **params)
        return funk
    return decorator


class StatusStream(Stream):
    host = 'stream.twitter.com'
    listener = StatusStreamListener()

    @default_kwargs(
            count=0,
            delimited='length',
            stall_warning='true')
    @encode_list_params('track', 'locations', 'follow')
    def filter(self, **params):
        params['headers'] = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self.POST('/1.1/statuses/filter.json', **params)

    @default_kwargs(
            count=0,
            delimited='length',
            stall_warning='true')
    def firehose(self, **params):
        return self.GET('/1/statuses/firehose.json', **params)

    @default_kwargs(
            count=0,
            delimited='length',
            stall_warning='true')
    def links(self, **params):
        return self.GET('/1/statuses/links.json', **params)

    @default_kwargs(
            delimited='length',
            stall_warning='true')
    def retweet(self, **params):
        return self.GET('/1/statuses/retweet.json', **params)

    @default_kwargs(
            count=0,
            delimited='length',
            stall_warning='true')
    def sample(self, **params):
        return self.GET('/1/statuses/sample.json', **params)


class UserStream(Stream):
    host = 'userstream.twitter.com'
    listener = Listener()

    @default_kwargs(**{
            'count': 0,
            'delimited': 'length',
            'stall_warning': 'true',
            'with': 'followings'}) # use 'user' for user related only
    def __call__(self, **params):
        return self.GET('/2/user.json', **params)


class SiteStream(Stream):
    host = 'sitestream.twitter.com'

    @default_kwargs(**{
            'count': 0,
            'delimited': 'length',
            'stall_warning': 'true',
            'with': 'followings'}) # use 'user' for user related only
    @encode_list_params('follow',)
    def __call__(self, **params):
        return self.stream.GET('/2b/site.json', **params)

'''
