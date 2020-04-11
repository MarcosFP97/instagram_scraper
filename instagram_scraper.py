from pygram import PyGram
from catenae import Link, Electron, utils
import json
from random import randint
from threading import Lock
import time


class InstagramSource(Link):

    def setup(self):
        self.counter_lock = Lock()
        self.counter = 0
        self.pygram = PyGram()

        self.logger.log(f'{self.args}')
        for query in self.args:
            self.launch_thread(self.search,[query])
            time.sleep(60)

    def search(self, query, max_items=-1):

        for post in self.pygram.get_posts(query):
            self.logger.log(post)
            post.update({'query': query})
            self.send(post, topic='posts')
            
            #####################################

            comments = self.pygram.get_comments(post)
            for comment in comments:
                self.logger.log(comment)
                comment.update({'query': query})
                self.send(comment, topic='comments')

            with self.counter_lock:

                self.counter += 1
            
                if self.counter % 10 == 0:
                    self.logger.log(f'{self.counter} retrieved posts for {query}')

                if self.counter == max_items:
                    self.logger.log(f'Search stopped for ({query}), max_items reached')
                    break

InstagramSource().start()