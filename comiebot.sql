-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 06, 2020 at 06:18 PM
-- Server version: 5.7.31-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `comiebot`
--
CREATE DATABASE IF NOT EXISTS `comiebot` DEFAULT CHARACTER SET utf16 COLLATE utf16_german2_ci;
USE `comiebot`;

-- --------------------------------------------------------

--
-- Table structure for table `tblUser`
--

CREATE TABLE `tblUser` (
  `uName` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `uID` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `uChips` bigint(64) NOT NULL DEFAULT '1000',
  `uCreated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tblVoting`
--

CREATE TABLE `tblVoting` (
  `vID` int(11) NOT NULL,
  `vMessage` varchar(256) COLLATE utf16_german2_ci NOT NULL,
  `vVotes` int(11) NOT NULL DEFAULT '0',
  `vAuthor` varchar(64) COLLATE utf16_german2_ci NOT NULL,
  `vCreated` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_german2_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tblUser`
--
ALTER TABLE `tblUser`
  ADD PRIMARY KEY (`uName`);

--
-- Indexes for table `tblVoting`
--
ALTER TABLE `tblVoting`
  ADD PRIMARY KEY (`vID`),
  ADD UNIQUE KEY `vMessageID` (`vMessage`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tblVoting`
--
ALTER TABLE `tblVoting`
  MODIFY `vID` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
