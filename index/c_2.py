import socket
import sys
import platform
import os
from time import sleep
from subprocess import run
import ast

global intranet_ip
global operating_system
global c
global file_name

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
        cmd = data['run']
        print(cmd)
        run(str(cmd),shell=True)
    def download(data,a_ip,b_ip):
        global c
        global file_input
        if '' != data['msg'] or ' ' != data['msg']:
            if input(a_ip+'请求下载'+data['msg']['download']+' (y / n) : ') == 'y':
                with open(r'{}'.format(data['msg']['download'].strip()), 'r') as fp:
                    while 1:
                        file_character = fp.read(1)
                        c.send(str({'a_ip':a_ip,'b_ip':b_ip,'file':file_character,'instructions':'file'}).encode())
                        data = c.recv(8192).decode()
                        if b_ip == opposite_ip and 'file' == data['instructions']:
                            if file_input:
                                file_storage_path = input('{} 发送文件存储位置 : '.format(a_ip))
                                file_input = False
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data['file'])
                                #print(data['file'],end='')
                            else:
                                with open(file_storage_path,'a') as file_downlaod:
                                    file_downlaod.write(data['file'])
                                #print(data['file']],end='')
        file_input = True
        print('file transfer complete')
    def file_download(b_ip):
        global file_name
        global c
        global intranet_ip
        global file_input
        data = list(c.recv(8192).decode())
        #print(data)
        if b_ip == intranet_ip and 'file' == data['instructions']:
            if file_input:
                file_storage_path = r'./download/{}'.format(file_name)
                file_input = False
            else:
                with open(file_storage_path,'a') as file_downlaod:
                    file_downlaod.write(data['file'])
                #print(data['file']],end='')
            file_input = True
    def monitor(a_ip,data,b_ip):
        global intranet_ip
        if b_ip == intranet_ip:
            print('{}向你发送 : {}'.format(a_ip,data['msg'])) # 输出接收信息

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

            # 发送信息的指令执行
            if '/*stop server*/' == msg_input:
                msg = {'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':msg_input,'operating system':operating_system,'instructions':'stop server'}
                c.send(msg.encode('utf-8'))  #发送信息
                instructions.stop_server()
            elif '/*exit*/' == msg_input:
                msg = {'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':msg_input,'operating system':operating_system,'instructions':'user exit'}
                c.send(str(msg).encode('utf-8'))  #发送信息
                instructions.user_exit()
            elif '/*cmd*/' == msg_input:
                msg = {'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':msg_input,'operating system':operating_system,'instructions':'cmd'}
                c.send(str(msg).encode('utf-8'))  #发送信息
                instructions.start_cmd()
            elif '/*not cmd*/' == msg_input:
                msg = {'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':msg_input,'operating system':operating_system,'instructions':'not cmd'}
                c.send(str(msg).encode('utf-8'))  #发送信息
                instructions.not_cmd()
            elif '/*download*/' in msg_input:
                msg = {'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':msg_input,'operating system':operating_system,'instructions':'download'}
                c.send(str(msg).encode('utf-8'))  #发送信息
                file_name = msg_input.split('/*download*/')[1]
            else:
                msg = {'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':msg_input,'operating system':operating_system,'instructions':'None'}
                c.send(str(msg).encode('utf-8'))  #发送信息
            
            # 收到信息的指令执行
            data = ast.literal_eval(c.recv(8192).decode()) #接收信息
            if data != '':
                try:
                    a_ip, b_ip = data['a_ip'], data['b_ip'] # 通过分割获取发送者ip和接收者ip分别赋值给a_ip和b_ip   {String}
                    if 'run' == data['instructions']:
                        if cmd_open == True:
                            instructions.run_cmd(data,a_ip)
                        else:
                            c.send(str({'a_ip':intranet_ip,'b_ip':opposite_ip,'msg':str(a_ip)+"didn't open the cmd",'operating system':operating_system,'instructions':'None'}).encode('utf-8'))
                            print("you didn't open the cmd")
                            data = c.recv(8192).decode()
                    elif 'download' == data['instructions']:
                        instructions.download(data,a_ip,b_ip)
                    elif 'file' == data['instructions']:
                        instructions.file_download()
                    else:
                        instructions.monitor(a_ip,data,b_ip)
                except Exception as e:
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
clisten.clisten_setup('127.0.0.1',3030)
clisten.clisten_start()
