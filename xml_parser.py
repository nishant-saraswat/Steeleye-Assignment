"""
@author: Nishant Saraswat

Module containing functions related to xml parsing
"""
import os
import pandas
from logger import log
# For parsing XML
from xml.etree import ElementTree as ET


def parse_xml(xml_file, condition, output_elements):
    """Parses the xml file for finding specific data
    Param(s):
        xml_file (str)    :   Path to the xml file
        condition (tuple) :   Condition to pick specific node from xml
        output_elements   :   The elements whose text is required in output
    Return(s):
        values (list)     :   Value for the required xml elements
    """
    try:
        log.info('Loading the xml file: {0}'.format(xml_file))
        # Loading the xml file contents
        xmlparse = ET.parse(xml_file)
        # Pulling the required xml root (result)
        log.info('Parsing the xml file')
        root = xmlparse.getroot()[1]
        # Finding all the elements with doc tag
        all_docs = root.findall('doc')
        log.info('Iterating over all the doc elements')
        for doc in all_docs:
            # Extracting the tag mentioned in condition
            tag = doc.find(".//str[@name='{0}']".format(condition[0]))
            # Checking if tag text matches value specified in the condition
            if tag.text == condition[1]:
                log.info('Found a for {0}'.format(condition[1]))
                log.info('Extracting the required attributes')
                # Created list for holding data for required elements
                values = list()
                for element in output_elements:
                    element_value = doc.find(
                        ".//str[@name='{0}']".format(element)).text
                    values.append(element_value)
                    log.info(
                        f'Attr Name: {element} Attr value: {element_value}')
                # Returning the required attributes
                return values
    except Exception as e:
        log.error(f"Error occurred - {str(e)}")


def convert_to_csv(xml_file_path, csv_path):
    """ Creates a CSV from the XML File
    Param(s):
        xml_file_path (str)  :   Path of XML file
        csv_path (str)       :   Path to write csv file
    Return(s):
        csv_file (str)       :   Path of csv file
    """
    # Initializing the required csv columns
    csv_columns = [
        "FinInstrmGnlAttrbts.Id",
        "FinInstrmGnlAttrbts.FullNm",
        "FinInstrmGnlAttrbts.ClssfctnTp",
        "FinInstrmGnlAttrbts.CmmdtyDerivInd",
        "FinInstrmGnlAttrbts.NtnlCcy",
        "Issr",
    ]

    # Creating a dataframe to hold values
    df_csv = pandas.DataFrame(columns=csv_columns)

    data_rows = []
    try:
        # Checking if the path exists or not
        if not os.path.exists(csv_path):
            # Creating the directory
            log.info("Creating CSV file path")
            os.makedirs(csv_path)

        # Initializing iterator to the xml file
        iter_xml = ET.iterparse(xml_file_path, events=("start",))
        for event, element in iter_xml:

            # Checking for 'TermntdRcrd' tag
            if 'TermntdRcrd' in element.tag:

                # Dictionary to hold data for a particular row
                dict_output = {}
                for nested_elem in element:

                    attr_tag = 'FinInstrmGnlAttrbts'
                    # Checking if we found FinInstrmGnlAttrbts
                    if attr_tag in nested_elem.tag:

                        # Traversing child elements of FinInstrmGnlAttrbts tag
                        for child in nested_elem:

                            child_tag = child.tag.partition('}')[2]
                            if '.'.join([attr_tag, child_tag]) in csv_columns:
                                dict_output['.'.join(
                                    [attr_tag, child_tag])] = child.text

                    if 'Issr' in nested_elem.tag:
                        dict_output['Issr'] = nested_elem.text

                data_rows.append(dict_output)

        # Appending data rows to dataframe
        df_csv = pandas.concat(
            [df_csv, pandas.DataFrame.from_records(data_rows)], axis=0)

        # Dropping empty rows if any
        log.info('Dropping empty rows')
        df_csv.dropna(inplace=True)

        log.info('Creating the csv file')

        converted_csv_path = os.path.join(
            csv_path, xml_file_path.split(os.sep)[-1].split(".")[0] + ".csv")
        df_csv.to_csv(converted_csv_path, index=False)
        log.info('CSV file successfully created after parsing xml')

        return converted_csv_path
    except Exception as e:
        log.error(f"Error occurred while extracting - {str(e)}")
