from multiprocessing import process
import pandas as pd
import argparse

# Main function to load and process the CSV file
def main():
    # Set up argument parser to accept file input with a default value
    parser = argparse.ArgumentParser(description='Process a CSV file.')
    parser.add_argument('file', type=str, nargs='?', default='fines.csv', help='Path to the CSV file (default: fines.csv)')
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
            date  = row.iloc[1]
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
    print(fines_df)
    


if __name__ == "__main__":
    main()
