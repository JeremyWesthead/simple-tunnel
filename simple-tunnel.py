'''Simple python script for simplifying creation of systemd services for SSH tunnels
'''
import argparse
import os
import uuid

def create(options):
    '''Create a systemd user service to run the specified SSH tunnel
    '''
    #Check required args exist
    if not (options.ext_ip and options.ext_port and options.local_port):
        print("Missing options. --ext_ip, --ext_port and --local_port are required to create a tunnel.")
        print("Try --help for troubleshooting.")
        return
    
    #Name validation
    if options.name is None:
        #No given name so use a uuid
        name = str(uuid.uuid4())
    else:
        #Name given so check if already exists
        services = os.listdir(os.path.expanduser("~/.config/systemd/user"))
        if f"simple-tunnel-{options.name}.service" in services:
            #Service with this name exists so check for overwriting
            check = str(input("A service with this name already exists! Overwrite? [Y/N] "))
            if check.upper() != "Y":
                return
            else:
                name = options.name

    template = f'''[Unit]
Description=SSH tunnel for {name}

[Service]
ExecStart=/usr/bin/ssh -N -L {options.local_ip}:{options.local_port}:{options.ext_ip}:{options.ext_port} -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -p 22  {options.proxy}
RestartSec=5
Restart=always


[Install]
WantedBy=default.target'''

    with open(os.path.expanduser(f"~/.config/systemd/user/simple-tunnel-{name}.service"), "w") as f:
        f.write(template)
    
    os.popen(f"systemctl --user {'enable --now' if options.persist else 'start'} simple-tunnel-{name}")
    os.system("systemctl --user daemon-reload")


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
            status = "\033[1;31mis not running.\033[0m"
        print(service.split(".")[0].replace("simple-tunnel-",""), status)

def delete(name):
    '''Delete the service specified by the name

    Args:
        name (str): Name of the service
    '''
    #Check a tunnel with this name exists
    services = os.listdir(os.path.expanduser("~/.config/systemd/user"))
    if f"simple-tunnel-{name}.service" not in services:
        print(f"No tunnel found with name {name}")
        return

    #Double check with the user
    check = str(input(f"Really delete the tunnel {name}? [Y/N] "))
    if check.upper() != "Y":
        return
    
    os.popen(f"systemctl --user stop simple-tunnel-{name}.service")
    os.remove(os.path.expanduser(f"~/.config/systemd/user/simple-tunnel-{name}.service"))
    os.system("systemctl --user daemon-reload")

def stop(name):
    '''Stop the tunnel service specified by the name

    Args:
        name (str): Name of tunnel to stop
    '''
    #Check a tunnel with this name exists
    services = os.listdir(os.path.expanduser("~/.config/systemd/user"))
    if f"simple-tunnel-{name}.service" not in services:
        print(f"No tunnel found with name {name}")
        return
    
    #Stop it
    os.popen(f"systemctl --user stop simple-tunnel-{name}.service")

def start(name):
    '''Start the tunnel service specified by the name

    Args:
        name (str): Name of tunnel to start
    '''
    #Check a tunnel with this name exists
    services = os.listdir(os.path.expanduser("~/.config/systemd/user"))
    if f"simple-tunnel-{name}.service" not in services:
        print(f"No tunnel found with name {name}")
        return
    
    #Start it
    os.popen(f"systemctl --user start simple-tunnel-{name}.service")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ext_ip", default=None, help="External IP address")
    parser.add_argument("--ext_port", default=None, help="External port")
    parser.add_argument("--local_ip", default="localhost", help="Local IP")
    parser.add_argument("--local_port", default=None, help="Local port")
    parser.add_argument("--name", default=None, help="Name of the connection")
    parser.add_argument("--proxy", default="", help="A proxy jump")
    parser.add_argument("--list", action='store_true', default=False, help="Show the current services")
    parser.add_argument("--stop", default=None, help="Stop a tunnel by name")
    parser.add_argument("--start", default=None, help="Start a tunnel by name")
    parser.add_argument("--delete", default=None, help="Delete a tunnel by name")
    parser.add_argument("--persist", action='store_true', default=False, help="Persist the service between reboots")

    options = parser.parse_args()

    if options.list:
        list_tunnels()
    elif options.delete:
        delete(options.delete)
    elif options.stop:
        stop(options.stop)
    elif options.start:
        start(options.start)
    else:
        create(options)
    

