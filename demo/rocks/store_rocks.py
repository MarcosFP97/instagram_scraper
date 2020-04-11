#!/usr/bin/env python
# encoding=utf8

from catenae import Link, Electron, utils
import uuid


class StoreRocks(Link):
    KEY_SIZE = 128
    TIMESTAMP_SIZE = 13

    def get_key(self, tweet):
        timestamp = str(tweet['timestamp']).ljust(StoreRocks.TIMESTAMP_SIZE, '0')
        key = f"{timestamp}{tweet['query']}".ljust(StoreRocks.KEY_SIZE, '0')
        key = list(key)
        key[-len(tweet['id']):] = tweet['id']
        key = ''.join(key)
        self.logger.log(key)

        if len(key) > StoreRocks.KEY_SIZE:
            raise ValueError
        return key

    def transform(self, electron):
        tweet = electron.value
        key = self.get_key(tweet)

        self.rocksdb.put(key, tweet)
        value = self.rocksdb.get(key)
        self.logger.log(f'Valor recuperado de la bd: {value}')


if __name__ == '__main__':
    StoreRocks().start()