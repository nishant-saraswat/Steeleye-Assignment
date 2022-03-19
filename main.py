"""
@author: Nishant Saraswat

Main module for extracting all the required info
"""

import os
from logger import log
from xml_parser import parse_xml, convert_to_csv
from utils import download_file, upload_to_s3, unzip_file, read_config


def main():
    """
    Main function for the program
    """
    try:
        # Read config
        config = read_config()
        # Extracting xml file url
        url = config.get("xmlfile", "xml_url")

        # Extracting csv file path
        csv_path = os.path.join(os.getcwd(), config.get("csv", "csv_path"))

        # Extracting xml file download path
        download_path = os.path.join(
            os.getcwd(), config.get("download", "download_path")
        )

        # Extracting s3 resource information from config
        bucket_name = config.get("aws", "bucket_name")
        aws_access_key_id = config.get("aws", "aws_access_key_id")
        aws_secret_access_key = config.get("aws", "aws_secret_access_key")
        region_name = config.get("aws", "region_name")

        # Calling download function to download the file from url
        xml_file = download_file(url, download_path, "source_xml_file.xml")

        # Parse xml file to extract the required file path from xml file
        attributes = parse_xml(xml_file, ('file_type', 'DLTINS'),
                               ['file_name', 'download_link'])
        if attributes:
            file_name, file_path = attributes
        else:
            log.info('Parsing failed')
            return

        # Calling download function to download the data
        zip_file = download_file(file_path, download_path, file_name)

        if zip_file:
            if not unzip_file(zip_file, download_path):
                log.info('Error in trying to unzip file: {zip_file}')
                return
        else:
            log.info('Error in downloading the zip file')
            return
        xml_file_path = os.path.join(
            download_path, file_name.split(".")[0] + ".xml")
        # Calling convert_to_csv function to conver the xml file to csv
        csv_file = convert_to_csv(xml_file_path, csv_path)
        if not csv_file:
            log.info('Error in parsing and converting to csv')

        upload_status = upload_to_s3(
            region_name, aws_access_key_id,
            aws_secret_access_key,
            bucket_name, csv_file)
        if upload_status:
            log.info('Process Completed Successfully')
        else:
            log.info('Error in uplaoding the csv file, Exiting....')
            return
    except Exception as e:
        log.info(f'Error occured : {str(e)}')


print(__name__)
if __name__ == '__main__':
    from timeit import default_timer as timer
    from datetime import timedelta
    start = timer()
    
    main()
    end = timer()
    print(f'Process completed. Time taken - {timedelta(seconds=end-start)}')
    


