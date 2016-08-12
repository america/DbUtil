INSERT INTO tweet_contents (
  sid,
  uid,
  lang,
  screen_name,
  name,
  tweet,
  reply,
  created_time)
VALUES (
  %s,
  %s,
  %s,
  %s,
  %s,
  %s,
  %s,
  %s
)
