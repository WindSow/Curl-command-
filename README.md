# Curl-command

Objective : Reduce the human mistake when excute curl command curl -Iv URL --resolve Domain:Port:IP

Rule :

1. If the Port input are 80, URL input must start with http. If the Port input are 443, URL input must start with https. And If the Port input are other number, URL input must end  with port such as https:xxx.com:Port. It will show the error message if against rule 

2. If IP is empty then  excute curl -Iv URL only.

3. If result are connection failed or http status 5XX, will continue tcp ping test.

Step:

1. Download the python https://www.python.org/downloads/ and install it,

2. Download python script here.

3. Install library pip install dnspython whois requests

4. Excute the script.

