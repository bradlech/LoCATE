import os
import subprocess

# Terminal commands in use
wlan0_down = "sudo ifconfig wlan0 down"
wlan0_mode = "sudo iwconfig wlan0 mode monitor"
wlan0_up = "sudo ifconfig wlan0 up"
tshark_start = "tshark -i wlan0 -Y wlan.fc.type_subtype==0x08 -T fields "
tshark_fields = "-e frame.time -e wlan.bssid -e radiotap.dbm_antsignal -e wlan_mgt.ssid "
tshark_end = "-a duration:6"

# Setup wlan interfaces
print "Setting up wlan interfaces..."
os.system(wlan0_down)
os.system(wlan0_mode)
os.system(wlan0_up)
print "Wlan interface setup complete."

# Redirect tshark output using subprocess
print "Running tshark capture..."
proc = subprocess.Popen([tshark_start + tshark_fields + tshark_end], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print "Tshark capture complete."
print "output:\n", out

results = out.split("\n")
print "split:"
print "\n".join(results)
