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
BUCKET="agri_csv_123"


# Query USDA NASS Agri Dataset and Save Result to a Table
echo "-----------------------------------------------------------"
echo "In Project:" $PROJECT ", Querying BigQuery using $file_name"
echo "-----------------------------------------------------------"

bq query --use_legacy_sql=false < $file_name --project_id $PROJECT --destination_table $PROJECT:$DATASET.$destination_table


# Extract Table from BigQuery as CSV, then send it to Google Cloud Storage
echo "-----------------------------------------------------------"
echo "Sending BigQuery Table called " $destination_table " to" $destination_table ".csv as CSV"
echo "-----------------------------------------------------------"

bq extract --destination_format CSV $PROJECT:$DATASET.$destination_table gs://$BUCKET/$destination_table.csv

# Download CSV to data dir from Google Cloud Storage
echo "-----------------------------------------------------------"
echo "Downloading " $destination_table ".csv to local"
echo "-----------------------------------------------------------"

gcloud storage cp gs://$BUCKET/$destination_table.csv /home/therealmolf/nass_agri_dash/data/agri/$destination_table.csv


