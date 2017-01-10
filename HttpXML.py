import httplib, urllib
import re
 
params = urllib.urlencode({'q': 'login', 'email': 'juasjuas@lol.com', 'pwd': 'lala'})
 
conn = httplib.HTTPConnection("my.lolizator.com:80")
conn.request("GET", "/cmd.php?"+params)
response = conn.getresponse()
print response.status, response.reason
 
#data = response.read()
#print data
 
cookies = response.getheader("set-cookie")
m = re.search('.*PHPSESSID=([a-zA-Z0-9]+);.*', cookies)
session = m.group(1)
print "session %s" % session
XML='<tag1 name="testgroup"><tag2 id="12" type="3"><tag3 id="1">aaa</tag3></tag2></tag1>'
params = urllib.urlencode({'q': 'set'})
headers = { "Cookie": "PHPSESSID=" + session, "Content-type": "text/xml",
            "Content-Length": "%d" % len(XML)}
conn.request("POST", "/cmd.php?"+params, "", headers)
conn.send(XML)
response = conn.getresponse()
print response.status, response.reason
 
print response.read()
conn.close()

