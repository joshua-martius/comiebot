SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `serwmsound` DEFAULT CHARACTER SET utf16 COLLATE utf16_german2_ci;
USE `serwmsound`;

CREATE TABLE `tblComment` (
  `cID` int(11) NOT NULL,
  `cUploadID` varchar(16) COLLATE utf16_german2_ci NOT NULL,
  `cAuthor` varchar(16) COLLATE utf16_german2_ci NOT NULL,
  `cComment` text COLLATE utf16_german2_ci NOT NULL,
  `cCreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cCreatedFrom` varchar(32) COLLATE utf16_german2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;

CREATE TABLE `tblUpload` (
  `uID` varchar(32) COLLATE utf16_german2_ci NOT NULL,
  `uUploaded` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `uUploaderIP` varchar(32) COLLATE utf16_german2_ci NOT NULL,
  `uInterpret` varchar(32) COLLATE utf16_german2_ci DEFAULT NULL,
  `uName` varchar(64) COLLATE utf16_german2_ci DEFAULT NULL,
  `uLyrics` text COLLATE utf16_german2_ci,
  `uAllowComments` tinyint(1) NOT NULL DEFAULT '1',
  `uHits` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;


ALTER TABLE `tblComment`
  ADD PRIMARY KEY (`cID`),
  ADD KEY `FK_uUpload` (`cUploadID`);

ALTER TABLE `tblUpload`
  ADD PRIMARY KEY (`uID`);


ALTER TABLE `tblComment`
  MODIFY `cID` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `tblComment`
  ADD CONSTRAINT `FK_uUpload` FOREIGN KEY (`cUploadID`) REFERENCES `tblUpload` (`uID`);
COMMIT;
