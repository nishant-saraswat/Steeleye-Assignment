# Steeleye-Assignment
--------------------

This repository consists of solution for Steeleye Python Developer assignment.
The solution is written in Python 3 language and requires some additional libraries to be installed.

## Table of contents
--------------------

* main.py
* utils.py
* logger.py
* config.cfg
* xml_parser.py

## Dependencies
---------------

The solution is using following python modules:

* os
* boto3
* pandas
* zipfile
* logging
* unittest
* requests
* xml.etree
* configparser


## Configuration
----------------

In config.cfg file the following configuration needs to be done:

* download_path

The relative path from the current directory of the controller script where source and target xml files needs to be downloaded by the script, the script is creating absolute path during it's run.

* csv_path

The relative path from the current directory of the controller script where the csv file needs to be created by the script, the script is creating absolute path during it's run.

* bucket_name

Provide the name of the S3 bucket to which file needs to be uploaded

* aws_access_key_id

Provide the AWS access key ID

* aws_secret_access_key

Provide the AWS secret access key

* region_name

Provide the AWS region in which the S3 bucket is hosted

## Files
--------

* config.cfg            : Configuration file consisting of paths and information required for script to work.

* main.py               : This is the main script that calls the specific function from utils and xml_parser modules to execute the steps for the assignment in the required sequence.

* utils                 : This module consists of all the common functions that are performing individual steps mentioned in the Assignment.

* logger.py             : This module initializes logger which is being used in the helper_functions and controller script for logging.

* tests.py              : This module performs the unit test.
* requirements.txt      : Contains additional libraries required for the project to run

