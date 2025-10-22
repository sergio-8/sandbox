import csv


def remove_duplicate_lines_case_insensitive(input_csv_path, output_csv_path):
    """
    Reads a CSV file, removes duplicate lines (case-insensitive and ignoring leading/trailing whitespace in cells),
    and writes the unique lines (in their original form) to a new CSV file.

    Args:
        input_csv_path (str): The path to the input CSV file.
        output_csv_path (str): The path to the output CSV file where unique lines will be saved.
    """
    seen_normalized_lines = set()

    try:
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile, \
                open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader, None)  # Read the header row
            if header:
                writer.writerow(header)  # Write original header to the output file
                # Normalize the header for the 'seen' set to prevent data rows identical
                # to a case-variant header from being dropped if data could match header.
                # However, for typical CSVs, the header is unique by nature.
                # For this script, we'll assume the first physical line is the header.
                # If your duplicates could *be* the header itself (e.g. header appearing mid-file),
                # and you want only the first instance, this logic would need adjustment.
                # For now, we add a normalized version of the header to seen_lines
                # ONLY IF you want to prevent a data row that is identical (case-insensitively)
                # to the header from appearing. Usually, this isn't desired.
                # Let's keep it simple: the header is written, and subsequent data is checked.

            for original_row in reader:
                # Normalize the row for comparison:
                # 1. Strip whitespace from each cell
                # 2. Convert each cell to lowercase
                normalized_row_list = [cell.strip().lower() for cell in original_row]

                # Convert the list of normalized cells to a tuple to make it hashable for the set
                normalized_row_tuple = tuple(normalized_row_list)

                if normalized_row_tuple not in seen_normalized_lines:
                    writer.writerow(original_row)  # Write the ORIGINAL row
                    seen_normalized_lines.add(normalized_row_tuple)

        print(f"Successfully processed. Unique lines saved to '{output_csv_path}' (case-insensitive)")

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- How to use the script ---
input_file = 'test_data.csv'
output_file = 'unique_data.csv'  # The output file will be overwritten if it exists

# Call the function to remove duplicates
remove_duplicate_lines_case_insensitive(input_file, output_file)