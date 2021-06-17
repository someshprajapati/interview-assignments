# Sample Nginx Log File Content

```
42.236.10.114 - - [19/Dec/2020:15:23:11 +0100] "GET /templates/jp_hotel/css/menu.css HTTP/1.1" 200 1457 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"
42.236.10.114 - - [19/Dec/2020:15:23:11 +0100] "GET /templates/jp_hotel/css/suckerfish.css HTTP/1.1" 200 3465 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"
42.236.10.125 - - [19/Dec/2020:15:23:12 +0100] "GET /media/system/js/caption.js HTTP/1.1" 200 1963 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"
42.236.10.114 - - [19/Dec/2020:15:23:12 +0100] "GET /modules/mod_bowslideshow/tmpl/js/sliderman.1.3.0.js HTTP/1.1" 200 33472 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"
54.36.149.55 - - [19/Dec/2020:16:06:42 +0100] "GET /index.php?option=com_content&view=article&id=46&Itemid=54 HTTP/1.1" 200 8938 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)" "-"
95.217.229.86 - - [19/Dec/2020:16:10:38 +0100] "GET /apache-log/access.log HTTP/1.1" 200 17171 "-" "Mozilla/5.0 (compatible; Seekport Crawler; http://seekport.com/" "-"
45.153.227.31 - - [19/Dec/2020:17:39:22 +0100] "POST /index.php?option=com_contact&view=contact&id=1 HTTP/1.1" 200 188 "" "Mozilla/5.0(WindowsNT10.0)AppleWebKit/537.36(KHTML,likeGecko)Chrome/51.0.2683.0Safari/537.36" "-"
182.239.117.249 - - [19/Dec/2020:16:13:33 +0100] "GET /apache-log/access.log HTTP/1.1" 200 17340 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36" "-"
42.236.10.117 - - [19/Dec/2020:15:23:13 +0100] "GET /images/stories/slideshow/almhuette_raith_04.jpg HTTP/1.1" 200 80637 "http://www.almhuette-raith.at/" "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 baidu.sogo.uc.UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN" "-"
```

### Assumptions:
Python 2 should be installed.

## How to Use:
1. Clone the repo.
2. Change the directory `cd log_parser`
2. Run the python script `python log_parser.py`
3. Use the below help menu to perform different action based on your requirement.

```
$ python log_parser.py -h
usage: log_parser.py [-h]
                     {top-requested-pages-count,successful-requests,unsuccessful-requests,top-unsuccessful-pages-count,top-requested-host-count,top-host-requested-page}
                     ...

Program to run the log parser

optional arguments:
  -h, --help            show this help message and exit

Log Parser:
  {top-requested-pages-count,successful-requests,unsuccessful-requests,top-unsuccessful-pages-count,top-requested-host-count,top-host-requested-page}
    top-requested-pages-count
                        Top [N] requested pages and the number of requests made for each page
    successful-requests
                        Calculate percentage of successful requests
    unsuccessful-requests
                        Calculate percentage of unsuccessful requests
    top-unsuccessful-pages-count
                        Top N unsuccessful page requests
    top-requested-host-count
                        Top [N] requested pages and the number of requests made for each host
    top-host-requested-page
                        For each of the top [N] hosts, show the top [C] pages requested and the number of requests for each
```

## We are going to perform the below actions using the log_parser script:

### 1. Top 10 requested pages and the number of requests made for each.

`python log_parser.py top-requested-pages-count -f access.log -n 10`


### 2. Percentage of successful requests (anything in the 200s and 300s range).

`python log_parser.py successful-requests -f access.log`


### 3. Percentage of unsuccessful requests (anything that is not in the 200s or 300s range).

`python log_parser.py unsuccessful-requests -f access.log`


### 4. Top 10 unsuccessful page requests.

`python log_parser.py top-unsuccessful-pages-count -f access.log -n 10`


### 5. The top 10 hosts making the most requests, displaying the IP address and number of requests made.

`python log_parser.py top-requested-host-count -f access.log -n 10`


### 6. For each of the top 10 hosts, show the top 5 pages requested and the number of requests for each.

`python log_parser.py top-host-requested-page -f access.log -n 10 -c 5`