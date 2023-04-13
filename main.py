from kivy.lang import Builder
from kivymd.uix.button.button import MDFloatingActionButton, MDFlatButton
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from kivymd.theming_dynamic_text import get_contrast_text_color
Window.size = (400,500)
import cv2
import time
import datetime
KV = '''
MDScreen:
    
    MDLabel:
        text: "Welcome to Smilecapture"
        font_style: 'H6'
        align: "center"
        pos_hint: {"center_x": .7, "center_y": .4}
    
    
    MDRectangleFlatIconButton:
        text: "How it's work"
        font_style: 'Button'
        icon: "tools"
        line_color: 1, 2, 3, 1
        pos_hint: {"center_x": .2, "center_y": .1}
        on_release: app.show_alert_dialog()
    
    MDFloatingActionButton:
        icon: "camera"
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"center_x": .8, "center_y": .2}
        on_press: app.smile()


    FitImage:
        source: "final.jpeg"
        size_hint_y: .5
        pos_hint: {"top":1}
        radius: 20,20,20,20
        
        '''


class Example(MDApp):
    dialog = None
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)


    def smile(self):
        # rectangle over the faces
        blue = (255, 0, 0)

        # start capturing the video from the cam
        video_capture = cv2.VideoCapture(0)

        # load the haar cascades face and smile detectors
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        smile_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

        # loop over the frames
        while True:
            # get the next frame from the video and convert it to grayscale
            _, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # apply our face detector to the grayscale frame
            faces = face_detector.detectMultiScale(gray, 1.1, 8)

            # let's assume the number of images gotten is 0

            # go through the face bounding boxes
            for (x, y, w, h) in faces:
                k = cv2.waitKey(1)
                # if the escape key has been pressed, the app will stop
                if k % 256 == 27:
                    print('escape hit, closing the app')
                    video_capture.release()
                    break
                # get the region of the face
                roi = gray[y:y + h, x:x + w]
                # apply our smile detector to the region of the face
                smile_rect, rejectLevels, levelWeights = smile_detector.detectMultiScale3(roi, 2.5, 20, outputRejectLevels=True)

                # weaker detections are classified as "Not Smiling" that we decide will be detection under 2
                # while stronger detection are classified as "Smiling" detection above 2
                if len(levelWeights) == 0:
                    cv2.putText(frame, "Not Smiling", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, blue, 3)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), blue, 2)
                else:
                    if max(levelWeights) < 2:
                        cv2.putText(frame, "Not Smiling", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, blue, 3)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), blue, 2)
                    else:
                        # name the image as the date and time at which it was taken
                        dt = str(datetime.datetime.now())
                        # change the invalid character in the image name
                        dt = dt.replace("-", "_")
                        dt = dt.replace(":", "_")
                        dt = dt.replace(".", "_")
                        # saves the image as a png file
                        img_name = 'smile pic_' + str(dt) + '.jpg'
                        time.sleep(0.25)
                        cv2.imwrite(img_name, frame)
                        print('screenshot taken')
            #    show the video
            cv2.imshow('Frame', frame)

        # close all windows
        cv2.destroyAllWindows()


    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="press the camera icon to open the camera, then a picture wil be taken whenever you smile.\nin order to exit press esc. ",
                buttons=[
                    MDFlatButton(
                        text="Return",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.dialog.dismiss()

                    ),
                ],
            )
        self.dialog.open()





Example().run()
