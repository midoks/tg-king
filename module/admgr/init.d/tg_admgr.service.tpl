[Unit]
Description=tg_admgr Service
After=network.target

[Service]
Type=forking
ExecStart=/etc/init.d/tg_admgr start
ExecStop=/etc/init.d/tg_admgr stop
ExecReload=/etc/init.d/tg_admgr reload
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target