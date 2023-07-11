#/bin/bash

while getopts ":f:d:" option; do
  case $option in
    f)
      file_name="$OPTARG"
      ;;
    d)
      destination_table="$OPTARG"
      ;;
    *)
      echo "Usage: $0 [-f file_name] [-d destination_table]"
      exit 1
      ;;
  esac
done

PROJECT="artemis-1-391005"
DATASET="agri"

# Create the Table if it does not already exist in the BigQuery Dataset
echo "-----------------------------------------------------------"
echo "Creating Table " $destination_table " in " $DATASET
echo "-----------------------------------------------------------"

bq mk --table $DATASET.$destination_table


# Query USDA NASS Agri Dataset and Save Result to a Table
echo "-----------------------------------------------------------"
echo "In Project:" $PROJECT ", Querying BigQuery using $file_name"
echo "-----------------------------------------------------------"

bq query --use_legacy_sql=false < $file_name --project_id $PROJECT --destination_table $PROJECT:$DATASET.$destination_table


# Extract Table from BigQuery as CSV, then send it to Google Cloud Storage


# Download CSV to data dir from Google Cloud Storage