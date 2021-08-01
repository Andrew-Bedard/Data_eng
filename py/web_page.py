from flask import Flask, render_template
import os

BANNER_FOLDER = os.path.join('static', 'banner_images', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = BANNER_FOLDER

# Landing page
@app.route("/")
@app.route('/index')
def show_index():
    imageList = os.listdir('static/banner_images/images')
    imageList = ['banner_images/images/' + image for image in imageList]
    imageList = imageList[0:5]
    return render_template("index.html", imageList=imageList)

if __name__ == "__main__":
    app.run()


