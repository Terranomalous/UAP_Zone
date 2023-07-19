import pdfplumber
import pandas as pd
from dateutil import parser
from dateutil.parser import ParserError
from datetime import datetime
import re
import os
import glob


#file_input = "ufo_report_2009.pdf" # NOTE parsing all PDF files in folder now
folder_input = "../../data_source/uk_gov/"
file_output = "../../data_transformed_intermediate/uk_gov_pdf_all.csv"
#standard_cols = ['Date', 'Time', 'Town', 'Area', 'Occupation', 'Description']
#standard_cols_obj = {0:'Date', 1:'Time', 2:'Town', 3:'Area', 4:'Occupation', 5:'Description'}


def remove_line_returns(text):
  if text is None:
    return text
  return text.replace('\n', ' ')


def format_date(date_str):
  return to_datetime(date_str, format='%d-%b-%y')


# handles also rare period entry formats like "29 Jun-2 Jul 09" . In that case we take the first datefrom datetime import datetime
def parse_date(date_string):
    # If the date_string is "No Firm Date" or "N/A", return the string itself
    if date_string in ["No Firm Date", "N/A"]:
        return date_string

    # Define the formats that the date could be in
    formats = ['%d-%b-%y', '%b-%y', '%m-%y', '%d-%m-%y']

    for fmt in formats:
        try:
            # Try to parse the date string
            date = datetime.strptime(date_string, fmt)

            # Check if the date includes a day
            if fmt in ['%d-%b-%y', '%d-%m-%y']:
                return date.strftime('%Y-%m-%d')
            else:
                return date.strftime('%Y-%m')
        except ValueError:
            continue

    # If all attempts to parse the date string fail, return None
    return None




# Get all pdf files in current directory
pdf_files = glob.glob(os.path.join(folder_input, "*.pdf"))
# sort pdf_files by last 4 chars in file name, NOTE make sure all files end with 4 digit year ( as they currently are in the source folder )
pdf_files.sort(key=lambda x: x[-8:])
print(f"Found {len(pdf_files)} PDF files")

# Initialize an empty DataFrame
all_tables = pd.DataFrame()


for pdf_file in pdf_files:
    print(f"Opening PDF with tables: `{pdf_file}`")
    # Load your PDF
    with pdfplumber.open(pdf_file) as pdf:

        df_index = 0
        # Loop through the pages
        for page in pdf.pages:
            # Extract tables from the page
            tables = page.extract_tables()

            # Loop through the tables
            for table in tables:
                # Convert the table to a DataFrame
                df = pd.DataFrame(table[1:], columns=table[0]) # CAREFUL : this was working, but we try to include the column heads in the first data frame

                if df_index == 0:
                    columns_list = df.columns.tolist()

                index_list  = df.columns.tolist()

                 # Reset the column names of df
                df.columns = range(df.shape[1])

                ### CELL TRANSFORMATIONS
                # Remove line returns in each cell
                df = df.applymap(remove_line_returns)

                # Date column transformations
                df[0] = df[0].apply(parse_date)
                ### / CELL TRANSFORMATIONS

                # Append the DataFrame to all_tables
                all_tables = pd.concat([all_tables, df]).reset_index(drop=True)

                # Debug output for each DataFrame
                print(f"Processed Table fragment {df_index+1}")

                df_index += 1


        # Append to master dataframe
        all_tables = pd.concat([all_tables, df])

# Save all_tables to CSV
all_tables.rename(columns=dict(enumerate(columns_list)), inplace=True)
all_tables.to_csv(file_output, index=False)

print(f"Written all fragments to `{file_output}`")




