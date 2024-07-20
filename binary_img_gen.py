from PIL import Image
import cv2
import numpy as np

count = 0

while True:
    image_path = 'scanned_plates\scanned_img_0.jpg'
    image = Image.open(image_path)

    threshold = 128
    binary_image = image.point(lambda p: p > threshold and 255)
    # binary_image = np.array(binary_image)

    # new_width = binary_image.shape[1] // 5
    # new_height = binary_image.shape[0] // 5
    # binary_image = cv2.resize(binary_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    # binary_image = Image.fromarray(binary_image)


    binary_image.save('./binary_images/binary_image_1')
    binary_image.show()
    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break