# Setting up Pi-Cam-Server


## Get files

```bash
cd /home/pi/
git clone git@github.com:NanoDano/Pi-Cam-Server.git
cd Pi-Cam-Server
python3 -m pip install -r requirements.txt
```

## Setup WSGI server

Symlink the systemd service file to run the WSGI server.

```bash
sudo ln -s /home/pi/Pi-Cam-Server/camserver.service /etc/systemd/system/camserver.service
sudo systemctl enable camserver
sudo systemctl start camserver
```

## Setup Nginx reverse proxy

Modify the nginx config for the localhost to include the paths for this app

```
    # Pi-Cam-Server
    location /camserver/static/ {
        alias /var/www/static-content/;
    }
    location /camserver/ {
        proxy_pass http://localhost:8002/;
        proxy_set_header X-Real-IP $remote_addr;
    }
```