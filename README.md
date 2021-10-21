# pi-connect

`client` pushes info (configure running through systemd/crontab.
`server` displays info through webserver.

### Use case
To simplify setting up a headless Raspberry Pi on WiFi in a new environment without access to the router admin interface.  
To see if a Raspberry Pi is currently online.

### On the Raspberry Pi
1. Install [rwbr/RaspiWiFi](https://github.com/rwbr/RaspiWiFi) for initial WiFi configuration
1. Create a systemd service to start push.py at boot (see client/system/pi-connect.service)
1. Create a cronjob to ping the server every 5 minutes (see client/system/crontab)
1. Place a file named .token in the client directory and write a token in it

### On the server
1. Install Docker and docker-compose
1. Put a copy of the .token file in the server directory
2. `docker build . --tag pi-connect:latest`
3. `docker-compose up`


![server page](/screenshot.png)
