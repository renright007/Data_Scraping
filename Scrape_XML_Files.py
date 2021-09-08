
import extract_msg
import os.path
import pandas as pd
from os import path
from independentsoft.msg import Message
from independentsoft.msg import Attachment
from bs4 import BeautifulSoup as BS
from datetime import datetime

vaccine_details = {

    "File Name": [],
    "PHN": [],
    "First Name": [],
    "Last Name": [],
    "DOB": [],
    "Phone": [],
    "Email": [],
    "Address": [],
    "City": [],
    "Province": [],
    "Postal Code": [],
    "Dose 1 - Vaccination Date": [],
    "Dose 1 - Product": [],
    "Dose 1 - Other Product": [],
    "Dose 1 - Origin" : [],
    "Dose 1 - Lot Number": [],
    "Dose 1 - Injection Site": [],
    "Dose 2 - Vaccination Date": [],
    "Dose 2 - Product": [],
    "Dose 2 - Other Product": [],
    "Dose 2 - Origin" : [],
    "Dose 2 - Lot Number": [],
    "Dose 2 - Injection Site": []
    }

dest_path = "O:/BCCDC/Groups/Data_Projects/PPHIS_Projects/Support_Operations/Robert/Historical Imms/Text Files/"

def scrape_vax_info(directory):

    for filename in os.scandir(directory):
        
        try:

            if os.path.join(directory, filename).endswith('.msg'):
            
                message = Message(os.path.join(directory, filename))  
                attachments = message.attachments

                for attachment in attachments:
                
                        if attachment.file_name.endswith('.xml'):

                            xml_attachment = attachment
                            xml_file_name = str(xml_attachment.file_name)
                            xml_attachment.save(dest_path + xml_file_name)

                            file = open(dest_path + xml_file_name, "r")    # Open XML file
                            contents = file.read()  # Read the file

                            soup = BS(contents,'xml')   # Use BS to access contents

                            # Add the details from the XML file to the dictionary

                            # File Name
                            vaccine_details["File Name"].append(str(filename)[11:].replace("'>","")) 
                            vaccine_details["PHN"].append(soup.find('phn').text) # BC PHN Identifier
    
                            # Demographic Info
                            vaccine_details["First Name"].append(soup.find('first-name').text)
                            vaccine_details["Last Name"].append(soup.find('last-name').text)
                            vaccine_details["DOB"].append(soup.find('dob').text)
                            vaccine_details["Phone"].append(soup.find('phone').text)
                            vaccine_details["Email"].append(soup.find('email').text)
                            vaccine_details["Address"].append(soup.find('control-1').text)
                            vaccine_details["City"].append(soup.find('control-3').text)
                            vaccine_details["Province"].append(soup.find('control-4').text)
                            vaccine_details["Postal Code"].append(soup.find('control-5').text)

                            # Dose 1 - Vaccine Info
                            if soup.find('date') is None:
                                vaccine_details["Dose 1 - Vaccination Date"].append('')
                            else:
                                vaccine_details["Dose 1 - Vaccination Date"].append(soup.find('date').text)

                            if soup.find('product') is None:
                                vaccine_details["Dose 1 - Product"].append('')
                            else:
                                vaccine_details["Dose 1 - Product"].append(soup.find('product').text)

                            if soup.find('other') is None:
                                vaccine_details["Dose 1 - Other Product"].append('')
                            else:
                                vaccine_details["Dose 1 - Other Product"].append(soup.find('other').text)
                    
                            if soup.find('origin') is None:
                                vaccine_details["Dose 1 - Origin"].append('')
                            else:
                                vaccine_details["Dose 1 - Origin"].append(soup.find('origin').text)

                            if soup.find('lot') is None:
                                vaccine_details["Dose 1 - Lot Number"].append('')
                            else:
                                vaccine_details["Dose 1 - Lot Number"].append(soup.find('lot').text.strip())
                    
                            if soup.find('lot') is None:
                                vaccine_details["Dose 1 - Injection Site"].append('')
                            else:                    
                                vaccine_details["Dose 1 - Injection Site"].append(soup.find('injection-site').text)

                            # Dose 2 - Vaccine Info
                            if soup.find('date2') is None:
                                vaccine_details["Dose 2 - Vaccination Date"].append('')
                            else:
                                vaccine_details["Dose 2 - Vaccination Date"].append(soup.find('date2').text)

                            if soup.find('product2') is None:
                                vaccine_details["Dose 2 - Product"].append('')
                            else:
                                vaccine_details["Dose 2 - Product"].append(soup.find('product2').text)

                            if soup.find('other2') is None:
                                vaccine_details["Dose 2 - Other Product"].append('')
                            else:
                                vaccine_details["Dose 2 - Other Product"].append(soup.find('other2').text)
                    
                            if soup.find('origin2') is None:
                                vaccine_details["Dose 2 - Origin"].append('')
                            else:
                                vaccine_details["Dose 2 - Origin"].append(soup.find('origin2').text)

                            if soup.find('lot2') is None:
                                vaccine_details["Dose 2 - Lot Number"].append('')
                            else:
                                vaccine_details["Dose 2 - Lot Number"].append(soup.find('lot2').text.strip())
                    
                            if soup.find('injection-site2') is None:
                                vaccine_details["Dose 2 - Injection Site"].append('')
                            else:                    
                                vaccine_details["Dose 2 - Injection Site"].append(soup.find('injection-site2').text)

        except:
            pass


scrape_vax_info(r'\\phsabc.ehcnet.ca\root\BCCDC\Groups\Data_Projects\PPHIS_Projects\Support_Operations\PPHIS Data Remediation\2 Activities\Adding Historical Imms\02a - Complete-Out of Province')
scrape_vax_info(r'\\phsabc.ehcnet.ca\root\BCCDC\Groups\Data_Projects\PPHIS_Projects\Support_Operations\PPHIS Data Remediation\2 Activities\Adding Historical Imms\02b - Complete in BC')

vaccine_details

vax_df = pd.DataFrame.from_dict(vaccine_details)

today = datetime.today().strftime('%Y-%m-%d')
# vax_df = pd.DataFrame.from_dict(vaccine_details, orient='index')

# vax_df = vax_df.transpose()

vax_df.to_csv('O:\BCCDC\Groups\Data_Projects\PPHIS_Projects\Support_Operations\Robert\Historical Imms\Vax Info Exports\Complete Imms Vax Details {}.csv'.format(today))

# scrape_vax_info(r'O:\BCCDC\Groups\Data_Projects\PPHIS_Projects\Support_Operations\Robert\Historical Imms\Rob')


