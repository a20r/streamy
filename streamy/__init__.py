

def run(host, port):
    import server.config as config
    from flask import Flask

    config.app.run(host=host, port=port, debug=True, use_reloader=False)

