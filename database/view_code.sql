SELECT 
    parent_id, 
    id AS comment_id, 
    (SELECT comment FROM table WHERE comment_id = parent_id.split('_')[1]) limit 1 AS parent,
    REPLACE(REPLACE(body, '\n', ' newchar ')) AS comment, --handle quote issues in dataframe
    subreddit, 
    created_utc AS unix, 
    score 
FROM table
