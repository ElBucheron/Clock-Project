# Clock-Project

## Requirements

- Raspberry pi
- Led pannel (8x32)
- [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython)
- Enable SPI on the pi configs

Python modules:
- pendulum

## To add as a startup service
In /lib/systemd/system, create a file `horloge.service` with:
```
[Unit]
Description=My Clock Screen Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /root/Clock-Project/horloge.py > /root/Clock-Project/logs.log

[Install]
WantedBy=multi-user.target
```

Then using the commands:

```
# systemctl daemon-reload
# systemctl enable horloge.service
```

## Colors

The colors are written in hexadecimal before beeing converted on an RGB format inside the code
