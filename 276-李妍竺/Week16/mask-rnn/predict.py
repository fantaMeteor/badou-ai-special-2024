from PIL import Image
from mask_rcnn import MASK_RCNN

mask_rcnn = MASK_RCNN()

while True:
    try:
        image = Image.open('img/street.jpg')
    except:
        print('Open Error! Try again!')
        continue
    else:
        mask_rcnn.detect_image(image)


mask_rcnn.close_session()