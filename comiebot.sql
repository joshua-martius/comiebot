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

CREATE TABLE `tblConfig` (
  `cID` int(11) NOT NULL,
  `cKey` varchar(32) COLLATE utf16_german2_ci NOT NULL,
  `cValue` varchar(64) COLLATE utf16_german2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;

CREATE TABLE `tblGame` (
  `gID` int(11) NOT NULL,
  `gChannelID` varchar(32) COLLATE utf16_german2_ci NOT NULL,
  `gTeamsize` tinyint(4) NOT NULL,
  `gName` varchar(16) COLLATE utf16_german2_ci NOT NULL,
  `gRoleName` varchar(16) COLLATE utf16_german2_ci NOT NULL,
  `gEmoji` varchar(32) COLLATE utf16_german2_ci NOT NULL
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
CREATE TABLE `viewConfig` (
`Entry` varchar(32)
);
CREATE TABLE `viewImagePercentage` (
`Name` varchar(64)
,`Percentage` decimal(27,3)
);
CREATE TABLE `viewImagePercentageClean` (
`Name` varchar(64)
,`Percentage` decimal(27,3)
);
CREATE TABLE `viewImages` (
`uName` varchar(64)
,`uID` varchar(64)
,`Images` bigint(21)
);
CREATE TABLE `viewImagesLite` (
`Name` varchar(64)
,`Images` bigint(21)
);
DROP TABLE IF EXISTS `viewConfig`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `viewConfig`  AS  select `tblConfig`.`cKey` AS `Entry` from `tblConfig` ;
DROP TABLE IF EXISTS `viewImagePercentage`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `viewImagePercentage`  AS  select `viewImagesLite`.`Name` AS `Name`,round(((`viewImagesLite`.`Images` / (select sum(`viewImagesLite`.`Images`) from `viewImagesLite`)) * 100),3) AS `Percentage` from `viewImagesLite` ;
DROP TABLE IF EXISTS `viewImagePercentageClean`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `viewImagePercentageClean`  AS  select `viewImagePercentage`.`Name` AS `Name`,`viewImagePercentage`.`Percentage` AS `Percentage` from `viewImagePercentage` where (`viewImagePercentage`.`Percentage` > 0.0) ;
DROP TABLE IF EXISTS `viewImages`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `viewImages`  AS  select `tblUser`.`uName` AS `uName`,`tblUser`.`uID` AS `uID`,(select count(0) from `tblVoting` where (`tblVoting`.`vAuthor` = `tblUser`.`uID`)) AS `Images` from `tblUser` order by `Images` desc ;
DROP TABLE IF EXISTS `viewImagesLite`;

CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `viewImagesLite`  AS  select substring_index(`viewImages`.`uName`,'#',1) AS `Name`,`viewImages`.`Images` AS `Images` from `viewImages` ;


ALTER TABLE `tblAnime`
  ADD PRIMARY KEY (`aID`),
  ADD KEY `FK_UID_UID` (`aCreator`);

ALTER TABLE `tblConfig`
  ADD PRIMARY KEY (`cID`);

ALTER TABLE `tblGame`
  ADD PRIMARY KEY (`gID`),
  ADD UNIQUE KEY `gChannelID` (`gChannelID`);

ALTER TABLE `tblUser`
  ADD PRIMARY KEY (`uName`),
  ADD UNIQUE KEY `FK_UNIQUE` (`uID`);

ALTER TABLE `tblVoting`
  ADD PRIMARY KEY (`vID`),
  ADD UNIQUE KEY `vMessageID` (`vMessage`);


ALTER TABLE `tblAnime`
  MODIFY `aID` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `tblConfig`
  MODIFY `cID` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `tblGame`
  MODIFY `gID` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `tblVoting`
  MODIFY `vID` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `tblAnime`
  ADD CONSTRAINT `FK_UID_UID` FOREIGN KEY (`aCreator`) REFERENCES `tblUser` (`uID`);
COMMIT;
