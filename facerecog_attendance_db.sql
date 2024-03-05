-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 05, 2024 at 09:32 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerecog_attendance_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accs_hist`
--

CREATE TABLE `accs_hist` (
  `accs_id` int(11) NOT NULL,
  `accs_date` date NOT NULL,
  `accs_prsn` varchar(3) NOT NULL,
  `accs_added` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `name` varchar(255) NOT NULL,
  `time_in` varchar(255) DEFAULT NULL,
  `time_out` varchar(255) DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`name`, `time_in`, `time_out`, `date`) VALUES
('Aro', '01:02 PM', NULL, '2024-01-16'),
('james', '01:32 PM', '01:33 PM', '2024-01-14');

-- --------------------------------------------------------

--
-- Table structure for table `enrolled_students`
--

CREATE TABLE `enrolled_students` (
  `students_name` varchar(255) NOT NULL,
  `students_id_no` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrolled_students`
--

INSERT INTO `enrolled_students` (`students_name`, `students_id_no`) VALUES
('unknown', '195730'),
('James Juta', '2020-11120'),
('Michael Ivan Landicho', '2020-11456'),
('Anne Villasoto', '2020-11719'),
('Jezreel Di Rinehart', '2020-11739'),
('Aro Sanuel D. Alca', '2020-898'),
('Nico', '26262'),
('Sherwin Carias', '4846');

-- --------------------------------------------------------

--
-- Table structure for table `img_dataset`
--

CREATE TABLE `img_dataset` (
  `img_id` int(11) NOT NULL,
  `img_person` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `img_dataset`
--

INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
(1, '2020-11120'),
(2, '2020-11120'),
(3, '2020-11120'),
(4, '2020-11120'),
(5, '2020-11120'),
(6, '2020-11120'),
(7, '2020-11120'),
(8, '2020-11120'),
(9, '2020-11120'),
(10, '2020-11120'),
(11, '2020-11120'),
(12, '2020-11120'),
(13, '2020-11120'),
(14, '2020-11120'),
(15, '2020-11120'),
(16, '2020-11120'),
(17, '2020-11120'),
(18, '2020-11120'),
(19, '2020-11120'),
(20, '2020-11120');

-- --------------------------------------------------------

--
-- Table structure for table `notice`
--

CREATE TABLE `notice` (
  `id` varchar(10) NOT NULL,
  `notice_message` varchar(255) NOT NULL,
  `notice_status` varchar(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notice`
--

INSERT INTO `notice` (`id`, `notice_message`, `notice_status`, `date`) VALUES
('2020-11120', 'notice sample: sample notice to the user', '0', '2024-03-05 03:19:31');

-- --------------------------------------------------------

--
-- Table structure for table `time_log`
--

CREATE TABLE `time_log` (
  `log_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `id_no` varchar(50) NOT NULL,
  `building_name` varchar(255) NOT NULL,
  `time` varchar(50) NOT NULL,
  `date` varchar(50) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `time_log`
--

INSERT INTO `time_log` (`log_id`, `name`, `id_no`, `building_name`, `time`, `date`, `datetime`) VALUES
(1, 'James Juta', '2020-11120', 'jmc building', '10:23:41 PM', '01-24-2024', '2024-01-25 10:23:57'),
(2, 'James Juta', '2020-11120', 'jmc building', '11:15:29 AM', '01-25-2024', '2024-01-25 11:15:29'),
(3, 'James Juta', '2020-11120', 'jmc building', '03:12:15 PM', '02-01-2024', '2024-02-01 15:12:17'),
(4, 'James Juta', '2020-11120', 'jmc building', '10:14:48 AM', '02-02-2024', '2024-02-02 10:14:50'),
(5, 'James Juta', '2020-11120', 'jmc building', '10:19:47 AM', '02-02-2024', '2024-02-02 10:19:48'),
(6, 'James Juta', '2020-11120', 'jmc building', '10:55:03 AM', '02-05-2024', '2024-02-05 10:55:09'),
(7, 'James Juta', '2020-11120', 'jmc building', '11:08:53 AM', '02-05-2024', '2024-02-05 11:08:54'),
(8, 'James Juta', '2020-11120', 'jmc building', '11:18:50 AM', '02-05-2024', '2024-02-05 11:18:51'),
(9, 'James Juta', '2020-11120', 'jmc building', '11:19:03 AM', '02-05-2024', '2024-02-05 11:19:04'),
(10, 'James Juta', '2020-11120', 'jmc building', '11:23:31 AM', '02-05-2024', '2024-02-05 11:23:32'),
(11, 'James Juta', '2020-11120', 'jmc building', '11:23:46 AM', '02-05-2024', '2024-02-05 11:23:47'),
(12, 'James Juta', '2020-11120', 'jmc building', '11:33:47 AM', '02-05-2024', '2024-02-05 11:33:48'),
(13, 'James Juta', '2020-11120', 'jmc building', '11:34:01 AM', '02-05-2024', '2024-02-05 11:34:02'),
(14, 'James Juta', '2020-11120', 'jmc building', '11:34:17 AM', '02-05-2024', '2024-02-05 11:34:18'),
(15, 'James Juta', '2020-11120', 'jmc building', '11:34:35 AM', '02-05-2024', '2024-02-05 11:34:36'),
(16, 'James Juta', '2020-11120', 'jmc building', '11:34:49 AM', '02-05-2024', '2024-02-05 11:34:50'),
(17, 'James Juta', '2020-11120', 'jmc building', '11:38:30 AM', '02-05-2024', '2024-02-05 11:38:31'),
(18, 'James Juta', '2020-11120', 'jmc building', '11:40:20 AM', '02-05-2024', '2024-02-05 11:40:21'),
(19, 'James Juta', '2020-11120', 'jmc building', '03:42:19 PM', '03-05-2024', '2024-03-05 15:42:20'),
(20, 'James Juta', '2020-11120', 'jmc building', '03:42:38 PM', '03-05-2024', '2024-03-05 15:42:39'),
(21, 'James Juta', '2020-11120', 'jmc building', '03:43:20 PM', '03-05-2024', '2024-03-05 15:43:21');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_no` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `time_added` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_no`, `name`, `time_added`) VALUES
('2020-11120', 'James Juta', '2024-01-24 22:21:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accs_hist`
--
ALTER TABLE `accs_hist`
  ADD PRIMARY KEY (`accs_id`),
  ADD KEY `accs_date` (`accs_date`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`name`,`date`);

--
-- Indexes for table `enrolled_students`
--
ALTER TABLE `enrolled_students`
  ADD UNIQUE KEY `students_id_no` (`students_id_no`);

--
-- Indexes for table `img_dataset`
--
ALTER TABLE `img_dataset`
  ADD PRIMARY KEY (`img_id`);

--
-- Indexes for table `notice`
--
ALTER TABLE `notice`
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `time_log`
--
ALTER TABLE `time_log`
  ADD PRIMARY KEY (`log_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accs_hist`
--
ALTER TABLE `accs_hist`
  MODIFY `accs_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=299;

--
-- AUTO_INCREMENT for table `time_log`
--
ALTER TABLE `time_log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
