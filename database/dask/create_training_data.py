import sqlite3
import pandas as pd
import dask.dataframe as dd

def update_parent():

    pass

def get_data_from_local_data(file_name = "dummy_data.txt"):
    limit = 5000
    last_unix = 0
    cur_length = limit
    counter = 0
    test_done = False
    # column_list = ['name', 'id', 'body', 'created_utc', 'parent_id', 'score', 'subreddit']
    # rename_column_list = ['comment_id', 'parent_id', 'comment', 'unix', 'parent', 'score', 'subreddit']

    df = dd.read_json(file_name, lines=True, blocksize=1000000)
    # print(df.head())
    with pd.option_context('display.max_rows', 100, 'display.max_columns', None):
    #     # print(df.loc[df['id'] == '2qyr1a'])
        print(df.head())
        
    
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



get_data_from_local_data("high_data_output.txt")