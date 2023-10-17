from dask.distributed import Client
from database.dask.create_training_data import get_data_from_local_data
import os
import dask.array as da

if __name__ == '__main__':
    client = Client(
        n_workers=4, 
        threads_per_worker=4, 
        memory_limit='3GB',
        name='DexBot'
        )
    # Step 1: Create a Dask client
    try:
        os.system('clear')
        print("Dask Job Started")
        # Step 2: Read JSON file and create a Dask DataFrame
        # json_file = 'your_data.json'  # Replace with your JSON file path
        df = get_data_from_local_data("high_data_output.txt")
        # Step 3: Perform operations on the Dask DataFrame
        # For example, filtering rows where 'column_name' is greater than a certain value
        # filtered_df = df[df['column_name'] > 5]
        # Step 4: Compute and print the results
        # Using .compute() to convert Dask DataFrame to Pandas DataFrame
        # result_df = df.compute()
        # Print the entire DataFrame
        # print(result_df)
        # You can also print the first few rows using .head()
        print(df.head())
        # df.to_csv("high_data_output.csv")
        # x = da.ones((1000, 1000), chunks=(100, 100))
        # result = x.sum()
        # print(result.compute())

    except KeyboardInterrupt or Exception as e:
        print("Dask Job Stopped")
        print(e)
    finally:
        # Ask the user if they want to close the client
        while True:
            answer = input("Do you want to close the Dask client? (y/n): ")
            if answer.lower() == 'y':
                client.close()
                print("Client Closed Successfully")
                break
            elif answer.lower() == 'n':
                print("Client will remain open.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

