[Unit]
Description=tg_gpmgr Service
After=network.target

[Service]
Type=forking
ExecStart=/etc/init.d/tg_gpmgr start
ExecStop=/etc/init.d/tg_gpmgr stop
ExecReload=/etc/init.d/tg_gpmgr reload
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target