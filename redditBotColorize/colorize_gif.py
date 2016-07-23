import sys
import cv2
import colorize
import os

colorize.loadDNN(False)

gif_path = sys.argv[1]

cam = cv2.VideoCapture(gif_path)

counter = 0
while True:
    ret,img = cam.read()
    if not ret:
        break
    temp_img_path = '/tmp/%06d.jpg'%counter
    cv2.imwrite(temp_img_path,img)
    coloredImage = colorize.runDNN(temp_img_path)
    cv2.imwrite(temp_img_path,coloredImage)
    counter += 1

os.system('ffmpeg -i /tmp/\%06d.jpg colorized_%s'%gif_path)

