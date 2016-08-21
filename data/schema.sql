DROP DATABASE IF EXISTS sample_auth;
CREATE DATABASE dev_cup2016;

USE sample_auth;

CREATE TABLE `users` (
    `id` BIGINT(20) AUTO_INCREMENT,
    `email` varchar(128) NOT NULL,
    `password` varchar(128) NOT NULL,
    `first_name` varchar(64) DEFAULT NULL,
    `last_name` varchar(64) DEFAULT NULL,
    `gender` varchar(16) DEFAULT NULL,
    `age` int(3) COLLATE utf8_unicode_ci NOT NULL,
    `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `mixed_email_pass` (`email`, `password`),
    KEY `mixed_name_fname` (`first_name`, `last_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `questions` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `quiz_id` bigint(20) NOT NULL,
  `question_phrase` TEXT NOT NULL,
  `is_multiple_choice` tinyint(1) DEFAULT 1,
  `choices` TEXT NOT NULL,
  `correct_choice` INT(2),
  `answer` varchar(64) DEFAULT NULL,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` datetime ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `quiz` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `article_url` varchar(400) NOT NULL,
  `article_title` varchar(400) NOT NULL,
  `article_summary` TEXT,
  `date_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` datetime ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;