# Importing required libraries, obviously
import streamlit as st
from PIL import Image
import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join

def Predict(image):
    net = cv2.dnn.readNetFromDarknet("yolov3_custom.cfg",r"yolov3_custom_last.weights")
    classes = ['Without Helmet', 'With Helmet']

    img = np.array(image.convert('RGB'))
    img = cv2.resize(img,(1280,720))
    hight,width,_ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255,(416,416),(0,0,0),swapRB = True,crop= False)

    net.setInput(blob)

    output_layers_name = net.getUnconnectedOutLayersNames()

    layerOutputs = net.forward(output_layers_name)

    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.6:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)


    indexes = cv2.dnn.NMSBoxes(boxes,confidences,.5,.4)

    boxes =[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * hight)
                w = int(detection[2] * width)
                h = int(detection[3]* hight)

                x = int(center_x - w/2)
                y = int(center_y - h/2)



                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,.8,.4)
    font = cv2.FONT_HERSHEY_PLAIN
    #colors = np.random.uniform(0,255,size =(len(boxes),3))
    if  len(indexes)>0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = [0,255,0]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img,label + " " + confidence, (x,y),font,2,color,2)
    return img, len(indexes)


def about():
    st.markdown("[Click here to see my resume](https://pratik-98.github.io/CV/)")
    logo = Image.open('logo/logo2.png')
    st.image(logo, width=200)


def main():
    st.header("Helmet Detection")

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("MENU", activities)
    st.sidebar.image("logo/logo1.jpg", use_column_width=True)

    if choice == "Home":
        # You can specify more file types below if you want
        image_file = st.file_uploader("Upload an image", type=['jpeg', 'png', 'jpg', 'webp'])

        if image_file is not None:
            image = Image.open(image_file)

            if st.button("Let's Predict"):
                result_img, total_detections = Predict(image)
                st.image(result_img, use_column_width = True)
                st.success("Wow... we got {} detections\n".format(total_detections))
        st.write("Go to the About section from the sidebar to contact me!")

    elif choice == "About":
        about()


if __name__ == "__main__":
    main()
