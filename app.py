#!C:\Users\chpark\Anaconda3\envs\yolo\python.exe

# Flask utils
import os.path
from flask import Flask, redirect, url_for, request, render_template, Response
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from werkzeug.wrappers import response
from camera import ObjectDetection
from playsound import playsound

import win32com.client as wincl       #### Python's Text-to-speech (tts) engine for windows, multiprocessing
speak = wincl.Dispatch("SAPI.SpVoice")    #### This initiates the tts engine

app = Flask(__name__)
@app.route("/")
def main():
    return render_template("index.html")

def gen(camera):
    while True:
        frame = camera.main()
        if frame != "":
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    id = "http://192.168.0.11:8080/video"
    # id = 0
    return Response(gen(ObjectDetection(id)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/read_txt')
def read_txt():
    if os.path.isfile('feedback.txt'):
        while True:
            f = open('feedback.txt', 'r')
            return "</br>".join(f.readlines())
    else :
        print("감지된 대상이 없습니다.")
    
        

@app.route('/voice_feedback')
def voice_feedback():
    if os.path.isfile('feedback_gtts_v2.mp3'):
        playsound('feedback_gtts_v2.mp3')
    else :
        print("감지된 대상이 없습니다.")


if __name__ == '__main__':
    # Serve the app with gevent
    app.run(host='192.168.0.7', port=9900, threaded=True, debug = True)
