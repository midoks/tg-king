CREATE TABLE IF NOT EXISTS `users` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` TEXT,
  `password` TEXT,
  `login_ip` TEXT,
  `login_time` TEXT,
  `phone` TEXT,
  `email` TEXT
);

INSERT INTO `users` (`id`, `username`, `password`, `login_ip`, `login_time`, `phone`, `email`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', '192.168.0.10', '2022-02-02 00:00:00', 0, 'midoks@163.com');


CREATE TABLE IF NOT EXISTS `logs` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `type` TEXT,
  `log` TEXT,
  `uid` TEXT,
  `addtime` TEXT
);
ALTER TABLE `logs` ADD COLUMN `uid` INTEGER DEFAULT '1';


CREATE TABLE IF NOT EXISTS `tg_bot` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `alias` TEXT, 
  `token` TEXT
);


CREATE TABLE IF NOT EXISTS `tg_client` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `app_id` TEXT, 
  `app_hash` TEXT,
  `token` TEXT default '',
  `is_vaild` INTEGER default '0',
  `data` TEXT
);


CREATE TABLE IF NOT EXISTS `module` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT,
  `range_type` INTEGER default '0',
  `range_val` TEXT,
  `config` TEXT,
  `status` TEXT
);
