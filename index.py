import tornado.web
import tornado.ioloop
import asyncio
import os

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # python-3.8.0a4

class uploadHandler(tornado.web.RequestHandler):
    def post(self):
        files = self.request.files["imgFile"]
        for f in files:
            fh = open(f"img/{f.filename}", "wb") #write with binary
            fh.write(f.body)
            fh.close()
        self.write(f"http://localhost:8080/img/{f.filename}")

    def get(self):
        self.render("index.html") #visiting from the browser

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/", uploadHandler),
            ("/img/(.*)", tornado.web.StaticFileHandler, {'path' : 'img'}), #using regex to take in any set of chars except line breaks
        ]

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "css") #searches for the static url in index.html as a template for CSS file
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if (__name__ == "__main__"):
    app = Application()
    app.listen(8080)
    print("Listening on port 8080")
    tornado.ioloop.IOLoop.instance().start() #enforcing only starting one instance!