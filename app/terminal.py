import asyncio
import tornado.web
from tornado.ioloop import IOLoop
from terminado import TermSocket, SingleTermManager

'''
def run():
    term_manager = SingleTermManager(shell_command=['bash'])
    app = tornado.web.Application(handlers)
    app.listen(8010)
    IOLoop.current().start()
'''

class WebServer(tornado.web.Application):

    def __init__(self):
        term_manager = SingleTermManager(shell_command=['bash'])
        handlers = [
                (r"/websocket", TermSocket, {'term_manager': term_manager}),
                (r"/()", tornado.web.StaticFileHandler, {'path':'index.html'}),
                (r"/(.*)", tornado.web.StaticFileHandler, {'path':'.'}),
               ]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self, port=8010):
        self.listen(port)
        tornado.ioloop.IOLoop.instance().start()


ws = WebServer()


def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    ws.run()


from threading import Thread
t = Thread(target=start_server, args=())
t.daemon = True
t.start()

t.join()
