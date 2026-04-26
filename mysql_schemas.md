mysql> show tables;
+---------------------+
| Tables_in_appdbproj |
+---------------------+
| attendee            |
| company             |
| registration        |
| room                |
| session             |
+---------------------+
5 rows in set (0.05 sec)


mysql> Describe attendee;
+-------------------+-----------------------+------+-----+---------+-------+
| Field             | Type                  | Null | Key | Default | Extra |
+-------------------+-----------------------+------+-----+---------+-------+
| attendeeID        | int                   | NO   | PRI | NULL    |       |
| attendeeName      | varchar(100)          | NO   |     | NULL    |       |
| attendeeDOB       | date                  | NO   |     | NULL    |       |
| attendeeGender    | enum('Male','Female') | NO   |     | NULL    |       |
| attendeeCompanyID | int                   | NO   | MUL | NULL    |       |
+-------------------+-----------------------+------+-----+---------+-------+
5 rows in set (0.05 sec)

---------------------------------+
| attendee | CREATE TABLE `attendee` (
  `attendeeID` int NOT NULL,
  `attendeeName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attendeeDOB` date NOT NULL,
  `attendeeGender` enum('Male','Female') COLLATE utf8mb4_unicode_ci NOT NULL,
  `attendeeCompanyID` int NOT NULL,
  PRIMARY KEY (`attendeeID`),
  KEY `attendeeCompanyID` (`attendeeCompanyID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+----------+--------------------------------------------------------


mysql> describe company;
+-------------+--------------+------+-----+---------+-------+
| Field       | Type         | Null | Key | Default | Extra |
+-------------+--------------+------+-----+---------+-------+
| companyID   | int          | NO   | PRI | NULL    |       |
| companyName | varchar(100) | NO   |     | NULL    |       |
| industry    | varchar(60)  | NO   |     | NULL    |       |
+-------------+--------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

--------------------------------------------------------------------------------------------+
| company | CREATE TABLE `company` (
  `companyID` int NOT NULL,
  `companyName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `industry` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`companyID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+---------+------------------------------------------------------------


mysql> describe registration
    -> ;
+----------------+----------+------+-----+---------+-------+
| Field          | Type     | Null | Key | Default | Extra |
+----------------+----------+------+-----+---------+-------+
| registrationID | int      | NO   | PRI | NULL    |       |
| attendeeID     | int      | NO   | MUL | NULL    |       |
| sessionID      | int      | NO   | MUL | NULL    |       |
| registeredAt   | datetime | NO   |     | NULL    |       |
+----------------+----------+------+-----+---------+-------+
4 rows in set (0.00 sec)

-------------------------------------------------------------------------------------------------------------------------------------------------+
| registration | CREATE TABLE `registration` (
  `registrationID` int NOT NULL,
  `attendeeID` int NOT NULL,
  `sessionID` int NOT NULL,
  `registeredAt` datetime NOT NULL,
  PRIMARY KEY (`registrationID`),
  KEY `attendeeID` (`attendeeID`),
  KEY `sessionID` (`sessionID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+--------------+---------------------------------------------------------


mysql> describe room;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| roomID   | int         | NO   | PRI | NULL    |       |
| roomName | varchar(80) | NO   |     | NULL    |       |
| capacity | int         | NO   |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+


------------------------------------------+
| room  | CREATE TABLE `room` (
  `roomID` int NOT NULL,
  `roomName` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `capacity` int NOT NULL,
  PRIMARY KEY (`roomID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |
+-------+---------------------------------------------------------------

mysql> describe session;
+--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| sessionID    | int          | NO   | PRI | NULL    |       |
| sessionTitle | varchar(150) | NO   |     | NULL    |       |
| speakerName  | varchar(100) | NO   |     | NULL    |       |
| sessionDate  | date         | NO   |     | NULL    |       |
| roomID       | int          | NO   | MUL | NULL    |       |
+--------------+--------------+------+-----+---------+-------+

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| session | CREATE TABLE `session` (
  `sessionID` int NOT NULL,
  `sessionTitle` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `speakerName` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sessionDate` date NOT NULL,
  `roomID` int NOT NULL,
  PRIMARY KEY (`sessionID`),
  KEY `roomID` (`roomID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |



