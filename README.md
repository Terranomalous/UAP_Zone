# Folder Structure

## /data_source

### uk_gov 
UFO reports by the UK Government from 1997 to 2009
sources : https://www.gov.uk/government/publications/ufo-reports-in-the-uk
Note : some files have been renamed to carry the year of the report in the form YYYY trailing the file name

## /data_transformed_intermediate

### uk_gov_pdf_all.csv
file will be generated when runnnig the parser script src/uk_gov/uk_gov_pdf2csv.py

## /data_transformed_xfinal


# /src
Folder containing all parser-, transformation- and scraping-scripts

## /uk_gov

### uk_gov_pdf2csv.py
script to parse the pdf files from the UK government and transform them into a csv file. The source files being parsed are located in the folder data_source/uk_gov ( see data_source >> uk_gov above )

Install dependencies
```bash
# install dependencies, preferably via pip
cd src/uk_gov
pip install -r requirements.txt
```

Run the script 
```bash
cd src/uk_gov
python uk_gov_pdf2csv.py
# generated file: data_transformed_intermediate/uk_gov_pdf_all.csv 
```

