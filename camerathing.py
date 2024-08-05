import PySimpleGUI as sg
import cv2
import numpy as np

def main():
    sg.theme("DarkBrown")
    
    col1 = [
        [sg.Radio("None", "Radio", True, size=(10, 1))],
        [
            sg.Radio("pencil", "Radio", size=(10, 1), key="-PENCIL-"),
            sg.Radio("pencil(grayscale)", "Radio", size=(10, 1), key="-PENCIL GRAYSCALE-"),
            sg.Slider(
                (0.0, 100.0),
                60,
                1,
                orientation="h",
                size=(20, 15),
                key="-PENCIL SLIDER A-",
            ),
            sg.Slider(
                (0.0, 0.1),
                0.07,
                0.01,
                orientation="h",
                size=(20, 15),
                key="-PENCIL SLIDER B-",
            ),
            sg.Slider(
                (0.0, 0.1),
                0.05,
                0.01,
                orientation="h",
                size=(20, 15),
                key="-PENCIL SLIDER C-",
            )
         ],
        [
            sg.Radio("threshold", "Radio", size=(10, 1), key="-THRESH-"),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER-",
            ),
        ],
        [
            sg.Radio("canny", "Radio", size=(10, 1), key="-CANNY-"),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(20, 15),
                key="-CANNY SLIDER A-",
            ),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(20, 15),
                key="-CANNY SLIDER B-",
            ),
        ],       
    ]
    
    
    col2 = [
           [
            sg.Radio("blur", "Radio", size=(10, 1), key="-BLUR-"),
            sg.Slider(
                (1, 11),
                1,
                1,
                orientation="h",
                size=(40, 15),
                key="-BLUR SLIDER-",
            ),
        ],
        [
            sg.Radio("hue", "Radio", size=(10, 1), key="-HUE-"),
            sg.Slider(
                (0, 225),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-HUE SLIDER-",
            ),
        ],
        [
            sg.Radio("enhance", "Radio", size=(10, 1), key="-ENHANCE-"),
            sg.Slider(
                (1, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-ENHANCE SLIDER-",
            ),
        ],
        [sg.Button("Exit", size=(10, 1))],
        [sg.Button("Take Picture", size=(10,1))]
    ]
    # Define the window layout
    layout = [
        [sg.Text("OpenCV Demo", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
        [sg.Column(col1), sg.Column(col2)],
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(300, 200), resizable=True)

    cap = cv2.VideoCapture(0)
    
    img_counter = 0
    
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        if event == "Take Picture":
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            img_counter += 1
        
        ret, frame = cap.read()

        if values["-PENCIL-"]:
            frame2, frame = cv2.pencilSketch(frame, 
                                             sigma_s=values["-PENCIL SLIDER A-"], 
                                             sigma_r=values["-PENCIL SLIDER B-"], 
                                             shade_factor=values["-PENCIL SLIDER C-"])
        if values["-PENCIL GRAYSCALE-"]:
            frame, frame2 = cv2.pencilSketch(frame, 
                                             sigma_s=values["-PENCIL SLIDER A-"], 
                                             sigma_r=values["-PENCIL SLIDER B-"], 
                                             shade_factor=values["-PENCIL SLIDER C-"])
                    
        if values["-THRESH-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            frame = cv2.threshold(
                frame, values["-THRESH SLIDER-"], 255, cv2.THRESH_BINARY
            )[1]
            
        elif values["-CANNY-"]:
            frame = cv2.Canny(
                frame, values["-CANNY SLIDER A-"], values["-CANNY SLIDER B-"]
            )
        elif values["-BLUR-"]:
            frame = cv2.GaussianBlur(frame, (21, 21), values["-BLUR SLIDER-"])
        elif values["-HUE-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += int(values["-HUE SLIDER-"])
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        elif values["-ENHANCE-"]:
            enh_val = values["-ENHANCE SLIDER-"] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()

main()