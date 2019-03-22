#! /usr/bin/env python3

device_list = ["192.168.35.101",
               "192.168.35.102",
               "192.168.35.103",
               "192.168.35.104"]
import netmiko
#定义一个参数
def int_description(device_ip):
    print("#"*10)
    print("开始连接设备{}".format(device_ip))
    connection = netmiko.Netmiko(ip = device_ip,
                                 username = "yyn",
                                 password = "cisco123",
                                 device_type = "cisco_ios",
                                 secret = "cisco123")

    connection.enable()
    print("")
    print("获取邻居信息")
    cdp = connection.send_command("show cdp neighbor detail")

    #for in提取数据

    for i in cdp.split("-------------------------"):
        if i == '':
            continue
        cdp_split=i.split("\n")
        for j in cdp_split:
            if "Device ID" in j:
                remote_device = j.split(":")[1]
            elif "Platform" in j:
                remote_platform = j.split(", ")[0].split(": ")[1]
                continue
            elif "Interface:" in j:
                local_interface = j.split(", ")[0].split(": ")[1]
                remote_interface = j.split(", ")[1].split(": ")[1]
        #输出信息到屏幕

        print("")
        print("接口{0}的邻居信息为{1} {2} {3}".format(local_interface,remote_device,remote_platform,remote_interface))
        print("")
        print("检查接口是否已存在description配置")
        int_desc_check = connection.send_command("show run interface {} | include dsescription".format(local_interface))

        if int_desc_check == "":
            print("")
            print("当前接口无接口描述，开始添加接口描述")
            connection.send_config_set(["interface {}".format(local_interface),
                                     "description To {} {} {}".format(remote_device,
                                                                      remote_interface,
                                                                      remote_platform)])
        else:
            print("")
            print("当前接口存在description描述，内容为{}".format(int_desc_check),"no description")

            print("未添加接口描述，继续执行")

    connection.save_config()
    print("")
    print("执行完毕，断开设备连接")
    connection.disconnect()

for each_device in device_list:
    int_description(each_device)

