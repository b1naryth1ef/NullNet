from libnull.api import API


client = API(["http://localhost:1337"])
print "Hash: %s" % client.check_global_hash()
