[Unit]
Description=tg_clientmgr Service
After=network.target

[Service]
Type=forking
ExecStart=/etc/init.d/tg_clientmgr start
ExecStop=/etc/init.d/tg_clientmgr stop
ExecReload=/etc/init.d/tg_clientmgr reload
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target