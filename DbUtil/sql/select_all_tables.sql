select table_name from information_schema.tables where table_schema = database() and table_name not in ('twitter_users', 'tweet_contents')
