SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `comiebot` DEFAULT CHARACTER SET utf16 COLLATE utf16_german2_ci;
USE `comiebot`;

CREATE TABLE `tblAnime` (
  `aID` int(11) NOT NULL,
  `aTitle` varchar(128) COLLATE utf16_german2_ci NOT NULL,
  `aLink` varchar(512) COLLATE utf16_german2_ci NOT NULL,
  `aCreator` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `aCreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `aTags` varchar(128) COLLATE utf16_german2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;

CREATE TABLE `tblUser` (
  `uName` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `uID` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `uChips` bigint(64) NOT NULL DEFAULT '1000',
  `uCreated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;

CREATE TABLE `tblVoting` (
  `vID` int(11) NOT NULL,
  `vMessage` varchar(256) COLLATE utf16_german2_ci NOT NULL,
  `vVotes` int(11) NOT NULL DEFAULT '0',
  `vAuthor` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `vCreated` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;
CREATE TABLE `viewImages` (
`uName` varchar(64)
,`uID` varchar(64)
,`Images` bigint(21)
);
DROP TABLE IF EXISTS `viewImages`;

CREATE ALGORITHM=UNDEFINED DEFINER=`comie`@`%` SQL SECURITY DEFINER VIEW `viewImages`  AS  select `tblUser`.`uName` AS `uName`,`tblUser`.`uID` AS `uID`,(select count(0) from `tblVoting` where (`tblVoting`.`vAuthor` = `tblUser`.`uID`)) AS `Images` from `tblUser` order by `Images` desc ;


ALTER TABLE `tblAnime`
  ADD PRIMARY KEY (`aID`),
  ADD KEY `FK_UID_UID` (`aCreator`);

ALTER TABLE `tblUser`
  ADD PRIMARY KEY (`uName`),
  ADD UNIQUE KEY `FK_UNIQUE` (`uID`);

ALTER TABLE `tblVoting`
  ADD PRIMARY KEY (`vID`),
  ADD UNIQUE KEY `vMessageID` (`vMessage`);


ALTER TABLE `tblAnime`
  MODIFY `aID` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `tblVoting`
  MODIFY `vID` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `tblAnime`
  ADD CONSTRAINT `FK_UID_UID` FOREIGN KEY (`aCreator`) REFERENCES `tblUser` (`uID`);
COMMIT;

