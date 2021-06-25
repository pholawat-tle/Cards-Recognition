import math
import torch
from PIL import Image

# Model
model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')
model.conf = 0.8


def findCentroid(card1):
    return [abs((card1['xmin'] + card1['xmax'])/2), abs((card1['ymin'] + card1['ymax'])/2)]


def findDistance(card1, card2):
    center1 = findCentroid(card1)
    center2 = findCentroid(card2)

    return math.sqrt((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)


def isClose(unitDistance, card1, card2):
    return findDistance(card1, card2) < unitDistance * 6


while True:
    path = input("Enter the path to image: ")

    if path == 'q':
        break  # Quit the program

    img = Image.open(path)  # Open Image with PIL

    width, height = img.size  # Image Size

    # Inference
    results = model(img)  # includes NMS

    cards = results.pandas().xyxy[0].drop_duplicates(
        subset=['name']).to_dict(orient="records")

    if(len(cards) <= 0):
        print("No card is detected")
    elif(len(cards) == 1):
        print("1 Card is detected")
    else:
        unitDistance = abs(cards[0]['xmin'] - cards[0]['xmax'])
        hands = []

        while(len(cards) != 0):
            if len(hands) == 0:
                hands.append([])
                hands[0].append(cards.pop())
            else:
                currentCard = cards.pop()
                foundHand = False
                for hand in hands:
                    for card in hand:
                        if isClose(unitDistance, currentCard, card) and foundHand == False:
                            hand.append(currentCard)
                            foundHand = True
                if not foundHand:
                    hands.append([])
                    hands[len(hands) - 1].append(currentCard)
        for hand in hands:
            str = "This hand has"
            for card in hand:
                str += " " + card['name']
            print(str)
