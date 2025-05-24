import csv


def debug_remove_duplicate_lines(input_csv_path, output_csv_path):
    """
    Reads a CSV file, attempts to remove duplicate lines (case-insensitive, ignoring whitespace),
    and writes unique lines to a new CSV. Includes extensive print statements for debugging.

    Args:
        input_csv_path (str): The path to the input CSV file.
        output_csv_path (str): The path to the output CSV file.
    """
    seen_normalized_lines = set()
    line_number = 0
    duplicates_found_count = 0
    unique_lines_written_count = 0

    print(f"--- Starting processing for {input_csv_path} ---")

    try:
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile, \
                open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader, None)  # Read the header row
            line_number += 1
            if header:
                print(f"\nLine {line_number} (Header): {header}")
                writer.writerow(header)
                unique_lines_written_count += 1
                # For debugging, let's see the normalized header too, though we don't add it to seen_normalized_lines
                # unless we want to prevent data rows identical to the header.
                # normalized_header_list = [cell.strip().lower() for cell in header]
                # normalized_header_tuple = tuple(normalized_header_list)
                # print(f"Normalized Header Tuple: {normalized_header_tuple}")
                # seen_normalized_lines.add(normalized_header_tuple) # Optional: only if header itself could be a duplicate data pattern
            else:
                print("No header found or file is empty.")

            print("\n--- Processing data rows ---")
            for original_row in reader:
                line_number += 1
                print(f"\nLine {line_number}: Original Row: {original_row}")

                normalized_row_list = [cell.strip().lower() for cell in original_row]
                normalized_row_tuple = tuple(normalized_row_list)

                print(f"Line {line_number}: Normalized Tuple: {normalized_row_tuple}")

                if normalized_row_tuple not in seen_normalized_lines:
                    print(f"Line {line_number}: Normalized tuple is NEW. Writing original row to output.")
                    writer.writerow(original_row)
                    seen_normalized_lines.add(normalized_row_tuple)
                    unique_lines_written_count += 1
                    # print(f"Current seen_normalized_lines: {seen_normalized_lines}") # Can be very verbose
                else:
                    print(f"Line {line_number}: Normalized tuple is a DUPLICATE. Skipping.")
                    duplicates_found_count += 1

        print(f"\n--- Processing Complete ---")
        print(f"Total lines read (including header): {line_number}")
        print(f"Unique lines written (including header, if present): {unique_lines_written_count}")
        print(f"Duplicate lines skipped: {duplicates_found_count}")
        if duplicates_found_count == 0 and line_number > (1 if header else 0):
            print("WARNING: No duplicates were identified based on the current logic.")
        print(f"Unique lines saved to '{output_csv_path}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- How to use the script ---
input_file = 'test_data.csv'
output_file = 'unique_data_debug.csv'  # Using a new output name to avoid overwriting previous results

# Call the function
debug_remove_duplicate_lines(input_file, output_file)