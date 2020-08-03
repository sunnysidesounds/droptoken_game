/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table games
# ------------------------------------------------------------

DROP TABLE IF EXISTS `games`;

CREATE TABLE `games` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `columns` int unsigned NOT NULL DEFAULT '0',
  `rows` int unsigned NOT NULL DEFAULT '0',
  `board` json DEFAULT NULL,
  `state` enum('DONE','INPROGRESS') NOT NULL,
  `active_turn` varchar(255) DEFAULT NULL,
  `winner` varchar(255) DEFAULT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;

INSERT INTO `games` (`id`, `name`, `columns`, `rows`, `board`, `state`, `active_turn`, `winner`, `last_updated`)
VALUES
	(1,'e3a0425e-d546-11ea-b86b-8c85904e8d06',4,4,'\"[[0, 0, 0, 0], [0, 0, 0, 0], [0, \\\"2\\\", 0, 0], [\\\"1\\\", \\\"1\\\", \\\"2\\\", 0]]\"','INPROGRESS','testPlayer1','','2020-08-02 22:09:00'),
	(2,'fadc6b1e-d546-11ea-b86b-8c85904e8d06',4,4,'\"[[0, 0, \\\"3\\\", 0], [0, 0, \\\"3\\\", 0], [\\\"4\\\", 0, \\\"3\\\", 0], [\\\"4\\\", 0, \\\"3\\\", \\\"4\\\"]]\"','DONE','','testPlayer3','2020-08-02 22:11:31'),
	(3,'098ebc48-d547-11ea-b86b-8c85904e8d06',4,4,'\"\\\"[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, \\\\\\\"6\\\\\\\", 0], [0, 0, \\\\\\\"5\\\\\\\", 0]]\\\"\"','DONE','','','2020-08-02 22:13:55');

/*!40000 ALTER TABLE `games` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table games_to_players
# ------------------------------------------------------------

DROP TABLE IF EXISTS `games_to_players`;

CREATE TABLE `games_to_players` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `game_id` int unsigned NOT NULL,
  `player_id` int unsigned NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `game_id_constraint_2` (`game_id`),
  KEY `player_id_constraint_2` (`player_id`),
  CONSTRAINT `game_id_constraint_2` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`),
  CONSTRAINT `player_id_constraint_2` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `games_to_players` WRITE;
/*!40000 ALTER TABLE `games_to_players` DISABLE KEYS */;

INSERT INTO `games_to_players` (`id`, `game_id`, `player_id`, `last_updated`)
VALUES
	(1,1,1,'2020-08-02 22:05:03'),
	(2,1,2,'2020-08-02 22:05:03'),
	(3,2,3,'2020-08-02 22:05:42'),
	(4,2,4,'2020-08-02 22:05:42'),
	(5,3,5,'2020-08-02 22:06:06'),
	(6,3,6,'2020-08-02 22:06:06');

/*!40000 ALTER TABLE `games_to_players` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table moves
# ------------------------------------------------------------

DROP TABLE IF EXISTS `moves`;

CREATE TABLE `moves` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `game_id` int unsigned NOT NULL,
  `player_id` int unsigned NOT NULL,
  `type` enum('MOVE','QUIT') NOT NULL,
  `board_column` int NOT NULL,
  `board_row` int NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `game_id_constraint_1` (`game_id`),
  KEY `player_id_constraint_1` (`player_id`),
  CONSTRAINT `game_id_constraint_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`),
  CONSTRAINT `player_id_constraint_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `moves` WRITE;
/*!40000 ALTER TABLE `moves` DISABLE KEYS */;

INSERT INTO `moves` (`id`, `game_id`, `player_id`, `type`, `board_column`, `board_row`, `last_updated`)
VALUES
	(1,1,1,'MOVE',2,4,'2020-08-02 22:06:52'),
	(2,1,2,'MOVE',2,3,'2020-08-02 22:07:57'),
	(3,1,1,'MOVE',1,4,'2020-08-02 22:08:42'),
	(4,1,2,'MOVE',3,4,'2020-08-02 22:09:00'),
	(5,2,3,'MOVE',3,4,'2020-08-02 22:10:06'),
	(6,2,4,'MOVE',1,4,'2020-08-02 22:10:29'),
	(7,2,3,'MOVE',3,3,'2020-08-02 22:10:40'),
	(8,2,4,'MOVE',1,3,'2020-08-02 22:10:53'),
	(9,2,3,'MOVE',3,2,'2020-08-02 22:11:07'),
	(10,2,4,'MOVE',4,4,'2020-08-02 22:11:23'),
	(11,2,3,'MOVE',3,1,'2020-08-02 22:11:31'),
	(12,3,5,'MOVE',3,4,'2020-08-02 22:12:44'),
	(13,3,6,'MOVE',3,3,'2020-08-02 22:12:54'),
	(14,3,5,'QUIT',-1,-1,'2020-08-02 22:13:55');

/*!40000 ALTER TABLE `moves` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table players
# ------------------------------------------------------------

DROP TABLE IF EXISTS `players`;

CREATE TABLE `players` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;

INSERT INTO `players` (`id`, `name`, `last_updated`)
VALUES
	(1,'testPlayer1','2020-08-02 22:05:03'),
	(2,'testPlayer2','2020-08-02 22:05:03'),
	(3,'testPlayer3','2020-08-02 22:05:42'),
	(4,'testPlayer4','2020-08-02 22:05:42'),
	(5,'testPlayer5','2020-08-02 22:06:06'),
	(6,'testPlayer6','2020-08-02 22:06:06');

/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
