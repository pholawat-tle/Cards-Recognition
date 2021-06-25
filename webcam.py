import cv2
import torch

# Model
model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')
model.conf = 0.8

# Webcam
capture = cv2.VideoCapture(0)

if capture.isOpened() == False:
    print("Error: Video source not found")

while capture.isOpened():
    ret, img = capture.read()  # Read frame from source

    if ret:
        cv2.imshow("Video Feed", img)  # Display video to the screen

        h, w, c = img.shape
        print(h, w, c)

        if cv2.waitKey(25) & 0xFF == ord('q'):  # Exit if 'q' is pressed
            break

        # Inference

        results = model(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), size=max(h, w))
        # Convert the captured frame into RGB and feed it into the model

        # Result
        df = results.pandas().xyxy[0]  # img1 predictions (pandas)

        for card in df['name']:
            print(card)
            results.save()

    else:
        break  # Exit if there is no frame to be read

capture.release()

cv2.destroyAllWindows()
