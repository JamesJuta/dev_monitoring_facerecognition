-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 14, 2024 at 06:55 AM
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
-- Database: `dev_monitoring`
--

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
  `account_status` varchar(255) NOT NULL COMMENT '1 - Registered\r\n2 - Not Registered\r\n3 - Deleted\r\n4 - Suspended\r\n5 - Graduated',
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
  `date_modified` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_users`
--

INSERT INTO `student_users` (`id`, `student_id`, `department`, `program`, `major`, `year`, `account_status`, `first_name`, `middle_name`, `last_name`, `suffix`, `sex`, `home_address`, `ccc_email`, `number`, `contact_name`, `contact_number`, `contact_address`, `date_modified`) VALUES
(24, '2020-11392', 'Department of Computing and Informatics', '12', 'xxx-ccc-xxx', '4', '1', 'Lance Cyrill', 'Dela Peña', 'Gapas', '', 'Male', 'Blk 1 Lot 147, Southville 6', 'ldgapas@ccc.edu.ph', '0977-059-6497', 'Sarah D. Gapas', '0977-059-6497', 'Kay-Anlog', '2024-03-08'),
(26, '2020-2020', 'Department of Computing and Informatics', '12', 'xxx-ccc-xxx', '4', '1', 'name', 'name', 'name', 'Jr.', 'Male', 'address', 'ccc@email.com', '7418-529-6395', 'contact name', '7418-529-6375', 'ghjaksdasdkwaksdjk', '2024-03-08'),
(27, '4526-25213', 'Department of Teacher and Education', '2', 'English', '1', '1', 'alksdakljsd', 'jdlkajsldkajd', 'lkajsdlkasd', '', 'Female', 'ahdgagsdhjg', 'email@email.com', '6543-124-5613', 'akjsdlkajskljdklad', '4565-454-6545', 'jshadkjahskdjhaskdj', '2024-03-08'),
(28, '9879-87987', 'Department of Computing and Informatics', '15', 'xxx-ccc-xxx', '3', '1', 'akjdslakjsdk', 'jlaksjdlasjd', 'klajlskdjalskdj', 'Jr.', 'Male', 'alkjdsakljd', 'email@email.com', '5465-465-4654', 'lklajdlkajsdkj', '9879-879-8465', 'lkajsdkljalskdjald', '2024-03-08'),
(29, '8798-79878', 'Department of Business and Accountancy', '13', 'xxx-ccc-xxx', '4', '2', 'dakdskajsd', 'jlaksjdalkjsd', 'lkajskldjaskldj', '', 'Male', 'adkajldJLkj', 'alskdja@e.com', '8798-798-7987', 'djakldjalkjKJ', '9987-465-5621', 'klAJLDKjakldjalkjd', '2024-03-08'),
(30, '6545-46545', 'Department of Teacher and Education', '2', 'Mathematics', '2', '1', 'adsasldl', 'jajsdklajsdj', 'jalksdjlkajsd', 'Jr.', 'Female', 'jhasdjhaksjd', 'asdkjasdkjad@e.com', '9879-879-8798', 'jhadhskjahsdakdhd', '8795-643-2168', 'lkjadjkajhdkjahsjd', '2024-03-08'),
(31, '2020-11120', 'Department of Computing and Informatics', '15', 'xxx-ccc-xxx', '4', '1', 'James', 'Fajardo', 'Juta', '', 'Male', 'asdakjsdhj', 'jfjuta@ccc.edu.ph', '0000-000-0000', 'kajshdjashd', '5465-465-4654', 'akjshdjkashdjkasd', '2024-03-11'),
(32, '1231231', 'Department of Arts and Sciences', '18', 'xxx-ccc-xxx', '2', '1', 'ssdsdsd', 'aaa', 'dasd', 'Jr.', 'Male', 'asdasdasd', 'sample@ccc.edu.ph', '0931-232-1231', 'asdasdas', '0934-524-3234', 'dasasddasadsadsasdsa', '2024-03-11'),
(33, '89798798', 'Department of Business and Accountancy', '16', 'xxx-ccc-xxx', '1', '3', 'asdklajsd', 'jalksjda;lksjd', 'oasijdaosd', 'Sr.', 'Female', 'ajdkasdlahsd', 'akjsaksd@ccc.edu.ph', '9875-465-4656', 'aksjdakjsd', '1465-465-3216', 'akjhdkajsjkahd', '2024-03-11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `student_users`
--
ALTER TABLE `student_users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `student_users`
--
ALTER TABLE `student_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
