# Spotipi

### Overview

This project is to display information on 32x32 led matrix from the Spotify web api.

### Getting Started

- Create a new application within the
  [Spotify developer dashboard](https://developer.spotify.com/dashboard/applications) <br />
- Edit the settings of the application within the dashboard.
  - Set the redirect uri to any local url such as http://127.0.0.1/callback
- First step is to ssh to your raspberry pi to clone the repository
- Install python and pip

```
sudo apt install python3-pip
```

- Next go ahead and change into the directory using

```
cd spotipi
```

- Install the software: <br />

```
cd spotipi
sudo bash setup.sh
```

- Edit settings on the web app: <br />

```
navigate to http://<raspberrypi_hostname or ip_address> within a web browser
```

### Useful commands

Restart spotipi service<br />

```
sudo service spotipi restart
```

Tail the logs <br />

```
systemctl status spotipi -f
```

Alternative to the previous command

```
journalctl -u spotipi.service -f
```
