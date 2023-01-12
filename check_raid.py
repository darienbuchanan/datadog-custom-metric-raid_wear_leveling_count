#!/usr/bin/env python3
import subprocess
import re

#generic list of ssd disks on host
disk_list = [0,1,2,3,4,5]
#will be used to create key
disk = 'raid'

def getraidwear():  
    #iterate through disk_list
    for x in disk_list:
        #execute subprocess command to get wear level count for each disk
        p1 = subprocess.Popen(["sudo", "smartctl", "-a", "-d", "sat+megaraid,"+ str(x) , "/dev/sdb"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "Wear_Leveling_Count"],
             stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p3 = subprocess.Popen(["awk", "{{print $4}}"],
             stdin=p2.stdout,stdout=subprocess.PIPE)
        p2.stdout.close()
        output = p3.communicate()[0]
        #removing any extra characters
        output1 = re.sub("[^0-9]", "", str(output)) 
        
        #assign disk and raid_value from subcommand output
        raid_value = output1
        raid = disk + str(x)
        if raid_value != '':
            print(raid+':'+raid_value)

getraidwear()
