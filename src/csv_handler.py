import pandas as pd

def import_csv(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)

    # Validate contents
    missing_data = data.isnull().sum()
    if missing_data.any():
        print("Missing data detected:", missing_data[missing_data > 0])

    # Remove duplicates based on 'Word/Phrase' and 'Category'
    data.drop_duplicates(subset=['Word/Phrase', 'Category'], inplace=True)

    # Display summary
    print(f"Imported {len(data)} entries.")
    print(data['Category'].value_counts())

    # Save clean data to database or further process
    # Example: data.to_sql('vocabulary', connection, if_exists='append', index=False)

    return data

# Example usage
import_csv('your_csv_file.csv')
