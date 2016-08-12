SELECT
user,
consumer_key,
consumer_secret,
access_token,
access_token_secret
FROM
twitter_users
WHERE
No = (%s)
