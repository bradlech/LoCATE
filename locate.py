import os
import time
import subprocess
import MySQLdb
import socket
import fcntl
import struct

def main():
    # Setup wlan interfaces
    setup_monitor()

    # Infinitely loop the packet capture and data push
    prev_distance = 0
    while (1):
        pcap = run_tshark().split("\n")
        # Process data if packets were captured
        if len(pcap) > 1:
            data = get_data(pcap)
            curr_distance = data[3]
            difference = abs(curr_distance - prev_distance)
            print "Change in Distance: ", difference
            # If the edge node distance (in feet) has changed, push data
            if difference >= 10 and data[3] != -1:
                push_data(data)
                prev_distance = data[3]

        # Wait a period of time
        print "Wait...\n\n",
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
    # TShark commands in use
    tshark_start = "tshark -i wlan1 -Y wlan.fc.type_subtype==0x08 -T fields "
    tshark_fields = "-e frame.time -e wlan.bssid -e radiotap.dbm_antsignal -e wlan_mgt.ssid "
    tshark_end = "-a duration:3"

    # Redirect TShark output using subprocess
    print "Running tshark capture..."
    proc = subprocess.Popen([tshark_start + tshark_fields + tshark_end], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print "Tshark capture complete.\n"
    #print "Captured data:\n", out

    return out

def get_data(pcap):
    # Get data for a particular wireless access point (WAP) by checking for its MAC
    data = [" ", " ", " ", -1, " "]
    for wap in pcap:
        if len(wap) > 1 and wap.split("\t")[1] == "FF:FF:FF:FF:FF:FF":
            print "MATCH: " + wap
            # Get node distance (in feet) from WAP
            rssi = wap.split("\t")[2]
            rssi = abs(int(rssi))
            distance = (0.161 * (2.71828 ** (0.0808 * rssi)))
            distance = round(distance, 1)
            # Set data values
            data = [wap.split("\t")[0],
                    wap.split("\t")[1],
                    wap.split("\t")[2],
                    distance,
                    wap.split("\t")[3]]

    return data

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
        )[20:24])

def push_data(data):
    # Database parameters in use
    db_endpoint = "<endpoint>"
    db_user = "<username>"
    db_pass = "<usernme_pass>"
    db_database = "<database_name>"

    # Get node IP
    node = get_ip_address("wlan0")

    # Setup the database connection (link, user, pass, database)
    print "Setting up the database connection..."
    conn = MySQLdb.connect(db_endpoint, db_user, db_pass, db_database)
    cursor = conn.cursor()
    print "Database connection setup complete.\n"

    # Push the new row to the table
    print "Pushing data..."
    cursor.execute("INSERT INTO test01 (time, mac, rssi, distance, ssid, node) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (data[0],
                    data[1],
                    data[2],
                    data[3], # Calculated distance
                    data[4],
                    node)) # Node IP address
    conn.commit()
    conn.close
    print "Data push complete.\n"

if __name__ == "__main__":
    main()
