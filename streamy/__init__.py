

def run(host, port):
    import server.config as config
    from flask import Flask
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer(
        (host, port), config.app
    )

    http_server.serve_forever()

