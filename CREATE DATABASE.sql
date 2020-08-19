/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 8.0.21-0ubuntu0.20.04.4 : Database - worldwar
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`worldwar` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `worldwar`;

/*Table structure for table `admincommands` */

DROP TABLE IF EXISTS `admincommands`;

CREATE TABLE `admincommands` (
  `id` int NOT NULL AUTO_INCREMENT,
  `command` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MEMORY DEFAULT CHARSET=utf8;

/*Table structure for table `dashboard` */

DROP TABLE IF EXISTS `dashboard`;

CREATE TABLE `dashboard` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dash_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dash_data` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `invite` */

DROP TABLE IF EXISTS `invite`;

CREATE TABLE `invite` (
  `iid` int NOT NULL AUTO_INCREMENT,
  `inviter_id` int DEFAULT NULL,
  `invited_id` int DEFAULT NULL,
  `accept_date` datetime NOT NULL,
  PRIMARY KEY (`iid`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;

/*Table structure for table `log` */

DROP TABLE IF EXISTS `log`;

CREATE TABLE `log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `action` json DEFAULT NULL,
  `action_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8;

/*Table structure for table `messages` */

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `msg_id` int NOT NULL AUTO_INCREMENT,
  `msg_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `msg_from` int NOT NULL,
  `msg_to` int NOT NULL,
  `msg_message` varchar(255) NOT NULL,
  `msg_admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`msg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8;

/*Table structure for table `village` */

DROP TABLE IF EXISTS `village`;

CREATE TABLE `village` (
  `vid` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `username` varchar(45) DEFAULT '',
  `first_name` varchar(45) DEFAULT '',
  `last_name` varchar(45) DEFAULT '',
  `name` varchar(45) DEFAULT '',
  `race` varchar(45) CHARACTER SET big5 COLLATE big5_chinese_ci DEFAULT 'Human',
  `score` int NOT NULL DEFAULT '0',
  `food` int NOT NULL DEFAULT '0',
  `gold` int NOT NULL DEFAULT '0',
  `wood` int NOT NULL DEFAULT '0',
  `farm_capacity` int NOT NULL DEFAULT '0',
  `worker` int NOT NULL DEFAULT '0',
  `farm_unit` int NOT NULL DEFAULT '0',
  `worker_randeman` float NOT NULL DEFAULT '1',
  `soldier_skill` float NOT NULL DEFAULT '1',
  `food_price` float NOT NULL DEFAULT '0',
  `wood_price` float NOT NULL DEFAULT '0',
  `home` int NOT NULL DEFAULT '0',
  `home_capacity` int NOT NULL DEFAULT '0',
  `era` int NOT NULL DEFAULT '0',
  `power_attack` int NOT NULL DEFAULT '0',
  `power_defence` int NOT NULL DEFAULT '0',
  `operation` varchar(45) DEFAULT '',
  `operation_time` int DEFAULT '0',
  `tired` int DEFAULT '0',
  `shield` int DEFAULT '0',
  `fast` tinyint NOT NULL DEFAULT '0',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_visit` datetime DEFAULT CURRENT_TIMESTAMP,
  `disabled` tinyint DEFAULT '0',
  `joined_channel` varchar(45) DEFAULT '0',
  PRIMARY KEY (`vid`),
  UNIQUE KEY `vid_UNIQUE` (`vid`),
  UNIQUE KEY `userid` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=227 DEFAULT CHARSET=utf8 DELAY_KEY_WRITE=1 COMMENT='village';

/*Table structure for table `weapons` */

DROP TABLE IF EXISTS `weapons`;

CREATE TABLE `weapons` (
  `vid` int NOT NULL,
  `wid` int NOT NULL DEFAULT '0',
  `wcount` int DEFAULT '0',
  PRIMARY KEY (`vid`,`wid`),
  KEY `index1` (`vid`,`wid`),
  CONSTRAINT `fk_weapons_vid` FOREIGN KEY (`vid`) REFERENCES `village` (`vid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
