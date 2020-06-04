# ericbo/apc-ipmi-monitor 
![Python package](https://github.com/ericbo/apc-ipmi-monitor/workflows/Python%20package/badge.svg)
![Upload Python Package](https://github.com/ericbo/apc-ipmi-monitor/workflows/Upload%20Python%20Package/badge.svg)

**WARNING!** This is just a prof of concept I created during some free time. It
is not in a state were I would use it in my own homelab yet.

A tool designed for non enterprise APC branded UPS's. This will allow you to define
many IPMI devices across your network and will trigger a graceful shutdown on all
servers in the event there is an extended power outage.

## Getting Started
In the system that will be directly interfacing with the APC UPS, you must have
apcupsd and ipmitool installed. On Ubuntu, this can be installed with the following
commands:

```shell script
sudo apt-get -y install apcupsd
sudo apt-get -y install ipmitool
```

### Running apcupsd
For this script to monitor the status of your APC battery **apcupsd** must be running.
Assuming you are using an APC with a single USB connection, make sure `UPSCABLE`
and `UPSTYPE` are both set to **usb** in your `/etc/apcupsd/apcupsd.conf` file. I
would also suggest commenting out `DEVICE /dev/ttyS0`. Example:

```text
## apcupsd.conf v1.1 ##
...
UPSCABLE usb
...
UPSTYPE usb
...
#DEVICE /dev/ttyS0
```

[source](https://www.pontikis.net/blog/apc-ups-on-ubuntu-workstation)

### Running the Monitor
You will need pip installed, specifically pip for python 3. You can then directly
install this package via pypi.org by running the following:

```text
sudo apt-get -y install python3-pip
pip3 install apc-ipmi-monitor-ericbo
```

Next create a simple config file with a list of your servers & credentials:

```yaml
servers:
  server 1:
    hostname: 0.0.0.0
    username: ADMIN
    password: ADMIN
  server 2:
    hostname: 0.0.0.0
    username: ADMIN
    password: ADMIN
apc_shutdown_threshold:
  field: BCHARGE # Which field do you want to consider
  value: 80      # When the field dips bellow this value, all servers will shutdown
```

Finally you can get a quick overview of all your IPMI devices by running:
```text
apc-ipmi-monitor monitoring server-status
```

### Running on Startup
Finally, you will want to ensure this monitor is being ran regularly. I would
suggest using systemctl or crontabs. The example bellow is a simple crontab setup.
In the future there will be a full guide on setting this up with systemctl.

```text
crontab -e

* * * * * python /home/user/upc-ipmi-tool/src/__main__.py # Run every minute
```