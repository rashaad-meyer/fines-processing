import pandas as pd
import argparse

# Main function to load and process the CSV file
def main():
    # Set up argument parser to accept file input as a positional argument
    parser = argparse.ArgumentParser(description='Process a CSV file.')
    parser.add_argument('file', type=str, help='Path to the CSV file')
    args = parser.parse_args()

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(args.file, header=None)
    print(df.head())
    process_fines = False
    date = None
    fines = {}

    # Loop through each row
    for index, row in df.iterrows():
        if row.iloc[0] == 'Player name':
            print('Player name found')
            process_fines = True
        elif pd.isna(row.iloc[0]):
            process_fines = False
        elif row.iloc[0] == 'Date':
            print('Date found')
            date = row.iloc[1]
        elif process_fines:
            name = row.iloc[0].strip()
            fine_count = int(row.iloc[1])
            description = row.iloc[2]
            if name in fines:
                fines[name]['fine_count'] += fine_count
                fines[name]['description'] += f',{description}[{date}]'
            else:
                fines[name] = {
                    'fine_count': fine_count,
                    'description': f'{description}[{date}]'
                }
    
    fines_list = [{'name': key, 'fine_count': value['fine_count'], 'description': value['description']} for key, value in fines.items()]
    fines_df = pd.DataFrame(fines_list)

    # Sort the DataFrame by the 'name' column
    fines_df = fines_df.sort_values(by='name')

    fines_df.to_csv('processed_fines.csv', index=False)
    print(fines_df)


if __name__ == "__main__":
    main()
