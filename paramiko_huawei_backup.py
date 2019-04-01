#! /usr/bin/env python3
import paramiko
import time
import os
import openpyxl

ssh_port = 22
ssh_user = "yyn"
ssh_passwd = "huawei123"
commands = ["screen-length 0 temporary",
            "display current-configuration"]

#预定义一个空的字典，用于容器存储后续的设备名称和设备ip
device_list_dict={}

#进入openpypl部分
print("\n开始加载excel表格内容。。。")
zichan = openpyxl.load_workbook("资产.xlsx")
huawei_sheet = zichan.get_sheet_by_name("华为")

i = 2
while i <= huawei_sheet.max_row:
    device_list_dict[huawei_sheet["a"+str(i)].value] = huawei_sheet["d"+str(i)].value
    i+=1
print("\nexcel读取完毕，关闭excel表")
zichan.close()

#迭代循环字典里面的key value项，并SSH到设备获取配置，最后存到文件内
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
        #此处把每一个命令执行后的内容通过append功能追加到列表内
        std_out=sterminal.recv(65535).decode("utf-8")
    print("\n{}设备配置获取成功，返回配置...".format(hostname))
    terminal.close()
    ssh_client.close()

    print("\n创建{}文件夹".format(hostname))
    config_file = open("/home/yyn/python/backup/"+ hostname + ".txt","w")
    
    config_file.write(std_output+"\n")
    config_file.close()

print("#"*10)
print("\n程序执行完毕，以下为备份文件列表")
print(os.system("ls /home/yyn/python/backup/ -ltr"))