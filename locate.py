import os
import subprocess

# Terminal commands in use
wlan0_down = "sudo ifconfig wlan0 down"
wlan0_mode = "sudo iwconfig wlan0 mode monitor"
wlan0_up = "sudo ifconfig wlan0 up"
tshark_start = "sudo tshark -i wlan0 -Y wlan.fc.type_subtype==0x08 -T fields -e frame.time -e wlan.bssid -e radiotap.dbm_antsignal -e wlan_mgt.ssid -a duration:6"
tshark_fields = ""
tshark_end = ""

# Setup wlan interfaces
#os.system(wlan0_down)
#os.system(wlan0_mode)
#os.system(wlan0_up)
print "Wlan interfaces ready."

# Redirect tshark output using subprocess
proc = subprocess.Popen([tshark_start + tshark_fields + tshark_end], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print "output:\n", out

results = out.split("\n")
print "split:"
print "\n".join(results)
