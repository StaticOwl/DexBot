import sqlite3
import pandas as pd
import dask.dataframe as dd
from dask import delayed
from dask.distributed import Client

def update_parent():
    pass

def get_data_from_local_data(file_name = "dummy_data.txt"):
    # column_list = ['name', 'id', 'body', 'created_utc', 'parent_id', 'score', 'subreddit']
    # rename_column_list = ['comment_id', 'parent_id', 'comment', 'unix', 'parent', 'score', 'subreddit']
    df = dd.read_json(file_name, lines=True, blocksize='64MB')
    
    # Select the relevant columns
    df = df[['name', 'id', 'body', 'created_utc', 'parent_id', 'score', 'subreddit']]
    
    # Create a new DataFrame containing only 'id' and 'body' columns
    parent_text_df = df[['id', 'body']].rename(columns={'id': 'parent_id', 'body': 'parent_text'})
    
    # Merge the original DataFrame with the parent_text DataFrame
    merged_df = dd.merge(df, parent_text_df, on='parent_id', how='left')
    
    # Return the resulting DataFrame
    return merged_df
        
    
    # while cur_length == limit:
    #     df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} AND score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix, limit), connection)
    #     last_unix = df.tail(1)['unix'].values[0]
    #     cur_length = len(df)
        
    #     if not test_done:
    #         with open("runtime/test.from", 'a+', encoding='utf8') as f:
    #             for content in df['parent'].values:
    #                 f.write(str(content)+'\n')
                    
    #         with open("runtime/test.to", 'a+', encoding='utf8') as f:
    #             for content in df['comment'].values:
    #                 f.write(str(content)+'\n')
                    
    #         test_done = True
    #     else:
    #         with open("runtime/train.from", 'a+', encoding='utf8') as f:
    #             for content in df['parent'].values:
    #                 f.write(str(content)+'\n')
                    
    #         with open("runtime/train.to", 'a+', encoding='utf8') as f:
    #             for content in df['comment'].values:
    #                 f.write(str(content)+'\n')
                    
    #     counter += 1
    #     if counter % 20 == 0:
    #         print(counter*limit, 'rows completed so far')