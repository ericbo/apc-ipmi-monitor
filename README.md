# ericbo/apc-ipmi-monitor 
**WARNING!** This is just a prof of concept I created during some free time. It
is not in a state were I would use it in my own homelab yet.

A tool designed for non enterprise APC branded UPS's. This will allow you to define
many IPMI devices across your network and will trigger a graceful shutdown on all
server in the event there is an extended power outage.

## Usage
Assuming you have the dependencies setup bellow, simply execute the `__main__.py`
using python. This was designed to be used as a cron. Future versions will be
ran as a systemctl service.

```
crontab -e

* * * * * python /home/user/upc-ipmi-tool/src/__main__.py #Run every minute
```

## Dependencies
This is presently being developed on Ubuntu 18.04. You will need to have apcupsd
and ipmitool installed for this application to work.

```shell script
sudo apt-get -y install apcupsd
sudo apt-get -y install ipmitool
```

### Running apcupsd

For this to monitor the status of your APC battery **apcupsd** must be running.
Assuming you are using an APC with a single USB connection, make sure `UPSCABLE`
and `UPSTYPE` are both set to usb in your `/etc/apcupsd/apcupsd.conf` file. I
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

