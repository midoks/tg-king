[Unit]
Description=tg_admgr Service
After=network.target

[Service]
Type=forking
ExecStart={$APP_PATH}/init.d/tg_admgr start
ExecStop={$APP_PATH}/init.d/tg_admgr stop
ExecReload={$APP_PATH}/init.d/tg_admgr reload
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target