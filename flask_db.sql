CREATE TABLE `accs_hist` (
  `accs_id` int(11) NOT NULL AUTO_INCREMENT,
  `accs_date` date NOT NULL,
  `accs_prsn` varchar(3) NOT NULL,
  `accs_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`accs_id`),
  KEY `accs_date` (`accs_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;