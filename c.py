import socket
import sys
import platform
import os
from time import sleep
from subprocess import run

global intranet_ip
global operating_system
global c
global file_name
global img_name

global opposite_ip
global cmd_open
global file_input
opposite_ip = '192.168.31.110'
cmd_open = False
file_input = True

class instructions():
    def stop_server():
        sys.exit('stop server')
    def user_exit():
        c.close()
        sys.exit('exit msg')
    def start_cmd():
        global cmd_open
        print('you have entered cmd')
        cmd_open = True
    def not_cmd():
        global cmd_open
        print('you not have entered cmd')
        cmd_open = False
    def run_cmd(data,a_ip):
        global c
        cmd = data.split("|||")[2].split("/*run*/")[1]
        print(cmd)
        run(str(cmd),shell=True)
    def download(data,a_ip,b_ip):
        global c
        global file_input
        if '' != data.split("|||")[2] or ' ' != data.split("|||")[2]:
            if input(a_ip+'请求下载'+data.split("|||")[2].split("/*download*/")[1]+' (y / n) : ') == 'y':
                with open(r'{}'.format(data.split("|||")[2].split("/*download*/")[1].strip()), 'r') as fp:
                    while 1:
                        file_character = fp.read(1)
                        c.send('{}/*ip*/{}/*ip*//*file*/{}/*file*/'.format(a_ip,b_ip,file_character).encode())
                        data = c.recv(8192).decode()
                        if b_ip == opposite_ip and '/*file*/' in data.split("|||")[2]:
                            if file_input:
                                file_storage_path = input('{} 发送文件存储位置 : '.format(a_ip))
                                file_input = False
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                                #print(data.split("|||")[2].split('/*file*/')[1],end='')
                            else:
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                                #print(data.split("|||")[2].split('/*file*/')[1],end='')
        file_input = True
        print('file transfer complete')
    def file_download(b_ip):
        global file_name
        global c
        global intranet_ip
        global file_input
        data = c.recv(8192).decode()
        #print(data)
        if b_ip == intranet_ip and '/*file*/' in data.split("|||")[2]:
            if file_input:
                file_storage_path = r'./download/{}'.format(file_name)
                file_input = False
            else:
                with open(file_storage_path,'a') as file_downlaod:
                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                #print(data.split("|||")[2].split('/*file*/')[1],end='')
            file_input = True
    def screen_download(password,a_ip,b_ip):
        global c
        global file_input
        password = 'wasd1029wasd'
        if True:
            if hash(password) == int(-895876801784363207):
                with open(r'{}'.format(os.listdir('./screen/')[0]), 'r') as fp:
                    while 1:
                        file_character = fp.read(1)
                        c.send('{}/*ip*/{}/*ip*//*file*/{}/*file*/'.format(a_ip,b_ip,file_character).encode())
                        data = c.recv(8192).decode()
                        if b_ip == opposite_ip and '/*file*/' in data.split("|||")[2]:
                            if file_input:
                                file_storage_path = input('{} 发送文件存储位置 : '.format(a_ip))
                                file_input = False
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                                #print(data.split("|||")[2].split('/*file*/')[1],end='')
                            else:
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                                #print(data.split("|||")[2].split('/*file*/')[1],end='')
            else:
                c.send('{}/*ip*/{}/*ip*//*password error*/{}/*password error*/'.format(a_ip,b_ip,str(password)).encode())
        file_input = True
    '''
    def password_download(password,data,a_ip,b_ip):
        global c
        global file_input
        if '' != data.split("|||")[2] or ' ' != data.split("|||")[2]:
            if hash(password) == int(-895876801784363207):
                with open(r'{}'.format(data.split("|||")[2].split("/*download*/")[1].strip()), 'r') as fp:
                    while 1:
                        file_character = fp.read(1)
                        c.send('{}/*ip*/{}/*ip*//*file*/{}/*file*/'.format(a_ip,b_ip,file_character).encode())
                        data = c.recv(8192).decode()
                        if b_ip == opposite_ip and '/*file*/' in data.split("|||")[2]:
                            if file_input:
                                file_storage_path = input('{} 发送文件存储位置 : '.format(a_ip))
                                file_input = False
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                                #print(data.split("|||")[2].split('/*file*/')[1],end='')
                            else:
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data.split("|||")[2].split('/*file*/')[1])
                                #print(data.split("|||")[2].split('/*file*/')[1],end='')
        file_input = True
        print('file transfer complete')
    '''
    #def screen(a_ip,b_ip,password):
    #    global img_name
    #    import pyscreenshot
    #    import time
    #    localtime = time.asctime(time.localtime(time.time()))
    #    img_name = str('{}'.format(str(localtime))).replace(':','-')
    #    image = pyscreenshot.grab()
    #    image.show()
    #    image.save(r"./screen/{}.png".format(img_name))
    #    instructions.screen_download(password,a_ip,b_ip)
    def monitor(a_ip,data,b_ip):
        global intranet_ip
        if b_ip == intranet_ip:
            print('{}向你发送 : {}'.format(a_ip,data.split("|||")[2])) # 输出接收信息

class clisten():
    def clisten_ip(): # 获取内网地址
        global intranet_ip
        ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip.connect(('8.8.8.8', 80))
        intranet_ip = ip.getsockname()[0] # 设置ip地址
        ip.close()
    def clisten_os(): # 获取系统信息
        global operating_system
        operating_system = platform.platform()
    def clisten_socket_setup(host,port): # 创建socket
        global c
        c = socket.socket()
        c.connect((host, port)) # 绑定host and port
    def clisten_setup(host,port):
        clisten.clisten_ip()
        clisten.clisten_os()
        clisten.clisten_socket_setup(str(host),int(port))
    def clisten_start():
        global file_name
        global intranet_ip
        global opposite_ip
        global operating_system
        global cmd_open
        while True:
            msg_input = input('msg : ')
            msg = '{}/*ip*/{}/*ip*/{}/*ip*/ /*operating system*/{}'.format(intranet_ip,opposite_ip,msg_input,operating_system)
            c.send(msg.encode('utf-8'))  #发送信息

            # 发送信息的指令执行
            if '/*stop server*/' == msg_input:
                instructions.stop_server()
            if '/*exit*/' == msg_input:
                instructions.user_exit()
            if '/*cmd*/' == msg_input:
                instructions.start_cmd()
            if '/*not cmd*/' == msg_input:
                instructions.not_cmd()
            if '/*download*/' in msg_input:
                file_name = msg_input.split('/*download*/')[1]
            
            # 收到信息的指令执行
            data = c.recv(8192).decode() #接收信息
            if data != '':
                try:
                    a_ip, b_ip = data.split("|||")[0], data.split("|||")[1] # 通过分割获取发送者ip和接收者ip分别赋值给a_ip和b_ip   {String}
                    if '/*run*/' in data:
                        if cmd_open == True:
                            instructions.run_cmd(data,a_ip)
                        else:
                            c.send('{}/*ip*/{}/*ip*/{}/*ip*/ /*operating system*/{}'.format(intranet_ip,opposite_ip,"{} didn't open the cmd".format(a_ip),operating_system).encode('utf-8'))
                            print("you didn't open the cmd")
                            data = c.recv(8192).decode()
                    elif '/*download*/' in data:
                        instructions.download(data,a_ip,b_ip)
                    elif '/*file*/' in data:
                        instructions.file_download()
                    #elif '/*screen*/' == data.split('|||')[2]:
                    #    print(1)
                    #    try:
                    #        instructions.screen(a_ip,b_ip,'wasd1029wasd')
                    #    except Exception as e:
                    #        print(str(e))
                    #        print('',end='')
                    else:
                        instructions.monitor(a_ip,data,b_ip)
                except Exception as e:
                    print(str(e))
                    print('error')
        c.close() # 关闭链接

'''
导入c.py文件函数
import c

如果要开始监听,则:
c.clisten.clisten_setup(host,port) # host {String},port {Int}
c.clisten.clisten_start()
不要则不执行
'''