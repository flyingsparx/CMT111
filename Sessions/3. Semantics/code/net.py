# Author: Will Webberley (flyingsparx).
# License: Apache
#
# Simple, quick, dirty HTTP requester. Hardcoded to http://localhost on port 80.
# Change this by editing the relevant lines below.
#
# Example usage:
# python net.py GET /users
# python net.py POST /users name:will age:20 "job:research associate"
# python net.py DELETE /users/will


import sys, urllib, urllib2

allowed_methods = ["GET", "POST", "PUT", "DELETE"]

if len(sys.argv) < 3:
    print "Usage: python net.py <HTTP_METHOD> <URL> *<DATA1>"
    exit()

method = sys.argv[1]
url = sys.argv[2]
data = {}
if len(sys.argv) > 3:
    for i in range(3, len(sys.argv)):
        data[sys.argv[i].split(":")[0]] = sys.argv[i].split(":")[1]

if method not in allowed_methods:
    print method+" is not a supported method"

opener = urllib2.build_opener(urllib2.HTTPHandler)
request = None
if data != {}:
    request = urllib2.Request('http://localhost:80'+url, data=urllib.urlencode(data))
else:
    request = urllib2.Request('http://localhost:80'+url)

#request.add_header('Content-Type', 'your/contenttype')
request.get_method = lambda: method 
response = None
try:
    response = opener.open(request)

    print response.getcode(),
    print response.msg
    print response.info()
    print 
    print response.read()
except Exception as e:
    print e
