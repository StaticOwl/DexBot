# DexBot

I have so far added some basic piece of code just to make sense out of it.

I'm actually trying out the sentdex tutorial here for creating a chatbot with reddit dataset. 

As far as of now I have only created the database code (WIP) and I'm working on creating a local database out of json data, and then start tokenize with it. 

The dataset link : [reddit_dataset](https://www.reddit.com/r/datasets/comments/3bxlg7/i_have_every_publicly_available_reddit_comment/?st=j9udbxta&sh=69e4fee7)

I have used the RC_2015-1 for my project, that's like 2015 january data. If you want to have something different, make sure you are changing the variable there.

You can download the data that is provided in the post using the magnet link. I'm currently working with the one month data due to limitation and high time consumption over the data download.

Later I am planning to create the bot with the bigquery table that they have [here](https://www.reddit.com/r/bigquery/comments/3cej2b/17_billion_reddit_comments_loaded_on_bigquery/?sort=new).

I have actually created a bq-view out of this. Here is the sample code for creating the view:

```
DECLARE sql_string STRING;
DECLARE final_sql_string STRING;
DECLARE total_rows INT64;
DECLARE max_table_name STRING;

-- Initialize the final SQL string
SET final_sql_string = '';

-- Query the INFORMATION_SCHEMA.TABLES view to get table names
SET total_rows = (
  SELECT COUNT(*)
  FROM `fh-bigquery.reddit_comments.INFORMATION_SCHEMA.TABLES`
  WHERE
    REGEXP_CONTAINS(table_name, r'^201._..$')
);

-- Loop through the tables and build the union statement
FOR table_info IN (
  SELECT table_name
  FROM `fh-bigquery.reddit_comments.INFORMATION_SCHEMA.TABLES`
  WHERE
    REGEXP_CONTAINS(table_name, r'^201._..$')
    order by table_name
) DO
  SET sql_string = CONCAT(
    'SELECT * FROM `fh-bigquery.reddit_comments.', table_info.table_name, '`'
  );

  -- Append the union statement to the final SQL string
  SET final_sql_string = CONCAT(final_sql_string, sql_string);

  -- Get the maximum table_name to check if it's the last table
  SET max_table_name = (SELECT MAX(table_name) FROM `fh-bigquery.reddit_comments.INFORMATION_SCHEMA.TABLES` WHERE REGEXP_CONTAINS(table_name, r'^201._..$'));

  -- Add UNION ALL between each statement if it's not the last table
  IF table_info.table_name != max_table_name THEN
    SET final_sql_string = CONCAT(final_sql_string, ' UNION ALL ');
  END IF;
END FOR;

-- Create the view with the generated SQL
EXECUTE IMMEDIATE 'CREATE OR REPLACE VIEW dlworks.dlworks.all_reddit_data AS ' || final_sql_string;
```


Note: This view only contains the data from 2010 to 2019 or as they have. Before that the tables are created with older bq formats only, so were not really able to convert them. Would appreciate if someone helps me with that as well.

BQ data pull and training is a WIP as of now. I will update more here as I make some progress.