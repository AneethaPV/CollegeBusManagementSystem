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

/*Table structure for table `bus` */

DROP TABLE IF EXISTS `bus`;

CREATE TABLE `bus` (
  `bus_id` int(11) NOT NULL AUTO_INCREMENT,
  `route_id` int(11) DEFAULT NULL,
  `bus_regno` varchar(50) NOT NULL,
  `bus_no` int(11) NOT NULL,
  `bus_name` varchar(50) NOT NULL,
  `bus_image` varchar(200) NOT NULL,
  `seat` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `available_seat` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`bus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

/*Data for the table `bus` */

insert  into `bus`(`bus_id`,`route_id`,`bus_regno`,`bus_no`,`bus_name`,`bus_image`,`seat`,`status`,`available_seat`) values 
(19,23,'KL 12 BS 1290',1,'Kmct Polytechnic College','b1.jpg',2,'active','0'),
(20,23,'KL 12 BS 1340',2,'KMCT College of Engineering','b2.jpg',2,'active','0'),
(21,24,'KL 12 KH 4567',3,'Kmct Pharmaceuticals College','20221013210120.jpg',5,'active','0'),
(22,0,'KL 12 TH 7890',4,'Kmct School of Business','p3.webp',5,'not active',NULL),
(23,0,'KL 12 UV 4531',5,'Kmct College of Architecture','20221014210336.jpg',5,'not active',NULL);

/*Table structure for table `driver` */

DROP TABLE IF EXISTS `driver`;

CREATE TABLE `driver` (
  `driver_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `driver_name` varchar(20) NOT NULL,
  `driver_address` varchar(100) NOT NULL,
  `driver_image` varchar(200) NOT NULL,
  `driver_email` varchar(50) NOT NULL,
  `driver_mobile` bigint(11) NOT NULL,
  `driver_license` varchar(30) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`driver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `driver` */

insert  into `driver`(`driver_id`,`login_id`,`driver_name`,`driver_address`,`driver_image`,`driver_email`,`driver_mobile`,`driver_license`,`status`) values 
(1,39,'Tony','Kunnil House, Karanthur Kozhikode','d1.jpg','anuaneetha2000@gmail.com',8848644022,'AB 332356789','current'),
(3,40,'Tom','Thamarath house , kunnamangalam , Kozhikode','d2.jpg','raj22@gmail.com',6785433115,'GF 2345678909876','current'),
(5,41,'Chris','Krishna House Mayanad Kozhikode','d3.jpg','krishnan@gmail.com',8848644011,'HR-0619850034761','current'),
(6,42,'Mark','Valathil House Mundikkal Thazham Kozhikode','d4.jpg','brijith6@gmail.com',8848677722,'HR-0619850034761','backup'),
(7,43,'Hemsworth','Parapanpoyil House Kozhikode','20221112121655.jpg','chrishemsworth@gmail.com',9988776655,'HR-0619850034567','backup');

/*Table structure for table `driverbus` */

DROP TABLE IF EXISTS `driverbus`;

CREATE TABLE `driverbus` (
  `driverbus_id` int(11) NOT NULL AUTO_INCREMENT,
  `driver_id` int(11) NOT NULL,
  `bus_id` int(11) NOT NULL,
  `from` date DEFAULT NULL,
  `to` date DEFAULT NULL,
  PRIMARY KEY (`driverbus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `driverbus` */

insert  into `driverbus`(`driverbus_id`,`driver_id`,`bus_id`,`from`,`to`) values 
(4,39,19,'2022-11-18','2022-12-31'),
(5,40,20,'2022-11-18','2022-12-31'),
(6,41,21,'2022-11-18','2022-12-31'),
(7,42,19,'2022-11-12','2022-11-15');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `feedback` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `response` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`login_id`,`feedback`,`date`,`response`) values 
(1,1,'hyy','2022-09-07','hello'),
(2,2,'Available bus route ','2022-09-14','Check bus route in dashboard'),
(3,15,'payment will be late','2022-10-10','Pay before 15-10-22'),
(4,15,'Bus didnt stop','2022-10-10','Sorry for the inconvenience'),
(5,15,'Payment is late','2022-10-11','pending'),
(6,41,'Bus punctured','2022-10-16','pending'),
(7,15,'Payment not done','2022-10-16','pending'),
(8,39,'Bus engine problem','2022-10-16','pending');

/*Table structure for table `leave` */

DROP TABLE IF EXISTS `leave`;

CREATE TABLE `leave` (
  `leave_id` int(11) NOT NULL AUTO_INCREMENT,
  `driver_id` int(11) NOT NULL,
  `reason` varchar(100) NOT NULL,
  `from` date NOT NULL,
  `to` date NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`leave_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `leave` */

insert  into `leave`(`leave_id`,`driver_id`,`reason`,`from`,`to`,`status`) values 
(1,39,'sdfghjk','2022-11-12','2022-11-15','Assigned'),
(2,40,'asdfg','2022-11-20','2022-11-24','pending');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `usertype` varchar(20) NOT NULL,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin','123','admin'),
(15,'anu_22','Anu2022','user'),
(16,'Amrutha','Amrutha2000','user'),
(20,'aisu_34','Aisu2334','user'),
(35,'pvsanan__','Sanan@pv2022','user'),
(36,'briji22','Briji@2001','user'),
(37,'junaid.22','Junaid@20','user'),
(39,'anuaneetha2000@gmail.com','8848644022','driver'),
(40,'raj22@gmail.com','6785433115','driver'),
(43,'chrishemsworth@gmail.com','9988776655','driver'),
(44,'Elka_29875','Elka Ajith22','user'),
(45,'Kavya_34','Kavya@3456','user');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `notification` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`notification_id`,`notification`,`date`) values 
(2,'Bus late by 100 mins','2022-10-03'),
(4,'Pay the fees on or before 05-10-22','2022-10-10'),
(5,'Tomorrow no bus service','2022-10-10'),
(7,'On 10-10-22...Bus will be early by 15 mins','2022-10-09'),
(8,'qwertyui','2022-11-16');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `pay_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `stop_id` int(11) NOT NULL,
  `bus_id` int(11) NOT NULL,
  `year` year(4) NOT NULL,
  `month` varchar(25) NOT NULL,
  `amount` float NOT NULL,
  `datetime` date NOT NULL,
  `status` varchar(15) NOT NULL,
  `pid` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pay_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`pay_id`,`login_id`,`stop_id`,`bus_id`,`year`,`month`,`amount`,`datetime`,`status`,`pid`) values 
(1,15,19,19,2022,'January',1300,'2022-11-12','paid','pay_Kf2NssRrHURrUs'),
(2,15,19,19,2022,'February',1300,'2022-11-12','paid','pay_Kf2P08CF3u9MEf'),
(10,15,17,19,2022,'March',500,'2022-11-16','paid','pay_Kgl6Lyx3Yoa4Tq'),
(13,15,17,19,2022,'April',500,'2022-11-16','paid','pay_KglUxsDuctJaD6'),
(15,15,17,19,2022,'May',500,'2022-11-16','paid','pay_KglWKmFCZ8EvZ0'),
(20,15,17,19,2022,'November',500,'2022-11-20','paid','pay_KiCogi9yNVWZqK'),
(25,15,17,19,2022,'October',500,'2022-11-20','paid','pay_KiD7VFhFMgYMkL');

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
  `bus_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

/*Data for the table `registration` */

insert  into `registration`(`user_id`,`login_id`,`name`,`email`,`mobile`,`address`,`college`,`category`,`department`,`designation`,`bus_id`) values 
(10,15,'Aneetha PV','anuaneetha2000@gmail.com',8848644022,'Padinjare Valathil (H),  Chathamangalam PO, Rec Nit, 673601','KMCT College of Engineering','Student','MCA','3',19),
(11,16,'Amrutha','amrutha20@gmail.com',9349494949,'Valathil (H),  Kunnamangalam PO, Rec Nit, 673601','KMCT College of Engineering','Student','MBA','4',19),
(15,20,'Aiswarya','aisu23566@gmail.com',9876543210,'padanilam house, Kunnamangalam','KMCT College of Engineering for Women','Student','MCA','5',NULL),
(18,35,'Sanan PV','sananpv@gmail.com',7896543210,'Kutipuram Malapuram ','KMCT College of Engineering','Student','MCA','8',NULL),
(19,36,'Briji','briji@gmail.com',8921383950,'Kalathil (H),  Kunnamangalam PO, Rec Nit, 673601','KMCT College of Engineering','Staff','MBA','Teacher',NULL),
(20,37,'Junaid','junaid@gmail.com',8765436790,'Junuveetil (H),  Kutipuram, Malappuram','KMCT College of Teacher Education','Staff','BTECH MECHANICAL ENGINEERING','Teacher',NULL),
(21,44,'Elka Ajith','elka31@gmail.com',6754367281,'Sumi house,  Kunnamangalam PO Near Church','KMCT College of Architecture','Staff','BARCH','Teacher',NULL),
(22,45,'Kavya ','kavya34@gmail.com',9061697367,'Kavil (h), Kovoor Po, Calicut','KMCT School of Business','Student','MCA','4',NULL);

/*Table structure for table `route` */

DROP TABLE IF EXISTS `route`;

CREATE TABLE `route` (
  `route_id` int(11) NOT NULL AUTO_INCREMENT,
  `route_no` int(11) NOT NULL,
  `route_code` varchar(30) NOT NULL,
  `route_name` varchar(50) NOT NULL,
  PRIMARY KEY (`route_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

/*Data for the table `route` */

insert  into `route`(`route_id`,`route_no`,`route_code`,`route_name`) values 
(23,1,'COEMPCLT','KMCT-MALAPARAMP-CALICUT'),
(24,2,'COEMCCLT','KMCT-MEDICAL COLLEGE-CALICUT'),
(26,3,'COEOSTSY','KMCT-OMASSERY-THAMARASSERY'),
(29,4,'COEKDDBSY','KMCT-KODUVALLY-BALUSSERY');

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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;

/*Data for the table `stop` */

insert  into `stop`(`stop_id`,`route_id`,`stop_name`,`stop_fees`,`latitude`,`longitude`,`mrngtime`,`evngtime`) values 
(17,23,'Kallanthode',500,11.318,75.9485,'11:59:00','22:59:00'),
(19,23,'Kunnamangalam',1300,11.3049,75.8771,'11:00:00','20:55:00'),
(23,23,'Moozhikal',1450,11.2953,75.8345,'10:17:00','22:17:00'),
(24,23,'Malaparamb',1600,11.2857,75.8115,'00:00:00','21:17:00'),
(25,23,'Kozhikode',1750,11.2588,75.7804,'00:00:00','21:18:00'),
(26,24,'Kallanthode',250,11.318,75.9485,'00:00:00','21:28:00'),
(27,24,'Kattangal',1100,11.3182,75.9376,'09:29:00','21:29:00'),
(28,24,'Kunnamangalam',1300,11.3049,75.8771,'09:30:00','21:30:00'),
(29,24,'Mundikkal Thazham',1450,11.2858,75.858,'09:32:00','21:32:00'),
(30,24,'Medical College',1600,11.2722,75.8372,'09:33:00','21:33:00'),
(31,24,'Kozhikode',1750,11.2588,75.7804,'09:36:00','21:36:00'),
(32,29,'new bus stand',3456,11.3122,75.7865,'09:47:00','21:47:00');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
