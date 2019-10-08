CREATE TABLE `tokens` (
  `id` int(10) unsigned PRIMARY KEY AUTO_INCREMENT,
  `owner` varchar(20) NOT NULL,
  `token` varchar(100) NOT NULL,
  `stem` varchar(100) NOT NULL,
  `frequency` int(10) unsigned NOT NULL,
  `syllables` tinyint(3) unsigned NOT NULL,
  KEY `owner` (`owner`),
  KEY `token` (`token`),
  KEY `stem` (`stem`),
  KEY `syllables` (`syllables`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;