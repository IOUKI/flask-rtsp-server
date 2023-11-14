from flask import Flask, render_template, Response
import cv2
import threading

app = Flask(__name__)

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture('rtsp://user:js1111111@10.13.10.3:7001/000F7C175E88')
        self.lock = threading.Lock()

    def getFrame(self):
        success, frame = self.camera.read()
        if not success:
            return None
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def release(self):
        self.camera.release()

cam = Camera()

def genFrames():
    while True:
        with cam.lock:
            frame = cam.getFrame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/videoStart')
def videoStart():
    return Response(genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
