'''Simple python script for simplifying creation of systemd services for SSH tunnels
'''
import argparse
import os

def create(options):
    '''Create a systemd user service to run the specified SSH tunnel
    '''
    if not (options.ext_ip and options.ext_port and options.local_port):
        print("Missing options. --ext_ip, --ext_port and --local_port are required to create a tunnel.")
        print("Try --help for troubleshooting.")
        return

    template = f'''[Unit]
Description=SSH tunnel for {options.name}

[Service]
ExecStart=/usr/bin/ssh -N -L {options.local_ip}:{options.local_port}:{options.ext_ip}:{options.ext_port} -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -p 22  {options.proxy}
RestartSec=5
Restart=always


[Install]
WantedBy=default.target'''

    with open(os.path.expanduser(f"~/.config/systemd/user/simple-tunnel-{options.name}.service"), "w") as f:
        f.write(template)
    
    os.system(f"systemctl --user {'enable --now' if options.persist else 'start'} simple-tunnel-{options.name}")


def list_tunnels():
    '''Print the names and statuses of the simple-tunnel services
    '''
    tunnels = os.listdir(os.path.expanduser("~/.config/systemd/user"))
    tunnels = [tunnel for tunnel in tunnels if "simple-tunnel" in tunnel]

    #Get the status of each tunnel
    for service in tunnels:
        ret_code = os.system(f"systemctl --user --quiet is-active {service}")
        if ret_code == 0:
            #Add ANSI colours for green/red appropriately
            status = "\033[1;32mis running.\033[0m"
        else:
            status = "\033[1;31mhas failed.\033[0m"
        print(service.split(".")[0].replace("simple-tunnel-",""), status)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ext_ip", default=None, help="External IP address")
    parser.add_argument("--ext_port", default=None, help="External port")
    parser.add_argument("--local_ip", default="localhost", help="Local IP")
    parser.add_argument("--local_port", default=None, help="Local port")
    parser.add_argument("--name", default=None, help="Name of the connection")
    parser.add_argument("--proxy", default="", help="A proxy jump")
    parser.add_argument("--list", action='store_true', default=False, help="Show the current services")
    parser.add_argument("--persist", action='store_true', default=False, help="Persist the service between reboots")

    options = parser.parse_args()

    if options.list:
        list_tunnels()
    else:
        create(options)
    

