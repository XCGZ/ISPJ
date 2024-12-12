import easyocr
from pdf2image import convert_from_path
import img2pdf
import cv2
import re
import matplotlib.pyplot as plt
from PIL import Image
import os
import time
from spire.doc import *
from spire.doc.common import *


# Initialize ocr model

ocr_reader = easyocr.Reader(['en'])

# defining regex
password_pattern = r"^(Pass|pass|Password|password):?\s*?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]*\s*$"
NRIC_pattern = r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*$"
credit_card_pattern = r"^(Credit Card Number|Card Number|Credit Card|Card):?\s*?\d{4} \d{4} \d{4} \d{4}|\d{16}\s*$"
CVC_pattern = r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\s*$"

def calc_font_scale(sensitive_dict):
    font_scale_list = []
    for key in sensitive_dict:
        top_left_corner = sensitive_dict[key][1][0]
        bottom_right_corner = sensitive_dict[key][1][2]
        font_scale = (bottom_right_corner[1] - top_left_corner[1]) / 40
        font_scale_list.append(font_scale)
    return (min(font_scale_list))

# User inputs. when user upload file, stored here
# user uploads file, it stored on my pc. i will get the file path and store it here. after that, i get the filename without the ./ part and save the pages as file_page 1...n.png.
# maybe everytime a user uploads, i create new folder for them, this is to prevent collisions.
user_file_path = './test_data_multi_page 2.pdf'
filename = ''

def mask_pdf(user_file_path):
    images = convert_from_path(user_file_path)
    edited_images_list = []


    for i in range(len(images)):
        images[i].save('test_data_page'+ str(i) +'.png')

    for i in range(len(images)):
        img = cv2.imread('test_data_page'+ str(i) +'.png')
        output = ocr_reader.readtext(img)
        sensitive_dict = {}
        for (bbox, text, prob) in output:
            print(text)
            if re.match(password_pattern, text):
                print(f'password found: {text}')
                sensitive_dict['Password'] = text, bbox
            elif re.match(credit_card_pattern, text, re.IGNORECASE):
                print(f'credit card found: {text}')
                sensitive_dict['Credit_Card_Number'] = text, bbox
            elif re.match(NRIC_pattern, text, re.IGNORECASE):
                print(f'NRIC found: {text}')
                sensitive_dict['NRIC'] = text, bbox
            elif re.match(CVC_pattern, text, re.IGNORECASE):
                print(f'CVC found: {text}')
                sensitive_dict['CVC'] = text, bbox

        # CV2 image manipulation
        for key in sensitive_dict:
            top_left_corner = sensitive_dict[key][1][0]
            bottom_right_corner = sensitive_dict[key][1][2]
            middle_left_x = top_left_corner[0]
            middle_left_y = (top_left_corner[1] + bottom_right_corner[1]) // 2
            font_scale = calc_font_scale(sensitive_dict)
            background_color_bgr = tuple(img[0, 0])
            print(background_color_bgr)

            cv2.rectangle(img, top_left_corner, bottom_right_corner, (int(background_color_bgr[0]), int(background_color_bgr[1]), int(background_color_bgr[2])), -1)
            cv2.putText(img, f"{key.replace('_',' ')}: [Hidden]", (middle_left_x, middle_left_y + 6), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), 2, cv2.LINE_AA)
        cv2.imwrite('test_data_page_edited'+ str(i) + '.png', img)
        os.remove('test_data_page'+ str(i) +'.png')
        edited_image = Image.open('test_data_page_edited' + str(i) + '.png')
        edited_images_list.append(edited_image.filename)
        edited_image.close()

    # # Convert all images to a single PDF
    # if edited_images_list:
    #     first_image = Image.open(edited_images_list[0])
    #     for img in edited_images_list[1:]:
    #         rest_images = [Image.open(img)]
    #     first_image.save(f'./test/manga_app_translated.pdf', save_all=True, append_images=rest_images)

    if edited_images_list:
        with open('test_data_page_edited 2.pdf', 'wb') as f:
            pdf_bytes = img2pdf.convert(edited_images_list)

            f.write(pdf_bytes)

    for img in edited_images_list:
        os.remove(img)

def mask_image(user_file_path):
    img = cv2.imread(user_file_path)
    output = ocr_reader.readtext(img)
    sensitive_dict = {}
    for (bbox, text, prob) in output:
        print(text)
        if re.match(password_pattern, text):
            print(f'password found: {text}')
            sensitive_dict['Password'] = text, bbox
        elif re.match(credit_card_pattern, text, re.IGNORECASE):
            print(f'credit card found: {text}')
            sensitive_dict['Credit_Card_Number'] = text, bbox
        elif re.match(NRIC_pattern, text, re.IGNORECASE):
            print(f'NRIC found: {text}')
            sensitive_dict['NRIC'] = text, bbox
        elif re.match(CVC_pattern, text, re.IGNORECASE):
            print(f'CVC found: {text}')
            sensitive_dict['CVC'] = text, bbox

        # CV2 image manipulation
        for key in sensitive_dict:
            top_left_corner = sensitive_dict[key][1][0]
            bottom_right_corner = sensitive_dict[key][1][2]
            middle_left_x = top_left_corner[0]
            middle_left_y = (top_left_corner[1] + bottom_right_corner[1]) // 2
            font_scale = calc_font_scale(sensitive_dict)
            background_color_bgr = tuple(img[0, 0])
            print(background_color_bgr)

            cv2.rectangle(img, top_left_corner, bottom_right_corner, (int(background_color_bgr[0]), int(background_color_bgr[1]), int(background_color_bgr[2])), -1)
            cv2.putText(img, f"{key.replace('_',' ')}: [Hidden]", (middle_left_x, middle_left_y + 6), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), 2, cv2.LINE_AA)
        cv2.imwrite('test_data 1 edited.png', img)
        os.remove('test_data 1.png')

def mask_txt(file_path):
    password_pattern = r"^(Pass|pass|Password|password):?\s*([a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]+)\s*.*$"
    NRIC_pattern = r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*.*$"
    credit_card_pattern = r"^(Credit Card Number|Card Number|Credit Card|Card):?\s*?\d{4} \d{4} \d{4} \d{4}|\d{16}\s*$"
    CVC_pattern = r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\s*$"

    file_path = 'test_data 1.txt'

    with open(file_path, 'r') as file:
        file_contents = file.read()
        updated_contents = re.sub(password_pattern, f'Password: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
    with open(file_path, 'w') as file:
        file.write(updated_contents)

    with open(file_path, 'r') as file:
        file_contents = file.read()
        updated_contents = re.sub(NRIC_pattern, f'NRIC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
    with open(file_path, 'w') as file:
        file.write(updated_contents)

    with open(file_path, 'r') as file:
        file_contents = file.read()
        updated_contents = re.sub(credit_card_pattern, f'Credit Card Number: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
    with open(file_path, 'w') as file:
        file.write(updated_contents)

    with open(file_path, 'r') as file:
        file_contents = file.read()
        updated_contents = re.sub(CVC_pattern, f'CVC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
    with open(file_path, 'w') as file:
        file.write(updated_contents)

def mask_docx():
    patterns = {
    "Password": r"^(Pass|pass|Password|password):?\s*?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]*\s*$",
    "CVC": r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\s*$",
    "NRIC": r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*$",
    "Credit Card Number": r"^(Credit Card Number|Card Number|Credit Card|Card):?\s?\d{4} \d{4} \d{4} \d{4}|\d{16}\s*$"
    }
    document = Document()
    document.LoadFromFile('test_data 1.docx')

    for key in patterns:
        pattern = patterns[key]
        if key == "Password":
            regex = Regex(pattern)
            document.Replace(regex, "Password: hidden")
        else:
            regex = Regex(pattern, RegexOptions.IgnoreCase)
            document.Replace(regex, f"{key}: hidden")
    document.SaveToFile("ReplaceTextUsingRegexPattern.docx", FileFormat.Docx2016)
    document.Close()

def mask_csv():
    pass

def mask_file_type(filename):
    split_tup = os.path.splitext(filename)
    file_type = split_tup[1]
    if file_type == '.pdf':
        mask_pdf(user_file_path)
    elif file_type == '.png' or file_type == '.jpg' or file_type == '.jpeg':
        mask_image(user_file_path)
    elif file_type == '.txt':
        mask_txt(user_file_path)
    elif file_type == '.docx':
        mask_docx(user_file_path)
    elif file_type == '.csv':
        mask_csv(user_file_path)
    else:
        print('Invalid file format. Please upload a pdf or png file.')
