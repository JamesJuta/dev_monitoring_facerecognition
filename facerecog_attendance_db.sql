-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 21, 2024 at 02:11 AM
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
-- Table structure for table `activity_log`
--

CREATE TABLE `activity_log` (
  `datetime` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `action` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`datetime`, `name`, `action`) VALUES
('2024-03-12 01:59:42', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - Detail: {id_no:26262, name: misd@ccc.edu.ph, time_added: 2024-03-12 01:59:42}'),
('2024-03-12 03:31:37', 'unknown', 'SUCCESS - FACE REGISTRATION -[A2023-00001] Details: {id_no:195730, name: unknown, time_added: 2024-03-12 03:31:37}'),
('2024-03-12 03:48:49', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-898, name: Aro Sanuel D. Alca, time_added: 2024-03-12 03:48:49}'),
('2024-03-13 01:56:22', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 195730, name: unknown, time_added: 2024-03-13 01:56:22}'),
('2024-03-13 02:02:08', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 4846, name: Sherwin Carias, time_added: 2024-03-13 02:02:08}'),
('2024-03-13 02:03:50', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-11739, name: Jezreel Di Rinehart, time_added: 2024-03-13 02:03:50}'),
('2024-03-13 02:21:37', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-11719, name: Anne Villasoto, time_added: 2024-03-13 02:21:37}'),
('2024-03-13 02:24:22', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-11456, name: Michael Ivan Landicho, time_added: 2024-03-13 02:24:22}'),
('2024-03-13 02:25:56', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 195730, name: unknown, time_added: 2024-03-13 02:25:56}'),
('2024-03-14 10:18:01', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-898, name: Aro Sanuel D. Alca, time_added: 2024-03-14 10:18:01}'),
('2024-03-14 10:46:39', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-11719, name: Anne Villasoto, time_added: 2024-03-14 10:46:39}'),
('2024-03-14 10:46:39', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 4846, name: Sherwin Carias, time_added: 2024-03-14 10:46:39}'),
('2024-03-14 10:46:39', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 26262, name: Nico, time_added: 2024-03-14 10:46:39}'),
('2024-03-15 09:30:22', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-11392, name: , time_added: 2024-03-15 09:30:22}'),
('2024-03-15 03:26:50', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-11392, time_added: 2024-03-15 03:26:50}'),
('2024-03-15 03:30:39', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 2020-2020, time_added: 2024-03-15 03:30:39}'),
('2024-03-15 03:43:47', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 4526-25213, time_added: 2024-03-15 03:43:47}'),
('2024-03-15 03:43:47', 'misd@ccc.edu.ph', 'SUCCESS - FACE REGISTRATION - [A2023-00001] Details: {id_no: 4526-25213, time_added: 2024-03-15 03:43:47}'),
('2024-03-19 03:08:19', 'Admin M. Account ', 'SUCCESS - FACE REGISTRATION - [User ID:1] Details: {id_no: 2020-11392, time_added: 2024-03-19 03:08:19}'),
('2024-03-19 04:25:43', 'Admin M. Account ', 'SUCCESS - FACE REGISTRATION - [User ID:1] Details: {id_no: 2020-11120, time_added: 2024-03-19 04:25:43}');

-- --------------------------------------------------------

--
-- Table structure for table `enrolled_students`
--

CREATE TABLE `enrolled_students` (
  `students_name` varchar(255) NOT NULL,
  `students_id_no` varchar(10) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `account_status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrolled_students`
--

INSERT INTO `enrolled_students` (`students_name`, `students_id_no`, `first_name`, `middle_name`, `surname`, `account_status`) VALUES
('unknown', '195730', '', '', '', 1),
('James Juta', '2020-11120', 'James', 'Fajardo', 'Juta', 1),
('Michael Ivan Landicho', '2020-11456', 'MIchael Ivan', '', 'Landicho', 1),
('Anne Villasoto', '2020-11719', 'Anne Ferdilyn', '', 'Villasoto', 1),
('Jezreel Di Rinehart', '2020-11739', 'Jezreel Di', '', 'Rinehart', 1),
('Aro Sanuel D. Alca', '2020-898', 'Aro Sanuel', '', 'Alca', 1),
('Nico', '26262', '', '', '', 1),
('Sherwin Carias', '4846', 'Sherwin', '', 'Carias', 1);

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
(20, '2020-11120'),
(21, '2020-11120'),
(22, '2020-11120'),
(23, '2020-11120'),
(24, '2020-11120'),
(25, '2020-11120'),
(26, '2020-11120'),
(27, '2020-11120'),
(28, '2020-11120'),
(29, '2020-11120'),
(30, '2020-11120'),
(31, '2020-11120'),
(32, '2020-11120'),
(33, '2020-11120'),
(34, '2020-11120'),
(35, '2020-11120'),
(36, '2020-11120'),
(37, '2020-11120'),
(38, '2020-11120'),
(39, '2020-11120'),
(40, '2020-11120'),
(41, '2020-11120'),
(42, '2020-11120'),
(43, '2020-11120'),
(44, '2020-11120'),
(45, '2020-11120'),
(46, '2020-11120'),
(47, '2020-11120'),
(48, '2020-11120'),
(49, '2020-11120'),
(50, '2020-11120'),
(51, '2020-11120'),
(52, '2020-11120'),
(53, '2020-11120'),
(54, '2020-11120'),
(55, '2020-11120'),
(56, '2020-11120'),
(57, '2020-11120'),
(58, '2020-11120'),
(59, '2020-11120'),
(60, '2020-11120'),
(61, '2020-11120'),
(62, '2020-11120'),
(63, '2020-11120'),
(64, '2020-11120'),
(65, '2020-11120'),
(66, '2020-11120'),
(67, '2020-11120'),
(68, '2020-11120'),
(69, '2020-11120'),
(70, '2020-11120'),
(71, '2020-11120'),
(72, '2020-11120'),
(73, '2020-11120'),
(74, '2020-11120'),
(75, '2020-11120'),
(76, '2020-11120'),
(77, '2020-11120'),
(78, '2020-11120'),
(79, '2020-11120'),
(80, '2020-11120'),
(81, '2020-11120'),
(82, '2020-11120'),
(83, '2020-11120'),
(84, '2020-11120'),
(85, '2020-11120'),
(86, '2020-11120'),
(87, '2020-11120'),
(88, '2020-11120'),
(89, '2020-11120'),
(90, '2020-11120'),
(91, '2020-11120'),
(92, '2020-11120'),
(93, '2020-11120'),
(94, '2020-11120'),
(95, '2020-11120'),
(96, '2020-11120'),
(97, '2020-11120'),
(98, '2020-11120'),
(99, '2020-11120'),
(100, '2020-11120'),
(101, '2020-11120'),
(102, '2020-11120'),
(103, '2020-11120'),
(104, '2020-11120'),
(105, '2020-11120'),
(106, '2020-11120'),
(107, '2020-11120'),
(108, '2020-11120'),
(109, '2020-11120'),
(110, '2020-11120'),
(111, '2020-11120'),
(112, '2020-11120'),
(113, '2020-11120'),
(114, '2020-11120'),
(115, '2020-11120'),
(116, '2020-11120'),
(117, '2020-11120'),
(118, '2020-11120'),
(119, '2020-11120'),
(120, '2020-11120'),
(121, '2020-11120'),
(122, '2020-11120'),
(123, '2020-11120'),
(124, '2020-11120'),
(125, '2020-11120'),
(126, '2020-11120'),
(127, '2020-11120'),
(128, '2020-11120'),
(129, '2020-11120'),
(130, '2020-11120'),
(131, '2020-11120'),
(132, '2020-11120'),
(133, '2020-11120'),
(134, '2020-11120'),
(135, '2020-11120'),
(136, '2020-11120'),
(137, '2020-11120'),
(138, '2020-11120'),
(139, '2020-11120'),
(140, '2020-11120'),
(141, '2020-11120'),
(142, '2020-11120'),
(143, '2020-11120'),
(144, '2020-11120'),
(145, '2020-11120'),
(146, '2020-11120'),
(147, '2020-11120'),
(148, '2020-11120'),
(149, '2020-11120'),
(150, '2020-11120'),
(151, '2020-11120'),
(152, '2020-11120'),
(153, '2020-11120'),
(154, '2020-11120'),
(155, '2020-11120'),
(156, '2020-11120'),
(157, '2020-11120'),
(158, '2020-11120'),
(159, '2020-11120'),
(160, '2020-11120'),
(161, '2020-11120'),
(162, '2020-11120'),
(163, '2020-11120'),
(164, '2020-11120'),
(165, '2020-11120'),
(166, '2020-11120'),
(167, '2020-11120'),
(168, '2020-11120'),
(169, '2020-11120'),
(170, '2020-11120'),
(171, '2020-11120'),
(172, '2020-11120'),
(173, '2020-11120'),
(174, '2020-11120'),
(175, '2020-11120'),
(176, '2020-11120'),
(177, '2020-11120'),
(178, '2020-11120'),
(179, '2020-11120'),
(180, '2020-11120'),
(181, '2020-11120'),
(182, '2020-11120'),
(183, '2020-11120'),
(184, '2020-11120'),
(185, '2020-11120'),
(186, '2020-11120'),
(187, '2020-11120'),
(188, '2020-11120'),
(189, '2020-11120'),
(190, '2020-11120'),
(191, '2020-11120'),
(192, '2020-11120'),
(193, '2020-11120'),
(194, '2020-11120'),
(195, '2020-11120'),
(196, '2020-11120'),
(197, '2020-11120'),
(198, '2020-11120'),
(199, '2020-11120'),
(200, '2020-11120');

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
('2020-11120', 'notice sample: sample notice to the user', '0', '2024-03-05 03:19:31'),
('2020-11121', 'sample notice for this day', '0', '2024-03-07 01:05:39');

-- --------------------------------------------------------

--
-- Table structure for table `student_users`
--

CREATE TABLE `student_users` (
  `id` int(11) NOT NULL,
  `student_id` varchar(255) NOT NULL,
  `department` varchar(255) NOT NULL COMMENT '1 - Department of Computing and Informatics\r\n2 - Department of Teacher and Education\r\n3 - Department of Business and Accountancy\r\n4 - Department of Arts and Sciences',
  `program` varchar(255) NOT NULL COMMENT '1 - Bachelor of Science in Psychology\r\n2 - Bachelor of Elementary Education\r\n3 - Bachelor of Secondary Education\r\n4 - Bachelor of Science in Accountancy\r\n5 - Bachelor of Science in Accounting Information System\r\n6 - Bachelor of Science in Information Technology\r\n7 - Bachelor of Science in Computer Science',
  `major` varchar(255) NOT NULL COMMENT '1 - Bachelor of Secondary Education Major in English\r\n2 - Bachelor of Secondary Education Major in Science\r\n3 - Bachelor of Secondary Education Major in Science\r\n',
  `year` varchar(255) NOT NULL COMMENT '1 - First Year\r\n2 - Second Year\r\n3 - Third Year\r\n4 - Fourth Year',
  `account_status` varchar(255) NOT NULL COMMENT '1 - Registered\r\n2 - Not Registered\r\n3 - Deleted\r\n4 - Suspended\r\n5 - Graduated\r\n6 - Face Registered',
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `suffix` varchar(10) NOT NULL,
  `sex` varchar(100) NOT NULL,
  `home_address` varchar(255) NOT NULL,
  `ccc_email` varchar(100) NOT NULL,
  `number` varchar(100) NOT NULL,
  `contact_name` varchar(255) NOT NULL,
  `contact_number` varchar(100) NOT NULL,
  `contact_address` varchar(255) NOT NULL,
  `date_modified` date DEFAULT NULL,
  `face_registration_date` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_users`
--

INSERT INTO `student_users` (`id`, `student_id`, `department`, `program`, `major`, `year`, `account_status`, `first_name`, `middle_name`, `last_name`, `suffix`, `sex`, `home_address`, `ccc_email`, `number`, `contact_name`, `contact_number`, `contact_address`, `date_modified`, `face_registration_date`) VALUES
(24, '2020-11392', 'Department of Computing and Informatics', '12', 'xxx-ccc-xxx', '4', '6', 'Lance Cyrill', 'Dela Peña', 'Gapas', '', 'Male', 'Blk 1 Lot 147, Southville 6', 'ldgapas@ccc.edu.ph', '0977-059-6497', 'Sarah D. Gapas', '0977-059-6497', 'Kay-Anlog', '2024-03-08', '2024-03-19 03:08:19'),
(26, '2020-2020', 'Department of Computing and Informatics', '12', 'xxx-ccc-xxx', '4', '1', 'name', 'name', 'name', 'Jr.', 'Male', 'address', 'ccc@email.com', '7418-529-6395', 'contact name', '7418-529-6375', 'ghjaksdasdkwaksdjk', '2024-03-08', '2024-03-15 03:30:39'),
(27, '4526-25213', 'Department of Teacher and Education', '2', 'English', '1', '1', 'Michael Ivan', 'jdlkajsldkajd', 'Landicho', '', 'Female', 'ahdgagsdhjg', 'email@email.com', '6543-124-5613', 'akjsdlkajskljdklad', '4565-454-6545', 'jshadkjahskdjhaskdj', '2024-03-08', '2024-03-15 03:43:47'),
(28, '9879-87987', 'Department of Computing and Informatics', '15', 'xxx-ccc-xxx', '3', '1', 'Jezreel Di', 'sdffsd', 'Rinehart', 'Jr.', 'Male', 'alkjdsakljd', 'email@email.com', '5465-465-4654', 'lklajdlkajsdkj', '9879-879-8465', 'lkajsdkljalskdjald', '2024-03-08', ''),
(29, '8798-79878', 'Department of Business and Accountancy', '13', 'xxx-ccc-xxx', '4', '1', 'Anne Ferdilyn', 'jlaksjdalkjsd', 'Villasoto', '', 'Male', 'adkajldJLkj', 'alskdja@e.com', '8798-798-7987', 'djakldjalkjKJ', '9987-465-5621', 'klAJLDKjakldjalkjd', '2024-03-08', ''),
(30, '6545-46545', 'Department of Teacher and Education', '2', 'Mathematics', '2', '1', 'Sherwin', 'jajsdklajsdj', 'Carias', 'Jr.', 'Female', 'jhasdjhaksjd', 'asdkjasdkjad@e.com', '9879-879-8798', 'jhadhskjahsdakdhd', '8795-643-2168', 'lkjadjkajhdkjahsjd', '2024-03-08', ''),
(31, '2020-11120', 'Department of Computing and Informatics', '15', 'xxx-ccc-xxx', '4', '6', 'James', 'Fajardo', 'Juta', '', 'Male', 'asdakjsdhj', 'jfjuta@ccc.edu.ph', '0000-000-0000', 'kajshdjashd', '5465-465-4654', 'akjshdjkashdjkasd', '2024-03-11', '2024-03-19 04:25:43'),
(32, '1231231', 'Department of Arts and Sciences', '18', 'xxx-ccc-xxx', '2', '1', 'Aro Sanuel', 'aaa', 'Alca', 'Jr.', 'Male', 'asdasdasd', 'sample@ccc.edu.ph', '0931-232-1231', 'asdasdas', '0934-524-3234', 'dasasddasadsadsasdsa', '2024-03-11', ''),
(33, '89798798', 'Department of Business and Accountancy', '16', 'xxx-ccc-xxx', '1', '1', 'Jasmine', 'jalksjda;lksjd', 'Morales', 'Sr.', 'Female', 'ajdkasdlahsd', 'akjsaksd@ccc.edu.ph', '9875-465-4656', 'aksjdakjsd', '1465-465-3216', 'akjhdkajsjkahd', '2024-03-11', '');

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
(10, 'James Juta', '2020-11120', 'jmc building', '11:23:31 AM', '02-05-2024', '2024-02-05 11:23:32');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_no` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `time_added` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
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
-- Indexes for table `enrolled_students`
--
ALTER TABLE `enrolled_students`
  ADD PRIMARY KEY (`students_id_no`);

--
-- Indexes for table `img_dataset`
--
ALTER TABLE `img_dataset`
  ADD PRIMARY KEY (`img_id`);

--
-- Indexes for table `student_users`
--
ALTER TABLE `student_users`
  ADD PRIMARY KEY (`id`);

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
-- AUTO_INCREMENT for table `student_users`
--
ALTER TABLE `student_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `time_log`
--
ALTER TABLE `time_log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=120;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
