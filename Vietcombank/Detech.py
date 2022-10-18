import cv2 
import pytesseract

img = cv2.imread('D:\Working\Octa\Readbankapp\z3347868787168_7683901ae19575eedd42b2a1b3d0c849.jpg')

# Adding custom options
custom_config = r'--oem 3 --psm 6'
print(pytesseract.image_to_string(img, config=custom_config))