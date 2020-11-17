CREATE TABLE `poi_ratings` (  
  id int NOT NULL primary key AUTO_INCREMENT comment 'primary key',
  created_time DATETIME COMMENT 'created time',
  `poi_id` varchar(255) comment '',
  `poi_name` varchar(255) comment '',
  `user_id` varchar(255) comment '',
  `rating` varchar(255) COMMENT '',
  `comment_time` VARCHAR (255) COMMENT ''
) default charset utf8 comment '';