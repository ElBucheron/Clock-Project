# Clock-Project

## Requirements

- Raspberry pi
- Led pannel (8x32)
- [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython)

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

* 0 noir
* 1 blanc
* 2 jaune
* 3 orange
* 4 rouge
* 5 violet
* 6 bleu clair
* 7 bleu
* 8 vert
