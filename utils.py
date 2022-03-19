"""
@author: Nishant Saraswat

Module containing all the common functions for the process
"""
import os
import boto3
import requests
import zipfile
from logger import log
from configparser import RawConfigParser


def read_config():
    """Reads config file
    Return(s):
        config (RawConfigParser)  :  Object containing the config information
    """
    # Accessing config variable
    try:
        log.info("Loading the config file")
        # Loading the config file
        config = RawConfigParser()
        config.read("config.cfg")
        log.info("Config file loaded successfully")
    except Exception as e:
        log.error(f"Error in loading config file : {str(e)}.")
    return config


def download_file(url, file_download_path, file_name):
    """Downloads the file to the download path using file url supplied as argument
    Param(s):
        url (str)                 :   link for downloading file
        file_download_path (str)  :   path for downloaded file
        filename (str)            :   filename to give the downlaoded xml
    Return(s):
        file (str)                :   absolute path to the downloaded xml file
    """
    log.info('Inside :-> download_file() function')
    complete_download_path = ''
    try:
        # Getting file contents from url
        log.info('Pulling file contents from url: {0}'.format(url))
        response = requests.get(url)

        # Checking if the correct response is received
        if response.ok:
            # Checking if the directory provided in download path exists
            if not os.path.exists(file_download_path):
                # Creating the directory
                os.makedirs(file_download_path)
            complete_download_path = os.path.join(
                file_download_path, file_name)
            # writing the file at the download path
            log.info('Writing the file at the download path: {0}'.format(
                complete_download_path))
            with open(complete_download_path, "wb") as f:
                f.write(response.content)
        else:
            log.error('Error in downloading xml file')
    except Exception as e:
        log.error(
            'Error in downloading xml file from location : {url} - {str(e)}')
    log.info('Exiting :-> download_file() function')
    return complete_download_path


def unzip_file(path_to_zip_file, directory_to_extract_to):
    """Unzips the compressed file to the path provided
    Param(s):
        path_to_zip_file (str)          : Compressed File path
        directory_to_extract_to (str)   : Path for the uncompressed file
    """
    try:
        log.info('Unzipping the compressed file')
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
            log.info('Extracted file from compressed file')
            return True
    except Exception as e:
        log.error(f"Error occurred while extracting - {str(e)}")
        return False


def upload_to_s3(region_name, aws_access_key, aws_secret_key,
                 bucket_name, file_path):
    """Uploads the file to s3 bucket
    Param(s):
        file_path (str)             :   Path of file to upload to s3 bucket
        region_name (str)           :   region name for s3 bucket
        aws_access_key_id (str)     :   AWS access key
        aws_secret_access_key (str) :   AWS secret access key
        bucket_name (str)           :   bucket name
    Return(s):
        True (bool) : True for successful upload
    """

    # Create an S3 access object
    try:
        # Extracting the file name
        filename_in_s3 = file_path.split(os.sep)[-1]
        log.info('Creating an s3 resource object')
        s3 = boto3.resource(
            service_name="s3",
            region_name=region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )
        log.info('Uploading the file to s3 bucket')
        s3.Bucket(bucket_name).upload_file(
            Filename=file_path, Key=filename_in_s3)
        log.info(
            'Uploaded file successfully to s3 bucket {0}'.format(bucket_name))
        # Returning true for successful file upload to s3 bucket
        return True
    except Exception as e:
        log.error(f"Error occurred while extracting - {str(e)}")
