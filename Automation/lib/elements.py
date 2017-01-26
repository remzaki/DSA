# /automation/lib/
import httplib
import json
import glob
from StringIO import StringIO

import lib.pre as pre


class Elements(object):
    """
    This Elements class queries the elements to either on a API server or a JSON downloaded file
    """

    def __init__(self):
        self.data = {}
        if pre.config['server_connection'] == 'offline':
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

        if pre.config['server_connection'] == 'offline':
            try:
                data = self.data[name]
            except KeyError:
                print "KeyError!"
            except Exception, ex:
                print ex

        elif pre.config['server_connection'] == 'online':
            request_site = httplib.HTTPConnection(pre.config['server_address'])
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


def _trim_name():
    pass
