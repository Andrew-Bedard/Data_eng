from flask import Flask, render_template
import os

BANNER_FOLDER = os.path.join('static', 'banner_images', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = BANNER_FOLDER

# Landing page
@app.route("/")
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'image_100.png')
    return render_template("index.html", user_image=full_filename)

if __name__ == "__main__":
    app.run()


