import requests, time, gnupg, os, json, getpass

# TODO: safe the requests

join = lambda *args: '/'.join(args)

class API(object):
    def __init__(self, trackers=[], home=None):
        self.trackers = trackers
        self.favorite = None
        self.home = home
        self.gpg = gnupg.GPG(homedir=home)

    def post_article(self, title=None, author=None, content=None, sign=False, password=None):
        new = json.dumps({
            "title": title,
            "author": author,
            "content": content,
        })

        if sign and not password:
            password = getpass.getpass("GNUPG Password: ")

        if sign:
            new = gpg.sign(json.dumps(new), passphrase=password)

        requests.post(join(self.get_favorite(), "post"), params={
                "data": new,
                "signed": sign
            })

    def check_global_hash(self):
        """
        Verify all the trackers agree with the global hash. The global
        hash is considered the 'id' of the current article board. This
        needs to match or the trackers will appear to be out of sync.

        :rtype: bool
        :returns: Whether the hash matches in every tracker.
        """
        return self.verify(self.mrequest(""), ["globhash"])

    def get_global_hash(self, safe=False):
        """
        Get the global tracker hash.

        :param safe: Verify all trackers have the same hash first.
        :type safe: bool
        :rtype: str
        :returns: The global 32bit hash.
        """
        if safe:
            if not self.check_global_hash():
                raise Exception("Tracker global hash mismatch!")
        return self.request()['globhash']

    def get_favorite(self):
        """
        Find a favorite server based on ping.
        """
        results = []
        for id, t in enumerate(self.trackers):
            start = time.time()
            requests.get(t)
            results.append((time.time()-start, id))
        return sorted(results, key=lambda i: i[0])[0][1]

    def choose_favorite(self):
        """
        Set the cached favorite using `API.get_favorite`
        """
        self.favorite = self.get_favorite()

    def mrequest(self, data={}}, url):
        """
        Make a request to all the trackers. These are used to ensure a
        tracker isnt fibbing results. Unless your worried about MITM, or
        can't trust your trackers, this is probablly overkill.
        """
        results = []
        for t in self.trackers:
            results.append(requests.get(join(t, url), params=data).json())
        return results

    def verify(self, rq, matches=[]):
        """
        Take a list of request, and a set of keys and
        verify they match in each request.
        """
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

    def request(self, url, data={}}, safe=False):
        """
        Make a request using our favorite tracker
        """
        if safe:
            return self.mrequest(url)

        if not self.favorite:
            self.choose_favorite()

        return requests.get(join(url, self.favorite), params=data).json()

    def query_articles(self, page=1, per_page=50, author=None, signed=None, contains=None, before=None, safe=False):
        q = {
            "page": page,
            "per": per_page,
            "author": author,
            "signed": signed,
            "contains": contains,
            "before": before
        }
        return self.request("query", data=q, safe=safe)




