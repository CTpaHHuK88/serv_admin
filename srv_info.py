import os, sys, psutil
import datetime
from psutil._common import bytes2human



def show_date():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

def disk_info():
    templ = "{:<17} {:>8} {:>8} {:>8} {:>5}% {:>9}  {}"
    print(
        templ.format(
            "Device", "Total", "Used", "Free", "Use ", "Type", "Mount"
        )
    )
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or not part.fstype:
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        line = templ.format(
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint,
        )
        print(line)

def main():
    print(f"Система загружена: {show_date()}")
    temps = psutil.sensors_temperatures()
    for name, entries in temps.items():
        for entry in entries:
            print(f"Temperature CPU: {entry.current} C")

            if entry.current > 20:
                bot.send_message(chat_id, 'Температура превышена!')
    
    print(f"CPU usage: {psutil.cpu_percent()} %")
    print(f"RAM usage: {psutil.virtual_memory().percent} %")
    print(f"SWAP free: {bytes2human(psutil.swap_memory().free)} Mb")
    disk_info()
    
bot.polling()

if __name__ == '__main__':
    main()