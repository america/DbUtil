CREATE
TABLE
twitter_users
(
  No INTEGER PRIMARY KEY AUTO_INCREMENT,
  user VARCHAR(50) NOT NULL,
  consumer_key VARCHAR(100) NOT NULL,
  consumer_secret VARCHAR(100) NOT NULL,
  access_token VARCHAR(100) NOT NULL,
  access_token_secret VARCHAR(100) NOT NULL
)
