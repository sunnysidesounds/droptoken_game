
/* GAMES TABLE */
CREATE TABLE `games` (
        `id` int unsigned NOT NULL AUTO_INCREMENT,
        `name` varchar(255) DEFAULT NULL,
        `columns` int unsigned NOT NULL DEFAULT '0',
        `rows` int unsigned NOT NULL DEFAULT '0',
        `board` json DEFAULT NULL,
        `state` enum('DONE','INPROGRESS') NOT NULL,
        `winner_id` int unsigned NOT NULL DEFAULT '0',
        `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* PLAYERS TABLE */
CREATE TABLE `players` (
       `id` int unsigned NOT NULL AUTO_INCREMENT,
       `name` varchar(255) DEFAULT NULL,
       `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/* GAMES TO PLAYER LOOKUP TABLE */
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


/* MOVES TABLE */
CREATE TABLE `moves` (
       `id` int unsigned NOT NULL AUTO_INCREMENT,
       `game_id` int unsigned NOT NULL,
       `player_id` int unsigned NOT NULL,
       `type` enum('MOVE','QUIT') NOT NULL,
       `board_colum` int unsigned NOT NULL,
       `board_row` int unsigned NOT NULL,
       `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
       PRIMARY KEY (`id`),
       KEY `game_id_constraint_1` (`game_id`),
       KEY `player_id_constraint_1` (`player_id`),
       CONSTRAINT `game_id_constraint_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`),
       CONSTRAINT `player_id_constraint_1` FOREIGN KEY (`player_id`) REFERENCES `players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;