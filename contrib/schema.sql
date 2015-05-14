


CREATE DATABASE `simple_review` /*!40100 DEFAULT CHARACTER SET utf8 */;



DROP TABLE IF EXISTS `simple_review`.`project`;
CREATE TABLE  `simple_review`.`project` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `alias` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `url` varchar(512) NOT NULL,
  `target` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

