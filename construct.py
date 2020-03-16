import cv2
from tkinter import *
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
from time import time, sleep
from ffpyplayer.player import MediaPlayer
import smtplib, os, pickle
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import json

with open("info.json", encoding='UTF8') as json_file:
     json_info = json.load(json_file)


video_path=json_info["video_path"]
email = json_info["myInfo"]["mail"]  # google mail
pw = json_info["myInfo"]["pw"]  # google app password required


# check student info
def exist_student(class_id, std_id, name):
    if (class_id not in json_info.keys()) or \
            (std_id not in json_info[class_id].keys()) or \
            (name != json_info[class_id][std_id]):
        return False
    else:
        return True


# SMTP type
def mailing(std_class, std_id, name, play_time):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, pw)

    msg = MIMEMultipart()
    msg['Subject'] = std_class + '_' + std_id + '_' + name + '_' + str(play_time)
    part = MIMEText(std_class + '_' + std_id + '_' + name + '_' + str(play_time))
    msg.attach(part)

    msg["To"] = email
    smtp.sendmail(email, email, msg.as_string())
    smtp.quit()


class VideoPlayer(Tk):
    def __init__(self, video_source=None):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(EntranceScene)
        self.video_source = video_source

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def end_app(self):
        self.destroy()


class EntranceScene(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        description_lbl1 = Label(self, text="created by ParkHeeChan")
        description_lbl1.pack()
        description_lbl2 = Label(self, text="hchan11@naver.com")
        description_lbl2.pack()

        class_lbl = Label(self, text="분반 (월/화/목오전/목오후)")  # class
        class_lbl.pack()
        class_txt = Entry(self)
        class_txt.pack()

        std_id_lbl = Label(self, text="학번(std_id)")  # student ID
        std_id_lbl.pack()
        std_id_txt = Entry(self)
        std_id_txt.pack()

        name_lbl = Label(self, text="이름(name)")  # student name
        name_lbl.pack()

        name_txt = Entry(self)
        name_txt.pack()

        def entrance_btn():
            class_id = class_txt.get()
            std_id = std_id_txt.get()
            name = name_txt.get()

            self.master.class_id = class_id
            self.master.std_id = std_id
            self.master.name = name

            if exist_student(class_id, std_id, name) is True:
                messagebox.showinfo("info", f"{std_id}_ {name}")
                master.switch_frame(PlayerScene)
            else:
                messagebox.showinfo("Error", "분반, 학번, 이름을 확인하세요.")

        entrance_btn = Button(self, text="확인", command=entrance_btn)
        entrance_btn.pack()


class PlayerScene(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        description_lbl1 = Label(self, text="동영상이 끝나고 확인 메세지가 나와야 출석 체크 됩니다.")
        description_lbl1.pack()

        def destroy_btn():
            messagebox.showinfo("info", "종료합니다.")
            master.destroy()

        def play_btn():
            try:
                cap = cv2.VideoCapture(self.master.video_source)

                sound_player = MediaPlayer(self.master.video_source)
            except:
                ValueError
                return 0

            start_time = time()

            fps = cap.get(cv2.CAP_PROP_FPS)
            delay = round(1000 / fps)
            cap.set(cv2.CAP_PROP_FPS, round(fps))

            ret = False
            while(cap.isOpened()):
                ret, frame = cap.read()
                audio_frame, val = sound_player.get_frame()

                if ret:
                    cv2.imshow('FPGA Player', frame)

                    if cv2.waitKey(delay-4) & 0xFF == ord('q'):  # fps - 4 frame will be sync with audio
                        break
                    if val != 'eof' and audio_frame is not None:
                        img, t = audio_frame
                else:
                    break

            cap.release()
            messagebox.showinfo("info", "학습이 끝났습니다.")
            cv2.destroyAllWindows()

            end_time = time()
            play_time = start_time - end_time  # play time check
            mailing(self.master.class_id, self.master.std_id, self.master.name, play_time)

        exit_lbl = Button(self, text="종료", command=destroy_btn)
        exit_lbl.pack()

        play_btn = Button(self, text="재생", command=play_btn)
        play_btn.pack()


if __name__ == "__main__":
    app = VideoPlayer(video_source=video_path)
    app.mainloop()








