from flask import (Blueprint, Flask, flash, g, jsonify, make_response,
                   redirect, render_template, request, session, url_for, send_file)
from zj_forms import FileUploadForm
import os
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

# General app config
app = Flask(__name__,
            static_url_path='',
            static_folder='static',)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Initialize ocr model

ocr_reader = easyocr.Reader(['en'])

# defining regex
password_pattern = r"^(Pass|pass|Password|password):?\s*?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]*\s*$"
NRIC_pattern = r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*$"
credit_card_pattern = r"^(Credit Card Number|Card Number|Credit Card|Card):?\s*?\d{4} \d{4} \d{4} \d{4}|\d{16}\s*$"
CVC_pattern = r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\s*$"

# calculate font scale for puttext
def calc_font_scale(sensitive_dict):
    font_scale_list = []
    for key in sensitive_dict:
        for item in sensitive_dict[key]:
            print(item)
            top_left_corner = item[1][0]
            bottom_right_corner = item[1][2]
            font_scale = (bottom_right_corner[1] - top_left_corner[1]) / 40
            font_scale_list.append(font_scale)
    return (min(font_scale_list))

# file upload functions
def mask_pdf(file, masking_options):
    file_path = file_path = os.path.join('./','uploaded_files', 'masked_files', file)
    images = convert_from_path(file_path)
    edited_images_list = []
    sensitive_dict_stats = {
        'Passwords_Masked': 0,
        'Credit_Card_Numbers_Masked': 0,
        'NRIC_Masked': 0,
        'CVC_Masked': 0
    }


    for i in range(len(images)):
        new_file_path = os.path.join('./','uploaded_files', 'masked_files', f'{file}_page {i}.png')
        images[i].save(new_file_path)
        print(new_file_path)

    for i in range(len(images)):
        new_file_path = os.path.join('./','uploaded_files', 'masked_files', f'{file}_page {i}.png')
        img = cv2.imread(new_file_path)
        img = cv2.bitwise_not(img)
        output = ocr_reader.readtext(img)
        img = cv2.bitwise_not(img)
        sensitive_dict = {
            'Password': [],
            'Credit_Card_Number': [],
            'NRIC': [],
            'CVC': []
        }
        for (bbox, text, prob) in output:
            print(text)
            if 'Password' in masking_options and re.match(password_pattern, text):
                print(f'password found: {text}')
                if 'Password' in sensitive_dict:
                    sensitive_dict['Password'].append((text, bbox))
                    sensitive_dict_stats['Passwords_Masked'] += 1
                else:
                    sensitive_dict['Password'].append((text, bbox))
                    sensitive_dict_stats['Passwords_Masked'] += 1
            elif 'Credit Card Number' in masking_options and re.match(credit_card_pattern, text, re.IGNORECASE):
                print(f'credit card found: {text}')
                if 'Credit_Card_Number' in sensitive_dict:
                    sensitive_dict['Credit_Card_Number'].append((text, bbox))
                    sensitive_dict_stats['Credit_Card_Numbers_Masked'] += 1
                else:
                    sensitive_dict['Credit_Card_Number'].append((text, bbox))
                    sensitive_dict_stats['Credit_Card_Numbers_Masked'] += 1
            elif 'NRIC' in masking_options and re.match(NRIC_pattern, text, re.IGNORECASE):
                print(f'NRIC found: {text}')
                if 'NRIC' in sensitive_dict:
                    sensitive_dict['NRIC'].append((text, bbox))
                    sensitive_dict_stats['NRIC_Masked'] += 1
                else:
                    sensitive_dict['NRIC'].append((text, bbox))
                    sensitive_dict_stats['NRIC_Masked'] += 1
            elif 'CVC' in masking_options and re.match(CVC_pattern, text, re.IGNORECASE):
                print(f'CVC found: {text}')
                if 'CVC' in sensitive_dict:
                    sensitive_dict['CVC'].append((text, bbox))
                    sensitive_dict_stats['CVC_Masked'] += 1
                else:
                    sensitive_dict['CVC'].append((text, bbox))
                    sensitive_dict_stats['CVC_Masked'] += 1

        # CV2 image manipulation
        for key in sensitive_dict:
            for item in sensitive_dict[key]:
                print(item)
                top_left_corner = item[1][0]
                bottom_right_corner = item[1][2]
                middle_left_x = top_left_corner[0]
                middle_left_y = (top_left_corner[1] + bottom_right_corner[1]) // 2
                font_scale = calc_font_scale(sensitive_dict)
                background_color_bgr = tuple(img[0, 0])
                print(background_color_bgr)

                cv2.rectangle(img, top_left_corner, bottom_right_corner, (int(background_color_bgr[0]), int(background_color_bgr[1]), int(background_color_bgr[2])), -1)
                cv2.putText(img, f"{key.replace('_',' ')}: [Hidden]", (middle_left_x, middle_left_y + 6), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), 2, cv2.LINE_AA)
        new_edited_file_path = new_file_path.replace('.png', ' edited.png')
        cv2.imwrite(new_edited_file_path, img)
        os.remove(new_file_path)
        edited_image = Image.open(new_edited_file_path)
        edited_images_list.append(edited_image.filename)
        edited_image.close()

    # # Convert all images to a single PDF
    # if edited_images_list:
    #     first_image = Image.open(edited_images_list[0])
    #     for img in edited_images_list[1:]:
    #         rest_images = [Image.open(img)]
    #     first_image.save(f'./test/manga_app_translated.pdf', save_all=True, append_images=rest_images)

    if edited_images_list:
        with open(file_path, 'wb') as f:
            pdf_bytes = img2pdf.convert(edited_images_list)

            f.write(pdf_bytes)

    for img in edited_images_list:
        print(img)
        os.remove(img)
    return sensitive_dict_stats

def mask_image(file, masking_options):
    file_path = os.path.join('./','uploaded_files', 'masked_files', file)
    image = cv2.imread(file_path)
    img = cv2.bitwise_not(image)
    output = ocr_reader.readtext(img, mag_ratio=4)
    img = cv2.bitwise_not(img)
    sensitive_dict = {
        'Password': [],
        'Credit_Card_Number': [],
        'NRIC': [],
        'CVC': []
    }
    sensitive_dict_stats = {
        'Passwords_Masked': 0,
        'Credit_Card_Numbers_Masked': 0,
        'NRIC_Masked': 0,
        'CVC_Masked': 0
    }
    background_color_bgr = tuple(img[0, 0])
    print(background_color_bgr)
    for (bbox, text, prob) in output:
        if 'cvvv' in text.lower():
            text = text.lower().replace('cvvv', 'cvc')
            print(text)
        if 'Password' in masking_options and re.match(password_pattern, text):
            print(f'password found: {text}')
            if 'Password' in sensitive_dict:
                sensitive_dict['Password'].append((text, bbox))
                sensitive_dict_stats['Passwords_Masked'] += 1
            else:
                sensitive_dict['Password'].append((text, bbox))
                sensitive_dict_stats['Passwords_Masked'] += 1
        elif 'Credit Card Number' in masking_options and re.match(credit_card_pattern, text, re.IGNORECASE):
            print(f'credit card found: {text}')
            if 'Credit_Card_Number' in sensitive_dict:
                sensitive_dict['Credit_Card_Number'].append((text, bbox))
                sensitive_dict_stats['Credit_Card_Numbers_Masked'] += 1
            else:
                sensitive_dict['Credit_Card_Number'].append((text, bbox))
                sensitive_dict_stats['Credit_Card_Numbers_Masked'] += 1
        elif 'NRIC' in masking_options and re.match(NRIC_pattern, text, re.IGNORECASE):
            print(f'NRIC found: {text}')
            if 'NRIC' in sensitive_dict:
                sensitive_dict['NRIC'].append((text, bbox))
                sensitive_dict_stats['NRIC_Masked'] += 1
            else:
                sensitive_dict['NRIC'].append((text, bbox))
                sensitive_dict_stats['NRIC_Masked'] += 1
        elif 'CVC' in masking_options and re.match(CVC_pattern, text, re.IGNORECASE):
            print(f'CVC found: {text}')
            if 'CVC' in sensitive_dict:
                sensitive_dict['CVC'].append((text, bbox))
                sensitive_dict_stats['CVC_Masked'] += 1
            else:
                sensitive_dict['CVC'].append((text, bbox))
                sensitive_dict_stats['CVC_Masked'] += 1

    # CV2 image manipulation
    for key in sensitive_dict:
        for item in sensitive_dict[key]:
            print(item)
            top_left_corner = item[1][0]
            bottom_right_corner = item[1][2]
            middle_left_x = top_left_corner[0]
            middle_left_y = (top_left_corner[1] + bottom_right_corner[1]) // 2
            font_scale = calc_font_scale(sensitive_dict)
            print(background_color_bgr)

            cv2.rectangle(img, top_left_corner, bottom_right_corner, (int(background_color_bgr[0]), int(background_color_bgr[1]), int(background_color_bgr[2])), -1)
            cv2.putText(img, f"{key.replace('_',' ')}: [Hidden]", (middle_left_x, middle_left_y + 6), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), 3, cv2.LINE_AA)
    cv2.imwrite(file_path, img)
    print(sensitive_dict_stats)
    return sensitive_dict_stats

def mask_txt(file, masking_options):
    file_path = os.path.join(r'.\\','uploaded_files', 'masked_files', file)
    password_pattern = r"^(Pass|pass|Password|password):?\s*([a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]+)\s*.*$"
    NRIC_pattern = r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\b"
    credit_card_pattern = r"^(Credit Card Number|Card Number|Credit Card|Card):?\s*?\d{4} \d{4} \d{4} \d{4}|\d{16}\b"
    CVC_pattern = r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\b"
    patterns = {
        "Password": r"^(Pass|pass|Password|password):?\s*([a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]+)\s*.*$",
        "NRIC": NRIC_pattern,
        "Credit Card Number": credit_card_pattern,
        "CVC": CVC_pattern
    }
    sensitive_dict_stats = {
        'Passwords_Masked': 0,
        'Credit_Card_Numbers_Masked': 0,
        'NRIC_Masked': 0,
        'CVC_Masked': 0
    }

    for key in patterns:
        pattern = patterns[key]
        if key == "Password" and 'Password' in masking_options:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                detected_passwords = re.findall(pattern, file_contents, flags= re.MULTILINE)
                sensitive_dict_stats['Passwords_Masked'] = len(detected_passwords)
                updated_contents = re.sub(pattern, 'Password: [Hidden]', file_contents, flags= re.MULTILINE)
            with open(file_path, 'w') as file:
                file.write(updated_contents)
        elif key == "NRIC" and 'NRIC' in masking_options:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                detected_NRICs = re.findall(pattern, file_contents, flags= re.IGNORECASE | re.MULTILINE)
                sensitive_dict_stats['NRIC_Masked'] = len(detected_NRICs)
                updated_contents = re.sub(pattern, 'NRIC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
            with open(file_path, 'w') as file:
                file.write(updated_contents)
        elif key == "Credit Card Number" and 'Credit Card Number' in masking_options:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                detected_credit_cards = re.findall(pattern, file_contents, flags= re.IGNORECASE | re.MULTILINE)
                sensitive_dict_stats['Credit_Card_Numbers_Masked'] = len(detected_credit_cards)
                updated_contents = re.sub(pattern, 'Credit Card Number: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
            with open(file_path, 'w') as file:
                file.write(updated_contents)
        elif key == "CVC" and 'CVC' in masking_options:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                detected_CVCs = re.findall(pattern, file_contents, flags= re.IGNORECASE | re.MULTILINE)
                sensitive_dict_stats['CVC_Masked'] = len(detected_CVCs)
                updated_contents = re.sub(pattern, 'CVC: [Hidden]', file_contents, flags= re.IGNORECASE | re.MULTILINE)
            with open(file_path, 'w') as file:
                file.write(updated_contents)
    return sensitive_dict_stats

def mask_docx(file, masking_options):
    patterns = {
    "Password": r"^(Pass|pass|Password|password):?\s*?[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{8,}\s*$",
    "CVC": r"^(CVC|Card Verification Code|card verification code|CVV|Card Verification Value):?\s*?\d{3}\s*$",
    "NRIC": r"^(IC|ic|NRIC|nric|National Registration Identity Card|national registration identity card)\s*?(Number|number|Num|num)?:?\s*?[STFG]\d{7}[A-Z]\s*$",
    "Credit Card Number": r"^(Credit Card Number|Card Number|Credit Card|Card):?\s?\d{4} \d{4} \d{4} \d{4}|\d{16}\s*$"
    }
    sensitive_dict_stats = {
        'Passwords_Masked': 0,
        'Credit_Card_Numbers_Masked': 0,
        'NRIC_Masked': 0,
        'CVC_Masked': 0
    }
    file_path = os.path.join('./','uploaded_files', 'masked_files', file)
    document = Document()
    document.LoadFromFile(file_path)

    for key in patterns:
        pattern = patterns[key]
        if key == "Password" and 'Password' in masking_options:
            regex = Regex(pattern)
            detected_passwords = document.FindAllPattern(regex)
            print(re.findall(pattern, document.GetText(), flags= re.MULTILINE))
            sensitive_dict_stats['Passwords_Masked'] = len(detected_passwords)
            document.Replace(regex, "Password: hidden")

        elif key == "NRIC" and 'NRIC' in masking_options:
            regex = Regex(pattern, RegexOptions.IgnoreCase)
            detected_NRICs = document.FindAllPattern(regex)
            sensitive_dict_stats['NRIC_Masked'] = len(detected_NRICs)
            document.Replace(regex, f"{key}: hidden")

        elif key == "Credit Card Number" and 'Credit Card Number' in masking_options:
            regex = Regex(pattern, RegexOptions.IgnoreCase)
            detected_credit_cards = document.FindAllPattern(regex)
            sensitive_dict_stats['Credit_Card_Numbers_Masked'] = len(detected_credit_cards)
            document.Replace(regex, f"{key}: hidden")

        elif key == "CVC" and 'CVC' in masking_options:
            regex = Regex(pattern, RegexOptions.IgnoreCase)
            detected_CVCs = document.FindAllPattern(regex)
            sensitive_dict_stats['CVC_Masked'] = len(detected_CVCs)
            document.Replace(regex, f"{key}: hidden")

    document.SaveToFile(file_path, FileFormat.Docx2016)
    document.Close()
    return sensitive_dict_stats

def mask_csv():
    pass

def mask_file_type(file, file_path, masking_options):
    split_tup = os.path.splitext(file)
    print(file)
    file_type = split_tup[1]
    filename = split_tup[0]
    if file_type == '.pdf':
        masked_file_stats_dict = mask_pdf(file, masking_options)
        return masked_file_stats_dict
    elif file_type == '.png' or file_type == '.jpg' or file_type == '.jpeg':
        masked_file_stats_dict = mask_image(file, masking_options)
        return masked_file_stats_dict
    elif file_type == '.txt':
        masked_file_stats_dict = mask_txt(file, masking_options)
        return masked_file_stats_dict
    elif file_type == '.docx':
        masked_file_stats_dict = mask_docx(file, masking_options)
        return masked_file_stats_dict
    elif file_type == '.csv':
        mask_csv(file, masking_options)
    else:
        print('Invalid file format. Please upload a pdf or png file.')

# routes
# Home/Root route
@app.route('/')
def home():
    return render_template('home.html')
# File upload route
@app.route('/fileUpload', methods=['GET', 'POST'])
def file_upload():
    file_upload_form = FileUploadForm(request.form)
    if request.method == 'POST':
        file = request.files['file_upload_field']
        masking_options = file_upload_form.masking_options.data
        print(masking_options)
        original_filepath = os.path.join('./','uploaded_files', 'original_files', file.filename)
        masked_filepath = os.path.join('./','uploaded_files', 'masked_files', file.filename)
        file_contents = file.read()
        with open(original_filepath, 'wb') as f:
            f.write(file_contents)
        with open(masked_filepath, 'wb') as f:
            f.write(file_contents)
        masked_file_stats_dict = mask_file_type(file.filename, masked_filepath, masking_options)
        if file:
            flash('File uploaded and contents have been masked successfully', 'success')
            return render_template('file_upload.html', form = file_upload_form, file=file.filename, masked_file_stats_dict=masked_file_stats_dict)
        return redirect(url_for('file_upload'))
    else:

        return render_template('file_upload.html', form = file_upload_form)

@app.route('/DownloadFile', methods=['GET', 'POST'])
def download_masked_file():
    if request.method == 'POST':
        file = request.form.get('file')
        print(file)

        path = os.path.join('./','uploaded_files', 'masked_files', file)

        return send_file(path, as_attachment=True)
    else:
        return redirect(url_for('file_upload'))
if __name__ == '__main__':
    app.run(port=3306, debug=True, ssl_context=("certs/cert.pem", "certs/key.pem"))
