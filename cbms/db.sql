/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - cbms
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`cbms` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `cbms`;

/*Table structure for table `bank` */

DROP TABLE IF EXISTS `bank`;

CREATE TABLE `bank` (
  `bank_id` int(11) NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(100) NOT NULL,
  `ifsc` varchar(50) NOT NULL,
  `pin` int(11) NOT NULL,
  `accountno` varchar(100) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`bank_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `bank` */

/*Table structure for table `bus` */

DROP TABLE IF EXISTS `bus`;

CREATE TABLE `bus` (
  `bus_id` int(11) NOT NULL AUTO_INCREMENT,
  `bus_regno` varchar(50) NOT NULL,
  `bus_no` int(11) NOT NULL,
  `bus_name` varchar(50) NOT NULL,
  `bus_image` varchar(200) NOT NULL,
  `seat` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`bus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

/*Data for the table `bus` */

insert  into `bus`(`bus_id`,`bus_regno`,`bus_no`,`bus_name`,`bus_image`,`seat`,`status`) values 
(19,'3',45,'fjgsi','adminhome.jpg',67,'active');

/*Table structure for table `driver` */

DROP TABLE IF EXISTS `driver`;

CREATE TABLE `driver` (
  `driver_id` int(11) NOT NULL AUTO_INCREMENT,
  `driver_no` int(11) NOT NULL,
  `driver_name` varchar(20) NOT NULL,
  `driver_address` varchar(100) NOT NULL,
  `driver_image` varchar(200) NOT NULL,
  `driver_email` varchar(50) NOT NULL,
  `driver_mobile` bigint(11) NOT NULL,
  `driver_license` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`driver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `driver` */

insert  into `driver`(`driver_id`,`driver_no`,`driver_name`,`driver_address`,`driver_image`,`driver_email`,`driver_mobile`,`driver_license`,`status`) values 
(1,1,'raj','asdaaaaaa','20220911124849.jpg','adasd',4323,332356789,'current'),
(2,1,'raammrr','sfsefe','Screenshot_26.png','sfvdfdfghjk',2147483647,898798,'current');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `feedback` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `response` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`user_id`,`feedback`,`date`,`response`) values 
(1,1,'hyy','2022-09-07','asdfghjkl'),
(2,2,'bus route ','2022-09-14','zxcvbnm,'),
(3,15,'werrtyui','2022-10-10','pending');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `usertype` varchar(20) NOT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','123','admin'),
(15,'anu_22','Anu2022','user'),
(16,'Amrutha','Amrutha2000','user');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`notification_id`,`notification`,`date`) values 
(2,'Bus late by 100 mins','2022-10-03'),
(4,'Pay the fees on or before 05-10-22','2022-10-10'),
(5,'Tomorrow no bus service','2022-10-10');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `pay_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `stop_id` int(11) NOT NULL,
  `month` varchar(20) NOT NULL,
  `amount` float NOT NULL,
  `datetime` datetime NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`pay_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

/*Table structure for table `registration` */

DROP TABLE IF EXISTS `registration`;

CREATE TABLE `registration` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `mobile` bigint(11) NOT NULL,
  `address` varchar(100) NOT NULL,
  `college` varchar(50) NOT NULL,
  `category` varchar(10) NOT NULL,
  `department` varchar(30) DEFAULT NULL,
  `designation` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `registration` */

insert  into `registration`(`user_id`,`login_id`,`name`,`email`,`mobile`,`address`,`college`,`category`,`department`,`designation`) values 
(10,15,'Aneetha','aneetha22@gmail.com',8848644022,'Padinjare Valathil (H),  Chathamangalam PO, Rec Nit, 673601','KMCT School of Business','Student','MCA','3'),
(11,16,'Amrutha','amrutha20@gmail.com',9349494949,'Valathil (H),  Kunnamangalam PO, Rec Nit, 673601','KMCT College of Engineering','Student','MBA','4');

/*Table structure for table `route` */

DROP TABLE IF EXISTS `route`;

CREATE TABLE `route` (
  `route_id` int(11) NOT NULL AUTO_INCREMENT,
  `route_no` int(11) NOT NULL,
  `route_code` varchar(30) NOT NULL,
  `route_name` varchar(50) NOT NULL,
  PRIMARY KEY (`route_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

/*Data for the table `route` */

insert  into `route`(`route_id`,`route_no`,`route_code`,`route_name`) values 
(23,1,'KMCT1','KMCT-MAL-CLT'),
(24,2,'KMCT2','KMCT-MED-CLT');

/*Table structure for table `stop` */

DROP TABLE IF EXISTS `stop`;

CREATE TABLE `stop` (
  `stop_id` int(11) NOT NULL AUTO_INCREMENT,
  `route_id` int(11) NOT NULL,
  `stop_name` varchar(30) NOT NULL,
  `stop_fees` int(11) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `mrngtime` time NOT NULL,
  `evngtime` time NOT NULL,
  PRIMARY KEY (`stop_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `stop` */

insert  into `stop`(`stop_id`,`route_id`,`stop_name`,`stop_fees`,`latitude`,`longitude`,`mrngtime`,`evngtime`) values 
(17,23,'new bus stand',1750,11.2582,75.7865,'11:59:00','22:59:00'),
(18,24,'kmct',250,11.3122,75.9545,'10:53:00','18:53:00'),
(19,23,'Malaparamb',1400,11.2857,75.8115,'11:00:00','20:55:00'),
(20,23,'asdfgh',2345,1234.46,12345.5,'12:35:00','18:52:00');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
