from flask import Flask, render_template, Response
from blaze import generate_frame

app = Flask(__name__, template_folder='webapp')

@app.route('/')
def index():
    return render_template('index.html')

# Function to generate video frames
def generate():
    for frame_base64, is_correct_horse_stance in generate_frame():
        # Yield each frame as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_base64.encode() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Return the response with video frames
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)