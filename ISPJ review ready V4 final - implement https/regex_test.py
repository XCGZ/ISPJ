# import re
# # defining regex
# password_pattern = r"^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]*$"
# credit_card_pattern = r"(\d{4} \d{4} \d{4} \d{4}|\d{16})"

# passwords = [
#     "password:12345abc",
#     "password: 12345abc",
#     "pass:12345abc!",
#     "password12345abc",
#     "pass: 12345abc",
#     "ddw"
# ]

# pattern = r"^(pass|password):?\s?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]*$"

# # Check if each password matches the regex
# for password in passwords:
#     if re.match(pattern, password):
#         print(f"Valid password: {password}")
#     else:
#         print(f"Invalid password: {password}")

# from spire.doc import *
import re
import cv2
import easyocr
from pdf2image import convert_from_path
import img2pdf
import re
import matplotlib.pyplot as plt
from PIL import Image
import os
import time
# from spire.doc.common import *

# patternss = [
#     """(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\\s?\\d{3}""",
# ]
patterns = {
"Password": r"^(Pass|pass|Password|password):?\s*?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]*\s*$",
"CVC": r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\s*$",
"NRIC": r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*$",
"Credit Card Number": r"^(Credit Card Number|Card Number|Credit Card|Card):?\s?\d{4} \d{4} \d{4} \d{4}|\d{16}\s*$"
}
# document = Document()
# document.LoadFromFile('test_data 1.docx')

# for key in patterns:
#     pattern = patterns[key]
#     if key == "Password":
#         regex = Regex(pattern)
#         document.Replace(regex, "Password: hidden")
#     else:
#         regex = Regex(pattern, RegexOptions.IgnoreCase)
#         document.Replace(regex, f"{key}: hidden")
# document.SaveToFile("ReplaceTextUsingRegexPattern.docx", FileFormat.Docx2016)
# document.Close()

# file_path = './test data 1.txt'

# password_pattern = r"^(Pass|pass|Password|password):?\s*([a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]+)\s*.*$"
# NRIC_pattern = r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\b"
# credit_card_pattern = r"^(Credit Card Number|Card Number|Credit Card|Card):?\s*?\d{4} \d{4} \d{4} \d{4}|\d{16}\b"
# CVC_pattern = r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\b"
# sensitive_dict_stats = {
#     'Passwords_Masked': 0,
#     'Credit_Card_Numbers_Masked': 0,
#     'NRIC_Masked': 0,
#     'CVC_Masked': 0
# }
# masking_options = ['Password', 'NRIC', 'CVC']

# patterns = {
#     "Password": r"^(Pass|pass|Password|password):?\s*([a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]+)\s*.*$",
#     "NRIC": NRIC_pattern,
#     "Credit Card Number": credit_card_pattern,
#     "CVC": CVC_pattern
# }
# for key in patterns:
#     pattern = patterns[key]
#     if key == "Password" and 'Password' in masking_options:
#         with open(file_path, 'r') as file:
#             file_contents = file.read()
#             detected_passwords = re.findall(pattern, file_contents, flags= re.MULTILINE)
#             sensitive_dict_stats['Passwords_Masked'] = len(detected_passwords)
#             updated_contents = re.sub(pattern, 'Password: [Hidden]', file_contents, flags= re.MULTILINE)
#         with open(file_path, 'w') as file:
#             file.write(updated_contents)
#     elif key == "NRIC" and 'NRIC' in masking_options:
#         with open(file_path, 'r') as file:
#             file_contents = file.read()
#             detected_NRICs = re.findall(pattern, file_contents, flags= re.IGNORECASE | re.MULTILINE)
#             sensitive_dict_stats['NRIC_Masked'] = len(detected_NRICs)
#             updated_contents = re.sub(pattern, 'NRIC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
#         with open(file_path, 'w') as file:
#             file.write(updated_contents)
#     elif key == "Credit Card Number" and 'Credit Card Number' in masking_options:
#         with open(file_path, 'r') as file:
#             file_contents = file.read()
#             detected_credit_cards = re.findall(pattern, file_contents, flags= re.IGNORECASE | re.MULTILINE)
#             sensitive_dict_stats['Credit_Card_Numbers_Masked'] = len(detected_credit_cards)
#             updated_contents = re.sub(pattern, 'Credit Card Number: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
#         with open(file_path, 'w') as file:
#             file.write(updated_contents)
#     elif key == "CVC" and 'CVC' in masking_options:
#         with open(file_path, 'r') as file:
#             file_contents = file.read()
#             detected_CVCs = re.findall(pattern, file_contents, flags= re.IGNORECASE | re.MULTILINE)
#             sensitive_dict_stats['CVC_Masked'] = len(detected_CVCs)
#             updated_contents = re.sub(pattern, 'CVC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
#         with open(file_path, 'w') as file:
#             file.write(updated_contents)
# print(sensitive_dict_stats)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(password_pattern, 'Password: [Hidden]', file_contents, flags= re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)
# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(NRIC_pattern, 'NRIC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(credit_card_pattern, 'Credit Card Number: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(CVC_pattern, 'CVC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(password_pattern, 'Password: [Hidden]', file_contents, flags= re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(NRIC_pattern, 'NRIC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(credit_card_pattern, 'Credit Card Number: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = re.sub(CVC_pattern, 'CVC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
# with open(file_path, 'w') as file:
#     file.write(updated_contents)

#     file_path = './test data 1.txt'

# password_pattern = r"^(Pass|pass|Password|password):?\s*([a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]+)\s*$"
# NRIC_pattern = r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*\b"
# credit_card_pattern = r"^(Credit Card Number|Card Number|Credit Card|Card):?\s*?\d{4} \d{4} \d{4} \d{4}|\d{16}\b"
# CVC_pattern = r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\b"
# sensitive_dict_stats = {
#     'Passwords_Masked': 0,
#     'Credit_Card_Numbers_Masked': 0,
#     'NRIC_Masked': 0,
#     'CVC_Masked': 0
# }

# def mask_sensitive_data_with_placeholders(pattern, replacement, file_contents):
#     # Temporarily replace the sensitive data with placeholders
#     temp_placeholder = "<<<TEMP_PLACEHOLDER>>>"
#     file_contents = re.sub(pattern, temp_placeholder, file_contents, flags=re.MULTILINE)
    
#     # Now, replace the placeholders with the final masked replacement
#     file_contents = re.sub(temp_placeholder, replacement, file_contents)
    
#     return file_contents

# # Reading, masking, and saving the content for each case
# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     print(file_contents)
#     updated_contents = mask_sensitive_data_with_placeholders(password_pattern, 'Password: [Hidden]', file_contents)
#     print(updated_contents)

# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     print(file_contents)

#     updated_contents = mask_sensitive_data_with_placeholders(NRIC_pattern, 'NRIC: [Hidden]', file_contents)
#     print(updated_contents)

# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = mask_sensitive_data_with_placeholders(credit_card_pattern, 'Credit Card Number: [Hidden]', file_contents)

# with open(file_path, 'w') as file:
#     file.write(updated_contents)

# with open(file_path, 'r') as file:
#     file_contents = file.read()
#     updated_contents = mask_sensitive_data_with_placeholders(CVC_pattern, 'CVC: [Hidden]', file_contents)

# with open(file_path, 'w') as file:
#     file.write(updated_contents)

file_path = './test_data 1.png'
image = cv2.imread(file_path)
inverted_image = cv2.bitwise_not(image)
cv2.imwrite('inverted_image.png', inverted_image)