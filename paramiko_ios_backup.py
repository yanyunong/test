#! /usr/bin/env python3
import paramiko
import openpyxl
import os
import time


ssh_port = 22
ssh_user = "cisco"
ssh_passwd = "cisco123"

commands = ["enable",
            "cisco123",
            "terminal length 0",
            "show running-config"]

device_list_dict = {}
std_out = []

print("\n开始加载excel表格内容")
zichan = openpyxl.load_workbook("资产.xlsx")
cisco_sheet = zichan.get_sheet_by_name("思科")

i = 2
while i <= cisco_sheet.max_row:
    device_list_dict[cisco_sheet["a"+str(i)].value] = cisco_sheet["d"+str(i)].value

    i+=1
print("\nexcel读取完毕，关闭")
zichan.close()


for hostname,hostip in device_list_dict.items():
    print("#"*10)
    print("\n开始SSH连接设备{}，获取配置".format(hostname))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostip,port=ssh_port,username=ssh_user,password=ssh_passwd,look_for_keys=False)
    terminal = ssh_client.invoke_shell()

    for each_command in commands:
            terminal.send(each_command+"\n")
            time.sleep(1)
            std_out.append(terminal.recv(65535).decode("utf-8"))
    print("\n{}设备配置获取成功，返回配置...".format(hostname))
    terminal.close()
    ssh_client.close()
    print("\n创建{}文件夹".format(hostname))
    config_file = open("/home/yyn/python/ios_backup/" + hostname + ".txt",'w')

    for each_output in std_out:
        config_file.write(each_output+"\n")
    std_out.clear()    
    config_file.close()
    

print("#"*10)
print("\n配置备份完毕，文件列表如下")
print(os.system("ls /home/yyn/python/ios_backup/ -ltr"))