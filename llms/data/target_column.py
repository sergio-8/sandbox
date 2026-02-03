import csv


def remove_duplicates_by_first_column(input_csv_path, output_csv_path):
    """
    Reads a CSV file, removes rows where the first column is a duplicate
    (case-insensitive and ignoring leading/trailing whitespace in the first cell),
    and writes the unique rows (keeping the first occurrence) to a new CSV file.

    Args:
        input_csv_path (str): The path to the input CSV file.
        output_csv_path (str): The path to the output CSV file where unique rows will be saved.
    """
    seen_first_column_values = set()

    try:
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile, \
                open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader, None)  # Read the header row
            if header:
                writer.writerow(header)  # Write header to the output file
                # We don't add the header's first column to seen_first_column_values
                # as it's not typically data to be de-duplicated against.

            for original_row in reader:
                if not original_row:  # Skip empty rows if any
                    continue

                # Get the first cell's value
                first_cell_original = original_row[0]

                # Normalize the first cell's value for comparison:
                # 1. Strip whitespace
                # 2. Convert to lowercase
                normalized_first_cell = first_cell_original.strip().lower()

                if normalized_first_cell not in seen_first_column_values:
                    writer.writerow(original_row)  # Write the ORIGINAL entire row
                    seen_first_column_values.add(normalized_first_cell)
                # Else (it's a duplicate based on the first column), do nothing (skip the row)

        print(f"Successfully processed. Rows unique by Column A saved to '{output_csv_path}'")
        print(f"Kept first occurrences, duplicates based on Column A were removed.")

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
    except IndexError:
        print("Error: A row was encountered that does not have a first column (e.g., an empty line parsed as a row).")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- How to use the script ---
input_file = 'test_data.csv'
# You might want to use a new output file name to see the effect of this specific logic
output_file = 'unique_by_column_A.csv'

# Call the function to remove duplicates
remove_duplicates_by_first_column(input_file, output_file)