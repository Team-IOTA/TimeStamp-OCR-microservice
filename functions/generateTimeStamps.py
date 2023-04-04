import json
import time
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ResponseData():
    def __init__(self, topic: str, timestamp: str, image: str):
        self.topic = topic
        self.timestamp = timestamp
        self.image = image
    def to_dict(self):
        return {'topic': self.topic, 'timestamp': self.timestamp, 'image': self.image}
    
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class TimeStamp :

    def encoder_response(response):
        if isinstance(response,ResponseData):
            return {'topic': response.topic, 'timestamp': response.timestamp, 'image': response.image}
        

    def generateTimeStamp(videoPath):

        responses = []
        jsonresponses = []

        #video_file = r"C:\Users\Ridma Premaratne\Desktop\SDGP\testvid.mp4"
        video_file = r'%s' % videoPath
        unique_frames_dir = r"C:\Users\Ridma Premaratne\Desktop\SDGP\timestampOCR\data"

        cap = cv2.VideoCapture(video_file)
        ret, prev_frame = cap.read()
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_num = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to grayscale for faster processing
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

            # Compute the absolute difference between the two frames
            diff = cv2.absdiff(frame_gray, prev_frame_gray)
            diff_mean = diff.mean()

            # If the difference is significant, save the current frame
            if diff_mean > 10:
                #filename = f'frame_{frame_num}.jpg'
                thresh = cv2.threshold(frame_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                text = pytesseract.image_to_string(thresh)
                # Use Tesseract to detect text regions in the image
                boxes = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

                # Identify the text regions that are located at the top of the image
                top_boxes = []
                for i in range(len(boxes['text'])):
                    if boxes['conf'][i] > 90 and boxes['top'][i] < thresh.shape[0] // 4 and boxes['height'][i] > 20:
                        top_boxes.append(boxes['text'][i])

                # Extract the text from the identified top text region
                top_text = ' '.join(top_boxes)

                # Print the top text
                #print('Top Text:', top_text)

                timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
                filename = f'frame_{frame_num}_{time.strftime("%H%M%S", time.gmtime(timestamp / 1000))}.jpg'
                cv2.imwrite(unique_frames_dir + '/' + filename, frame)

                obj = {"topic":top_text,"timestamp":time.strftime("%H:%M:%S", time.gmtime(timestamp / 1000)) , "image":"C:\\Users\\Ridma Premaratne\\Desktop\SDGP\\timestampOCR\\data" + "\\" + filename}
               
                responses.append(obj)
               
                #print(text,"\n")

            # Set the current frame as the previous frame for the next iteration
            prev_frame = frame.copy()
            frame_num += 1

        cap.release()    
        return responses
