# datadog-custom-metric-raid_wear_leveling_count
Summary: custom check will send the raid wear_leveling_count to datadog for each disk(0-5) on each target host.

**Description**:
This custom check will send the raid wear_leveling_count to datadog for each disk(0-5) on each target host. The command to run manually is for raid disk 2 is: smartctl -a -d sat+megaraid,2 /dev/sdb | grep Wear_Leveling_Count | awk '{print $4}'

**For more information please see 'Custom Metric: raid wear_leveling_count' in confluence**: https://scratchfoundation.atlassian.net/wiki/spaces/IBE/pages/edit-v2/258539533

**How does custom check custom_raidwearcheck work**:
In summary, the cron job executes check_raid.py and generates/modifies the raidwear.txt file which is then read by the custom_raidwearcheck.py. The custom_raidwearcheck.py script first checks the last_modified_date of the raidwear.txt file to ensure it is less than the current time minus one hour. If the raidwear.txt file is current, loop through and send wear_level_metric for each disk where value != ''. 
*note: a file was used because the ‘check_raid.py' subprocess command did not work when in 'custom_raidwear’, datadog customer service spent a week and did not find out why this is…

**How to add custom Custom Metric: raid wear_leveling_count to host**:
1. Connect to Markley      
2. ssh into bastion server: ssh -i /Users/dbuchanan/.ssh/id_ed25519 darien@cat.scratch.mit.edu 
3. ssh into target mysqlxx server
4. copy file custom_raidwearcheck.yaml to: /etc/datadog-agent/conf.d/custom_raidwearcheck.yaml 
5. copy check_raid.py file to: /etc/datadog-agent/checks.d/check_raid.py
6. make .py executable: chmod +x check_raid.py 
7. open up permissions: chmod 777 /etc/datadog-agent/conf.d/custom_raidwearcheck.yaml 
8. open up permissions: chmod 777 check_raid.py 
9. test check_raid.py: ./check_raid.py 
10. create cron job that creates txt file: crontab -e
*#job populates the etc/datadog-agent/checks.d/raidwear.txt file which is needed for custom_raidwearcheck.py in the same folder
*0 * * * * /usr/bin/python3 /etc/datadog-agent/checks.d/check_raid.py > /etc/datadog-agent/checks.d/raidwear.txt

***Muy Importante: cron job required for populating input file***
note: this will run every hour (test file creation with * * * * * (updates file every minute which is useful for testing)
note: for trouble shooting use the following to see any errors if any ‘grep check_raid /var/log/syslog’

11. create datadog check: vim custom_raidwearcheck.py
12. restart agent: sudo systemctl restart datadog-agent
13. Check log: grep 'custom_raidwearcheck' /var/log/datadog/agent.log
Example of check that worked:
14. verify in Datadog:
-datadog Metrics Summary screen
  https://app.datadoghq.com/metric/summary?filter=wear.level

-datadog Metrics Explorer Page
  https://app.datadoghq.com/metric/explorer?start=1673550441479&end=1673554041479&paused=false#N4Ig7glgJg5gpgFxALlAGwIYE8D2BXJVEADxQEYAaELcqyKBAC1pEbghkcLIF8qo4AMwgA7CAgg4RKUAiwAHOChASAtnADOcAE4RNIKtrgBHPJoQaUAbVBGN8qVoD6gnNtUZCKiOq279VKY6epbINiAiGOrKQdpYZAYgUJ4YThr42gDGSsgg6gi6mZaBZnHKGABuMMjaGNAADAB0YHAY2o1ocBVwaMAAVDwABABGWIPAjDgaCDwgfKCR0bmxWABMickIqel4WTl5iIXFICvlVTV1UGTNre2d3b0DI2MTUzNzFAtR+ysAzBspNIZbLKfJHRKnXKVaq1aCrG5tDpdHr9IajcaTaazeYRb4xUpYAAsAK2QN2INyYIgRQhBLOMMuvwRd2RjzRL0x7xxix+BIArCTtsD9lSaSUdDQoedYVBCcykQ9Uc8MW9sZ9cUsTgSAGyCsl7UGHanHSEgaEXaB8+X3FFPdGvLFzAC6VFc7jwmFC4Tdqg9GHxEoSOJ9foDcXWwbcvswYaw-0j7pjywJxIT0f9yYlArToczcV1PBdIGmWE6MhA8gwnQQCH2UBwMCcmU9GmpiTQojgTjkimU6Q7UHbnac9CYyhEUarHySEHsmCw3YU+w7IiUhZ4fGL8g7CAAwlJhDAUCIPWgeEA

-dashboard- mysql-raid-wear_level_count
  https://app.datadoghq.com/dashboard/7eb-csk-akr?from_ts=1673564028797&to_ts=1673567628797&live=true  

 *References: Writing a Custom Agent Check 
 *https://docs.datadoghq.com/developers/custom_checks/write_agent_check/
