import os
import subprocess
import MySQLdb

# Terminal commands in use
command01 = "sudo iw phy phy0 interface add mon0 type monitor"
command02 = "sudo ifconfig mon0 up"
tshark_start = "tshark -i mon0 -Y wlan.fc.type_subtype==0x08 -T fields "
tshark_fields = "-e frame.time -e wlan.bssid -e radiotap.dbm_antsignal -e wlan_mgt.ssid "
tshark_end = "-a duration:3"

# Setup wlan interfaces
print "Setting up monitor interface..."
os.system(command01)
os.system(command02)
print "Monitor interface setup complete.\n"

# Redirect tshark output using subprocess
print "Running tshark capture..."
proc = subprocess.Popen([tshark_start + tshark_fields + tshark_end], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print "Tshark capture complete.\n"
print "output:\n", out

results = out.split("\n")

# Setup the database connection (link, user, pass, database)
print "Setting up the database connection..."
conn = MySQLdb.connect('<db_endpoint>',
			'db_user',
			'db_user_pass',
			'db_databse')
cursor = conn.cursor()
print "Database connection setup complete.\n"

# Push the new rows to the table
print "Pushing data..."
cursor.execute('INSERT INTO test01 (time, mac, rssi, ssid) VALUES (%s, %s, %s, %s)',
		(results[0].split("\n")[0].split("\t")[0],
		results[0].split("\n")[0].split("\t")[1],
		results[0].split("\n")[0].split("\t")[2],
		results[0].split("\n")[0].split("\t")[3]
		))
conn.commit()
conn.close
print "Data push complete.\n"
