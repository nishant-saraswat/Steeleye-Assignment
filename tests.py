# -*- coding: utf-8 -*-
"""
@author: Nishant Saraswat

Unit Testing module
"""

import unittest
import os
from xml_parser import parse_xml, convert_to_csv
from utils import upload_to_s3, download_file, unzip_file, read_config


class TestXMLExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Class method calls once at the beginning of unit test
        """

        # loading the configuration
        config = read_config()
        cls.url = config.get("xmlfile", "xml_url")

        # Extracting csv file path
        cls.csv_path = config.get("csv", "csv_path")

        # Extracting the download path
        cls.download_path = config.get("download", "download_path")

        # Extracting the required s3 information from config
        cls.bucket_name = config.get("aws", "bucket_name")
        cls.aws_access_key_id = config.get("aws", "aws_access_key_id")
        cls.aws_secret_access_key = config.get("aws", "aws_secret_access_key")
        cls.region_name = config.get("aws", "region_name")

    def setUp(self):
        """Instance Method called everytime before a test case is executed"""

        # Path to xml files
        self.xmlfilepath = os.path.join(
            os.getcwd(), TestXMLExtraction.download_path)

        # Path to csv file
        self.csvfile = os.path.join(os.getcwd(), TestXMLExtraction.csv_path)

    def test_download(self):
        """Function to test download function"""

        # Test for all correct data
        self.assertEqual(
            download_file(TestXMLExtraction.url,
                          self.xmlfilepath, "source_xml_file.xml"),
            self.xmlfilepath + os.sep + "source_xml_file.xml",
        )

        # Checking for incorrect url/invalid file type
        self.assertEqual(
            download_file("http://testurl.com", self.xmlfilepath,
                          "source_xml_file.xml"), ""
        )

        # Test for different download path
        self.assertEqual(
            download_file(
                TestXMLExtraction.url,
                os.path.join(os.getcwd(), "testpath"),
                "source_xml_file.xml",
            ),
            os.path.join(os.getcwd(), "testpath") +
            os.sep + "source_xml_file.xml",
        )

        # Test for incorrect download path
        self.assertEqual(download_file(TestXMLExtraction.url,
                         "E:", "source_xml_file.xml"), "")

    def test_parse_source_xml(self):
        """Function to test parse_source_xml function"""

        # Path to the source xml
        file = self.xmlfilepath + os.sep + "source_xml_file.xml"

        # Path to non existent source file
        in_file = self.xmlfilepath + os.sep + "source_xml_file.pwg"

        # Test for correct data
        # NOTE : For this test case to pass the source xml file should be
        # present in the download path
        self.assertEqual(
            parse_xml(file, condition=('file_type', 'DLTINS'),
                      output_elements=['file_name', 'download_link']),
            [
                "DLTINS_20210117_01of01.zip",
                "http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip"
            ],
        )

        # Test for incorrect data
        self.assertEqual(parse_xml(in_file,
                         condition=('file_type', 'DLTINS'),
                         output_elements=['file_name', 'download_link']),
                         None)

    def test_unzip_file(self):
        """Function to test unzip_file function"""

        # Path to the compressed file
        zipped_file = os.path.join(
            self.xmlfilepath, "DLTINS_20210117_01of01.zip")
        # Test for correct data
        # NOTE : For this test case to pass the source xml zipped file
        # should be present in the download path
        self.assertTrue(unzip_file(zipped_file, self.xmlfilepath))

        # Test for wrong target path
        self.assertFalse(unzip_file(zipped_file, r"D:\kqcA CK j "))

        # Test for incorrect compressed file
        self.assertFalse(unzip_file(r"D:\testfile", self.xmlfilepath))

    def test_create_csv(self):
        """Function to test create_csv funtion"""

        # absolute path to xml file to parse
        xml_file = os.path.join(self.xmlfilepath, "DLTINS_20210117_01of01.xml")

        # absolute path to the csv file to create
        csv_file = os.path.join(self.csvfile, "DLTINS_20210117_01of01.csv")

        # Test for correct data
        self.assertEqual(convert_to_csv(xml_file, self.csvfile), csv_file)

        # Test for incorrect input xml file
        self.assertEqual(convert_to_csv("somerandomfile", self.csvfile), None)

        # Test for incorrect path to write csv to
        self.assertEqual(convert_to_csv(xml_file, r"D:\kqcA CK j "), None)

    def aws_s3_upload(self):
        """Function to test aws_s3_upload function"""

        # absolute path to the csv file to create
        csv_file = os.path.join(self.csvfile, "DLTINS_20210117_01of01.csv")

        # Test for correct data
        self.assertTrue(
            upload_to_s3(
                csv_file,
                self.region_name,
                self.aws_access_key_id,
                self.aws_secret_access_key,
                self.bucket_name,
            )
        )

        # Test for non existent bucket
        self.assertFalse(
            upload_to_s3(
                csv_file,
                "useast",
                self.aws_access_key_id,
                self.aws_secret_access_key,
                self.bucket_name,
            )
        )

        # Test for non existent region
        self.assertFalse(
            upload_to_s3(
                csv_file,
                self.region_name,
                self.aws_access_key_id,
                self.aws_secret_access_key,
                "samplebucket",
            )
        )

        # Test for incorrect keys
        self.assertFalse(
            upload_to_s3(
                csv_file,
                self.region_name,
                "testkey",
                "testid",
                self.bucket_name,
            )
        )


if __name__ == "__main__":
    unittest.main()
