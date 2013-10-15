import requests, time

# TODO: safe the requests

def join(*args):
    return '/'.join(args)

class API(object):
    def __init__(self, trackers=[]):
        self.trackers = trackers
        self.favorite = None

    def check_hash(self):
        """
        Verify all the trackers agree with the global hash. The global
        hash is considered the 'id' of the current article board. This
        needs to match or the trackers will appear to be out of sync.
        """
        return self._verify(self.mrequest(""), ["globhash"])

    def choose_favorite(self):
        """
        Choose a favorite tracker based on ping. This is relativly
        accurate, although ping can spike/change.
        """
        results = []
        for id, t in enumerate(self.trackers):
            start = time.time()
            requests.get(t)
            results.append((time.time()-start, id))
        self.favorite = sorted(results, key=lambda i: i[0])[0][1]

    def mrequest(self, url):
        """
        Make a request to all the trackers. These are used to ensure a
        tracker isnt fibbing results. Unless your worried about MITM, or
        can't trust your trackers, this is probablly overkill.
        """
        results = []
        for t in self.trackers:
            results.append(requests.get(join(t, url)))
        return results

    def _verify(self, rq, matches=[]):
        last = {}
        for entry in rq:
            entry = entry.json()
            if not last:
                last = {i: entry[i] for i in matches}
                continue
            for i in matches:
                if entry[i] != last[i]:
                    return False
        return True

    def request(self, url):
        """
        Make a request using our favorite tracker
        """
        if not self.favorite:
            self.choose_favorite()
        return requests.get(join(url, self.favorite))

    def get_articles(self, safe=False): pass
