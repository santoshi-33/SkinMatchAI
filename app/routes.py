from flask import Blueprint, render_template, request
import os
import cv2
from .utils import get_recommendations, analyze_skin_type  # new function
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('app/static/uploads', filename)
            image.save(image_path)

            # OpenCV processing to determine skin type
            full_image_path = os.path.abspath(image_path)
            skin_type = analyze_skin_type(full_image_path)  # NEW LOGIC

            # Get product recommendations
            recommendations = get_recommendations(skin_type)

            return render_template('results.html',
                                   image_path=image_path,
                                   recommendations=recommendations,
                                   skin_type=skin_type)

    return render_template('index.html')
