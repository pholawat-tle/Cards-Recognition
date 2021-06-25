import cv2
import torch
from PIL import Image

# Model
model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')
model.conf = 0.8

while True:
    path = input("Enter the path to image: ")

    if path == 'q':
        break  # Quit the program

    img = Image.open(path)  # Open Image with PIL

    width, height = img.size  # Image Size

    # Inference
    results = model(img)  # includes NMS

    df = results.pandas().xyxy[0].drop_duplicates(subset=['name'])

    visibleCards = []
    for card in df['name']:
        visibleCards.append(card)
    print('The visible cards are ' + str(visibleCards))
