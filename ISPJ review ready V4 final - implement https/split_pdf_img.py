from pdf2image import convert_from_path

# Path to the PDF file
PDF_file = "test_data 1.pdf"

# Store all the pages of the PDF in a variable
images = convert_from_path(PDF_file)

for i in range(len(images)):
    file_path = './test_data 1' + str(i + 2) + '.png'
    images[i].save(file_path)
    print(file_path)