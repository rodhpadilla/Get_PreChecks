#!/usr/bin/env python3

__author__ = "Rodrigo H Padilla"
__email__ = "rodrhern@cisco.com / rod.hpadilla@gmail.com"
__copyright__ = "Copyright (c) 2022 Cisco Systems. All rights reserved."


from netmiko import ConnectHandler
from devices import device_list
import time

def backup_config(device, command_list, date):
    file_name = f"{device['host']}_{date}.txt"
    with ConnectHandler(**device) as net_connect:
        with open(file_name, "w") as file_command_outputs:
            file_command_outputs.write(f"Device: {device['host']}\n")
            for command in command_list:
                output_command = net_connect.send_command(command, expect_string=r"#")
                file_command_outputs.write("\n\n")
                file_command_outputs.write(f" {command} ".center(90, "="))
                file_command_outputs.write("\n")
                file_command_outputs.write(f"\n{output_command}")
    return f"SUCCESS --> {device['host']}"


def main():
    date = str(time.strftime("%Y-%d-%m"))
    commands = [
        "show clock",
        "show int description",
        "show ip interface brief",
        "show ip route",
        "show inventory",
        "show run",
    ]
    for device in device_list:
        result_connect = backup_config(device, commands, date)
        if "SUCCESS" in result_connect:
            print(result_connect)
        else:
            print(f"FAILED --> {device['host']}")


if __name__ == '__main__':
    main()