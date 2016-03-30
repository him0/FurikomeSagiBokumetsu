import os
import json
import random
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.web import url
from Furikome import Furikome


class IndexHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        user_id = random.randint(0, 100)
        self.render('index.html', user_id=user_id)


class ChatHandler(tornado.websocket.WebSocketHandler):

    waiters = set()
    messages = [] # messageはidとtextを含むディクショナリ
    # チャットユーザのidとFurikomeインスタンスのディクショナリ
    furikome_by_ids = {}

    def open(self, *args, **kwargs):
        self.waiters.add(self)
        self.write_message({'messages': self.messages})

    def on_message(self, message):
        message = json.loads(message) # 紛らわしい
        id = message['id']
        text = message['message']
        if id in self.furikome_by_ids:
            r = self.furikome_by_ids[id].recode(text)
            print(r)
            if r["talk_dubious"] == True:
                text += " (詐欺！)"
        else:
            f = Furikome()
            f.recode(text)
            self.furikome_by_ids[id] = f

        self.messages.append(message)
        for waiter in self.waiters:
            if waiter == self:
                continue
            waiter.write_message({'id': id, 'message': text})

    def on_close(self):
        self.waiters.remove(self)


class Application(tornado.web.Application):

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        tornado.web.Application.__init__(self,
                                         [
                                         url(r'/', IndexHandler, name='index'),
                                         url(r'/chat', ChatHandler, name='chat'),
                                         ],
                                         template_path=os.path.join(BASE_DIR, 'templates'),
                                         static_path=os.path.join(BASE_DIR, 'static'),
                                         )


if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()