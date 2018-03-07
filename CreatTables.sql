DROP TABLE IF EXISTS `Houses`;

CREATE TABLE `Houses` (
  `Index` int(8) NOT NULL,
  `Zipcode` varchar(40) NULL,
  `Address` varchar(40) NULL,
  `City` varchar(40) NULL,
  `State` varchar(40)  NULL,
  `Neighborhood` varchar(40) NULL,
  `Price` int(11) NULL,
  `Type` int(11)  NULL,
  `Beds` int(11) NULL,
  `Baths` int(11) NULL,
  `Built` int(11)  NULL,
  `Space` int(11) NULL,
  `Lot_space` int(11) NULL,
  `Price/sqft` int(11)  NULL,
  `Average_Listing_Price_for_zip` int(11) NULL,
  `Median_Sale_Price_for_zip` int(11) NULL,
  `Average_price_sqft_for_zip` int(11)  NULL,
  `description` varchar(255)  NULL,
  PRIMARY KEY (`Index`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


LOAD DATA LOCAL INFILE 'C:/Users/yangz/Desktop/final/Infors.csv'
INTO TABLE discounts
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;