import os
import time
import subprocess
import MySQLdb

def main():
    # Setup wlan interfaces
    setup_monitor()

    # Run a tshark capture then push the data
    while (1):
        results = run_tshark().split("\n")
        push_data(results)

        # Wait a period of time
        print "Wait...\n",
        time.sleep(5)

def setup_monitor():
    # Terminal commands in use
    command_01 = "sudo ifconfig wlan1 down"
    command_02 = "sudo iwconfig wlan1 mode monitor"
    command_03 = "sudo ifconfig wlan1 up"

    # Setup wlan interfaces
    print "Setting up monitor interface..."
    os.system(command_01)
    os.system(command_02)
    os.system(command_03)
    time.sleep(3)
    print "Monitor interface setup complete.\n"

def run_tshark():
    # Terminal commands in use
    tshark_start = "tshark -i wlan1 -Y wlan.fc.type_subtype==0x08 -T fields "
    tshark_fields = "-e frame.time -e wlan.bssid -e radiotap.dbm_antsignal -e wlan_mgt.ssid "
    tshark_end = "-a duration:3"

    # Redirect tshark output using subprocess
    print "Running tshark capture..."
    proc = subprocess.Popen([tshark_start + tshark_fields + tshark_end], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print "Tshark capture complete.\n"
    print "output:\n", out

    return out

def push_data(data):
    # Database parameters in use
    db_endpoint = "endpoint"
    db_user = "username"
    db_pass = "username_pass"
    db_database = "database_name"

    # Setup the database connection (link, user, pass, database)
    print "Setting up the database connection..."
    conn = MySQLdb.connect(db_endpoint, db_user, db_pass, db_database)
    cursor = conn.cursor()
    print "Database connection setup complete.\n"

    # Push the new rows to the table
    print "Pushing data..."
    cursor.execute('INSERT INTO test01 (time, mac, rssi, ssid) VALUES (%s, %s, %s, %s)',
                    (data[0].split("\n")[0].split("\t")[0],
                    data[0].split("\n")[0].split("\t")[1],
                    data[0].split("\n")[0].split("\t")[2],
                    data[0].split("\n")[0].split("\t")[3]
                    ))
    conn.commit()
    conn.close
    print "Data push complete.\n"

if __name__ == "__main__":
    main()
