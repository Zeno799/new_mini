pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_license_plate(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Image not loaded correctly.")
        return blurred = cv2.GaussianBlur(img, (5, 5), 0)
    
    _, binary_image = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    custom_config = r'--oem 3 --psm 6'
    plate_text = pytesseract.image_to_string(binary_image, config=custom_config)

    plate_text = ''.join(e for e in plate_text if e.isalnum())
    
    print(f"Detected License Plate Text: {plate_text}")

    cv2.imshow("Original Image", img)
    cv2.imshow("Processed Image", binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return plate_text


image_path = 'test_images\binary_image_1.jpg'
