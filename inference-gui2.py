import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time
import torch
from ultralytics import YOLO

class App:
    def __init__(self, window, window_title, video_source):
        # self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        self.model = YOLO('yolov8n.pt')
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.cap = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # ret, frame = self.cap.read()
        # if ret:
        #     cv2.imwrite("snapshot_"+time.strftime("%Y%m%d_%H%M%S")+".jpg", frame)
        cv2.imwrite("snapshot_"+time.strftime("%Y%m%d_%H%M%S")+".jpg", self.infer_img)

    def update(self):
        ret, frame = self.cap.read()
        if ret:
        # YOLO8 사용시 주석 해제
            results = self.model(frame)
            if results is not None:
                boxes = results[0].boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy.cpu().detach().numpy().tolist()[0]
                    width = x2 - x1
                    height = y2 - y1
                    text_x = max(int(x2)-150, 0)
                    text_y = max(int(y1)-5, 0)
                    cv2.putText(frame, f"Width: {width:.1f}, Height: {height:.1f}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            self.infer_img = self.model(frame)[0].plot()

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.infer_img, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

# 웹캠 소스로 App 클래스를 호출합니다.
App(tk.Tk(), "YOLO Object Detection", 0)
