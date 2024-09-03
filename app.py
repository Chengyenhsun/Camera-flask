from flask import Flask, Response
import cv2

app = Flask(__name__)

# 定義 MJPG-Streamer 提供的 URL
url = "http://192.168.0.160:8080/?action=stream"


def generate_frames():
    # 創建 VideoCapture 物件
    cap = cv2.VideoCapture(url)

    while True:
        # 從視頻流中讀取幀
        success, frame = cap.read()
        if not success:
            break

        # 將幀轉換為灰階圖像
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 將灰階幀轉換為 JPEG 格式
        _, buffer = cv2.imencode(".jpg", gray_frame)
        frame = buffer.tobytes()

        # 生成 MJPEG 格式的幀
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
