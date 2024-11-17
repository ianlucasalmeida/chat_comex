from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from yt_dlp import YoutubeDL  # substitua youtube_dl por yt_dlp
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_filename = os.path.join(UPLOAD_FOLDER, 'downloaded_video.mp4')
    try:
        ydl_opts = {
            'outtmpl': output_filename,
            'format': 'mp4'
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_filename, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    output_format = request.form['format']
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)
    output_filename = os.path.splitext(file.filename)[0] + '.' + output_format
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    try:
        convert_image(input_path, output_path, output_format)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}", 500

def convert_image(input_path, output_path, output_format):
    with Image.open(input_path) as img:
        img.save(output_path, output_format.upper())

if __name__ == '__main__':
    app.run(debug=True)
