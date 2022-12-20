# simple-tunnel
Simple SSH tunnel manager. Utilises systemd user services to create daemon processes. Useful for accessing remote kubernetes clusters via Lens

## Requirements
* Systemd
* SSH
* Python3

## Usage
### Create new tunnel
Create a tunnel from 10.8.12.4:80 to localhost:6000
```
python simple-tunnel.py --name test-tunnel --local_port 6000 --ext_ip 10.8.12.4 --ext_port 80
```

Create a tunnel from 10.8.12.4:80 to localhost:6000 which jumps via some.proxy.com
```
python simple-tunnel.py --name test-tunnel --local_port 6000 --ext_ip 10.8.12.4 --ext_port 80 --proxy some.proxy.com
```

### List running tunnel services
```
python simple-tunnel.py --list
```

## Possible future additions
* Check for overwriting
* Added error message propagation
* Add management of tunnels e.g deletion
* GUI
    * Tray icon
    * Notifications on fail

## Current limitations
* Only supports key-based access

