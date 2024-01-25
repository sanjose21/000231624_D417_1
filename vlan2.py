import paramiko

# Device IPs
DEVICE_IPS = ['10.10.1.5', '10.10.1.6', '10.10.1.7', '10.10.1.8']
USERNAME = "admin"
PASSWORD = ""

# Initialize the SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Function to get VLANs from a device and append to a file
def get_vlans(ip_address, file_name):
    try:
        # Connect to the device
        ssh_client.connect(hostname=ip_address, username=USERNAME, password=PASSWORD, look_for_keys=False, allow_agent=False)
       
        # Execute the command to show VLANs
        stdin, stdout, stderr = ssh_client.exec_command("show vlan")
       
        # Read the command output
        output = stdout.read().decode()
       
        # Print the output to the console
        print(f"Output of 'show vlan' for {ip_address}:")
        print(output)
       
        # Append the output to the specified file
        with open(file_name, 'a') as file:
            file.write(f"--- VLAN details for {ip_address} ---\n")
            file.write(output + "\n\n")
       
        print(f"VLAN details for {ip_address} have been appended to {file_name}")
   
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {ip_address}, please verify your credentials.")
    except paramiko.SSHException as sshException:
        print(f"Could not establish SSH connection to {ip_address}: {sshException}.")
    except Exception as e:
        print(f"Failed to connect to {ip_address} due to {e}.")
    finally:
        # Close the SSH Client
        ssh_client.close()

# File to store all VLAN details
combined_file_name = "Access_Closet_1_on_the_10.10.1.1_network_vlans.txt"

# Clear the file if it already exists
open(combined_file_name, 'w').close()

# Iterate over the device IPs, get VLANs from each, and append to the file
for ip in DEVICE_IPS:
    get_vlans(ip, combined_file_name)
