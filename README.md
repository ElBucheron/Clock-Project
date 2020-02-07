# Clock-Project

## Requirements

- Raspberry pi
- Led pannel (8x32)

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
* 2 beige
* 3 rose
* 4 gris
* 5 gris fonce
* 6 jaune
* 7 orange
* 8 rouge
* 9 marron
* 10 marron fonce
* 11 violet
* 12 bleu
* 13 bleu fonce
* 14 vert
* 15 vert fonce
