"""
Flask webapp to display banners
"""
import flask
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import os
from banner_logic import *
import random

BANNER_FOLDER = os.path.join('static', 'banner_images', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = BANNER_FOLDER
app.secret_key = "purplemonkeydishwasher"

csv_path = os.getcwd() + "/data/csv/csv/"

# Data quality check
dat_check(csv_path, os.getcwd() + 'log.txt')

# dataframes pre-loaded for performance
clicks_df, conv_df, imp_df = load_frames(csv_path)

# dataframe pre-merged for performance
conv_click_df = pd.merge(conv_df, clicks_df, how='outer', on='click_id')

@app.route("/campaigns/<campaign_id>/")
def show_index(campaign_id):

    # Get user ip_address for creating session identifier to prevent same banner being served twice
    # TODO: this logic is unnecessarily complex, figure out a way to unnest some of these loops
    if 'ip' in session:
        if 'prev_banners' in session:
            banner_blacklist = session['prev_banners']
            banner_list = get_banners(imp_df, conv_click_df, campaign_id, banner_blacklist)
        else:
            banner_list = get_banners(imp_df, conv_click_df, campaign_id)

    else:
        session['ip'] = request.remote_addr
        banner_list = get_banners(imp_df, conv_click_df, campaign_id)

    session['prev_banners'] = banner_list  # save session data on banners already shown
    banner_list = [str(i) for i in banner_list]  # banner list is returned as list of int right now, needs to be str

    imageList = os.listdir('static/banner_images/images')
    imageList = ['banner_images/images/' + image for image in imageList]
    imageList = [image for image in imageList if image[-7:-4] in banner_list]
    random.shuffle(imageList) # Randomly shuffle imageList order
    return render_template("index.html", imageList=imageList)


if __name__ == "__main__":
    app.run()

