# /automation/lib/
import httplib
import json
import glob
from lib.config import config
from StringIO import StringIO


class Elements:
    """
    This Elements class queries the elements to either on a API server or a JSON downloaded file
    """

    def __init__(self):
        self.data = {}
        if config.mode == 'offline':
            path = "./Elements_*.json"
            g = glob.glob(path)
            if len(g) > 1:
                filename = g[len(g) - 1]
                with open(filename, 'r') as data_file:
                    contents = json.load(data_file)

                for content in contents:
                    name = content['Name']
                    value = content['Value']
                    self.data[name] = value

    def get_data(self, name):
        data = False

        if config.mode == 'offline':
            try:
                data = self.data[name]
            except KeyError:
                print "KeyError!"
            except Exception, ex:
                print ex

        elif config.mode == 'online':
            request_site = httplib.HTTPConnection(config.server)
            request_site.request('GET', '/DSA/api/elements?name=%s&min=true' % name,
                                 headers={"Accept": "application/json"})

            result = request_site.getresponse()

            io = StringIO(result.read())
            try:
                d = json.load(io)
                data = d['Value']
            except Exception:
                data = False

        return data

    def batch(self):
        req = httplib.HTTPConnection("localhost", 62526)

        for d in self.data.items():
            print "%s === %s" % (d[0], d[1][0])
            print "Creating Request body..."
            body = json.dumps({
                "Name": d[0],
                "Value": d[1][0],
                "ShortDesc": ""
            })
            print body

            print "Sending the API Request..."
            req.request('POST', '/api/elements', body, headers={"Content-Type": "application/json"})

            print "Acquiring Response..."
            result = req.getresponse()
            print "Response: %s" % result.read()

            print "_" * 100
