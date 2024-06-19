# Meowpi 
 Your purrfect API endpoint verification and filtering tool. 
 Meowpi actively and passively checks for API endpoints in your list of urls. It comes with HTTP probing and API keywords to perform the checks.
  
  Created by mrunoriginal/AtlasWiki
<br>
<br>

## Key Features:
+ **Stdout-Friendly:** basic printing of only urls to stdout.
+ **Fast HTTP Probing**: uses concurrent requests and allow you to optionally set the requests per sec.
+ **Filtering modes**: comes with filtering of status codes when doing http probing.
+ **Active Checking**: uses HTTP Probing to do active checks for single/multi-method APIs.
+ **Passive Checking**: uses API keywords and api paths on the url to determine the API endpoints.
<br>

## Installation:

clone the repo
```
git clone https://github.com/AtlasWiki/meowpi.git
```
install the dependencies
```
pip install -r requirements.txt
```

run the file:
+ python:
```
python meowpi.py all_urls.txt
```
or
+ linux:
```
./js-parse meowpi.py all_urls.txt
```


## Options:
```
-h, --help            show this help message and exit
-s, --stdout          stdout friendly, displays urls only in stdout compatibility. also known as silent mode (default: False)
-m {all,1xx,2xx,3xx,4xx,5xx,forbidden}, --mode {all,1xx,2xx,3xx,4xx,5xx,forbidden}
                      filter modes (default: None)
-p, --passive         enables passive API filtering only and disables active API probing (default: False)
-a, --active          enables active API probing and disables passive API filtering (default: False)
--no-api-check        uses only http probing and no api checks (default: False)
-r REQUESTS, --requests REQUESTS
                      the number of concurrent/multiple requests per second (it is multiplied by 2 as it does both GET and POST) (default is set to 15 req/sec (without specifying) which would be actually 30) (default: 15)  
```

## Some Example Usages:
basic usage:
```
python meowpi.py all_urls.txt
```
<img width="1200" alt="image" src="https://github.com/AtlasWiki/meowpi/assets/87085506/42cfd6b4-b5ae-4f7d-a4e5-b217513f1543">
<img width="1200" alt="image" src="https://github.com/AtlasWiki/meowpi/assets/87085506/c0a24715-5fae-43cf-a285-4e25ef8c8cd5">



<br>

Active Check Only: 
```
python meowpi.py all_urls.txt --active
```
<img width="1200" alt="image" src="https://github.com/AtlasWiki/meowpi/assets/87085506/6fdfbd25-16f5-47e6-b07f-df141426c5f8">





<br>

Passive Check Only: 

```
python meowpi.py all_urls.txt --passive
```
<img width="1200" alt="image" src="https://github.com/AtlasWiki/meowpi/assets/87085506/618fcdaa-1db6-4818-90e1-916587808655">



<br>


<br>


### Warranty
The creator(s) of this tool provides no warranty or assurance regarding its performance, dependability, or suitability for any specific purpose.

The tool is furnished on an "as is" basis without any form of warranty, whether express or implied, encompassing, but not limited to, implied warranties of merchantability, fitness for a particular purpose, or non-infringement.

The user assumes full responsibility for employing this tool and does so at their own peril. The creator(s) holds no accountability for any loss, damage, or expenses sustained by the user or any third party due to the utilization of this tool, whether in a direct or indirect manner.

Moreover, the creator(s) explicitly renounces any liability or responsibility for the accuracy, substance, or availability of information acquired through the use of this tool, as well as for any harm inflicted by viruses, malware, or other malicious components that may infiltrate the user's system as a result of employing this tool.

By utilizing this tool, the user acknowledges that they have perused and understood this warranty declaration and agree to undertake all risks linked to its utilization.
  
### License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/AtlasWiki/meowpi/blob/main/LICENSE) for details.
