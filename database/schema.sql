CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS `disabled_commands` (
  `server_id` varchar(20) NOT NULL,
  `command` varchar(50) NOT NULL,
  PRIMARY KEY (`server_id`, `command`)
);
CREATE TABLE IF NOT EXISTS `disbaled_cogs` (
  `server_id` varchar(20) NOT NULL,
  `cog` varchar(50) NOT NULL,
  PRIMARY KEY (`server_id`, `cog`)
);
CREATE TABLE IF NOT EXISTS `settings` (
  `server_id` varchar(20) NOT NULL,
  `prefix` varchar(10) NOT NULL DEFAULT '!',
  PRIMARY KEY (`server_id`)
);