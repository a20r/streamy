
from tornado import websocket, web, ioloop
import json

streamers = []
streamees = dict()
streamees_check = []
image = str()


class StreamerHandler(websocket.WebSocketHandler):

    def open(self, ws_id):
        self.ws_id = ws_id
        global streamers
        if self not in streamers:
            streamers.append(self)


    def on_message(self, message):
        self.write_message("OK")
        if self.ws_id in streamees.keys():
            for streamee in streamees[self.ws_id]:
                streamee.write_message(message)


    def on_close(self):
        global streamers
        if self in streamers:
            streamers.remove(self)


class StreameeHandler(websocket.WebSocketHandler):

    def open(self, ws_id):
        self.ws_id = ws_id
        global streamees_check, streamees
        if self not in streamees_check:
            if not ws_id in streamees.keys():
                streamees[ws_id] = list()
            streamees[ws_id].append(self)
            streamees_check.append(self)


    def on_close(self):
        global streamees, streamees_check
        if self in streamees_check:
            streamees_check.remove(self)
            streamees[self.ws_id].remove(self)


settings = {'auto_reload': True, 'debug': True}


streamer_app = web.Application([
    (r'/streamer/(.*)', StreamerHandler)
], **settings)

streamee_app = web.Application([
    (r'/streamee/(.*)', StreameeHandler)
], **settings)


if __name__ == '__main__':
    streamee_app.listen(8888)
    streamer_app.listen(8889)
    ioloop.IOLoop.instance().start()

