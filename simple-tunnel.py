'''Simple python script for simplifying creation of systemd services for SSH tunnels
'''
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ext_ip", required=True, help="External IP address")
    parser.add_argument("--ext_port", required=True, help="External port")
    parser.add_argument("--local_port", required=True, help="Local port")
    parser.add_argument("--name", required=True, help="Name of the connection")
    parser.add_argument("--proxy", required=False, default="", help="A proxy jump")

    options = parser.parse_args()

    template = f'''[Unit]
Description=SSH tunnel for {options.name}

[Service]
ExecStart=/usr/bin/ssh -N -L localhost:{options.local_port}:{options.ext_ip}:{options.ext_port} -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=3 -p 22  {options.proxy}
RestartSec=5
Restart=always


[Install]
WantedBy=default.target'''
    with open(os.path.expanduser(f"~/.config/systemd/user/simple-tunnel-{options.name}.service"), "w") as f:
        f.write(template)
    
    os.system(f"systemctl --user start simple-tunnel-{options.name}")
    

