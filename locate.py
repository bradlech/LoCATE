import os
import subprocess

# Terminal commands in use
tshark = "sudo tshark -i wlan0 -Y wlan.fc.type_subtype==0x08 -T fields -e frame.time -e wlan.bssid -e radiotap.dbm_antsignal -e wlan_mgt.ssid -a duration:6"

# Setup wlan interfaces
#os.system(sudo ifconfig )
Print "Wlan interfaces ready."

# Redirect tshark output using subprocess
proc = subprocess.Popen([tshark], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print "output:\n", out

results = out.split("\n")
print "split:"
print "\n".join(results)
