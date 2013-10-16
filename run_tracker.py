from libnull.tracker.main import app
#from gevent import wsgi

#wsgi.WSGIServer(('', 1337), app, spawn=None).serve_forever()

app.run(debug=True, port=1337)
