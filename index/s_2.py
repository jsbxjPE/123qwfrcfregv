import socket
import sys
import ast

global msg_server_run
global log_name
global file_name
global log_name_debug
global log_mode
global s

msg_server_run = True
log_mode = False

# 日志
class log():
    def log_setup_msg(host,port):
        global log_name
        global log_name_debug
        global log_mode
        import time
        localtime = time.asctime(time.localtime(time.time()))
        log_name = str('./server_log/{}.log'.format(str(localtime))).replace(':','-')
        log_name_debug = str('./server_log/{} debug.log'.format(str(localtime))).replace(':','-')
        print('log path : {}'.format(log_name))
        print('log path : {}'.format(log_name_debug))
        with open(log_name,'a') as log_msg:
            log_msg.write('log:')
            log_msg.write('\n')
            log_msg.write(str(localtime))
            log_msg.write('start server for host:{} port:{}'.format(host,port))
            log_msg.write('\n')
        with open(log_name_debug,'a') as log_msg:
            log_msg.write('debug log:')
            log_msg.write('\n')
            log_msg.write(str(localtime))
            log_msg.write('start server for host:{} port:{}'.format(host,port))
            log_msg.write('\n')
        log_mode = True
    def log_info_msg(data):
        global log_name
        import time
        localtime = time.asctime(time.localtime(time.time()))
        with open(log_name,'a') as log_msg:
            log_msg.write(str(localtime))
            log_msg.write(' : \n')
            log_msg.write('[INFO] ')
            log_msg.write(data)
            log_msg.write('\n\n')
    def log_debug_server(bug_msg):
        global log_name_debug
        import time
        localtime = time.asctime(time.localtime(time.time()))
        with open(log_name,'a') as log_msg:
            log_msg.write(str(localtime))
            log_msg.write(' : \n')
            log_msg.write('[DEBUG] ')
            log_msg.write(bug_msg)
            log_msg.write('\n\n')

# 消息指令
class instructions():
    def stop_server(data,a_ip):
        global log_mode
        global msg_server_run
        print('{} stop server'.format(a_ip))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} stop server'.format(a_ip))
        stop = False
        sys.exit('{} stop server'.format(a_ip))
    def start_cmd(data,a_ip,c):
        global log_mode
        c.send(str({'a_ip':'msg_server','b_ip':'everyone','operating system':data['operating system']}).encode('utf-8'))
        print('\n{} start cmd for {}'.format(a_ip,data['operating system']))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} start cmd for {}'.format(a_ip,data['operating system']))
    def not_cmd(data,a_ip,c):
        global log_mode
        c.send(str({'a_ip':'msg_server','b_ip':'everyone','operating system':data['operating system'],'instructions':'run'}).encode('utf-8'))
        print('{} stop cmd for {}'.format(a_ip,data['operating system']))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} stop cmd for {}'.format(a_ip,data['operating system']))
    def user_exit(data,a_ip,c):
        global log_mode
        c.send(str({'a_ip':'msg server','b_ip':'everyone','msg':str(a_ip)+' exit','operating system':data['operating system'],'instructions':'None'}).encode('utf-8'))
        print('{} exit'.format(a_ip))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} exit'.format(a_ip))
    def run_cmd_instructions(data,a_ip,b_ip,c,msg):
        global log_mode
        msgdata = (str({'a_ip':a_ip,'b_ip':b_ip,'msg':msg,'operating system':data['operating system'],'instructions':'run'})).encode('utf-8')
        print('{}让{}执行 : {}'.format(a_ip,b_ip,msg['run']))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{}让{}执行 : {}'.format(a_ip,b_ip,msg))
    def msg_to_msg(data,a_ip,b_ip,c,msg):
        global log_mode
        msgdata = (str({'a_ip':a_ip,'b_ip':b_ip,'msg':msg,'operating system':data['operating system'],'instructions':'run'})).encode('utf-8')
        print('{}向{}发送 : {}'.format(a_ip,b_ip,msg))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{}向{}发送 : {}'.format(a_ip,b_ip,msg))
    def file_download(a_ip,b_ip,c,msg,data):
        global log_mode
        global file_name
        file_name = msg['download']
        print(msg)
        msgdata = (str({'a_ip':a_ip,'b_ip':b_ip,'msg':file_name,'operating system':data['operating system'],'instructions':'download'})).encode('utf-8')
        print('{}请求下载{}路径 "{}" 的数据'.format(a_ip,b_ip,file_name))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(msg)
            log.log_info_msg('{}请求下载{}路径 "{}" 的数据'.format(a_ip,b_ip,file_name))
    def file_transmission_server(a_ip,b_ip,c,msg,data):
        global log_mode
        global file_name
        msgdata = (str({'a_ip':a_ip,'b_ip':b_ip,'msg':msg,'operating system':data['operating system'],'instructions':'file'})).encode('utf-8')
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(msg)
            log.log_info_msg('{}发送数据"{}"给{}'.format(a_ip,data[msg],b_ip))

# 服务器    
class server():
    def server_setup(host,port,listen_number):
        global s
        s = socket.socket()
        s.bind((str(host), int(port))) # 绑定ip和端口
        s.listen(listen_number) # 等待客户端连接
    def server_run():
        global msg_server_run
        global file_name
        global log_mode
        while msg_server_run:
            c, addr = s.accept() # 建立客户端连接
            print(c)
            if log_mode:
                log.log_info_msg(str(c))
            while msg_server_run:
                try:
                    data = ast.literal_eval(c.recv(8192).decode()) # 接收客户端信息
                    a_ip, b_ip = data['a_ip'], data['b_ip'] # 通过分割获取发送者ip和接收者ip分别赋值给a_ip和b_ip   (String)
                    msg = data['msg']
                    if data == '':
                        break
                    elif data['instructions'] == 'stop server':
                        instructions.stop_server(data,a_ip)
                    elif data['instructions'] == 'cmd':
                        instructions.start_cmd(data,a_ip,c)
                    elif data['instructions'] == 'not cmd':
                        instructions.not_cmd(data,a_ip,c)
                    elif data['instructions'] == 'user exit':
                        instructions.user_exit(data,a_ip,c)
                    elif data['instructions'] == 'run':
                        instructions.run_cmd_instructions(data,a_ip,b_ip,c,msg)
                    elif data['instructions'] == 'download':
                        instructions.file_download(a_ip,b_ip,c,msg,data)
                    elif data['instructions'] == 'file':
                        instructions.file_transmission_server(a_ip,b_ip,c,msg,data)
                    else:
                        instructions.msg_to_msg(data,a_ip,b_ip,c,msg)
                except Exception as e:
                    if log_mode:
                         log.log_debug_server(repr(e))
                    break

'''
导入s.py文件函数
import s

如果要使用log,则:
s.log.log_setup_msg(host,port) # host {String},port {Int}
不要则不执行

如果要打开服务器,则:
s.server.server_setup(host,port,listen_number) # host {String},port {Int},listen_number {Int}
s.sever.server_run()
不要则不执行

服务器日志存储在./server_log文件夹下
'''
server.server_setup('127.0.0.1',3030,5)
server.server_run()
