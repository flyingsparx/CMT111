import sys, httplib

allowed_methods = ["GET", "POST", "PUT", "DELETE"]

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print "Usage: python net.py <HTTP_METHOD> <URL> *<DATA>"
    exit()

method = sys.argv[1]
url = sys.argv[2]
data = None
if len(sys.argv) == 4:
    data = sys.argv[3]

if method not in allowed_methods:
    print method+" is not a supported method"

conn = httplib.HTTPConnection('localhost:80')
conn.request(method, url)
if data is not None:
    conn.send(data)
response = conn.getresponse()
print response.status
for header in response.getheaders():
    print header[0]+": "+header[1]
print
print response.read()
