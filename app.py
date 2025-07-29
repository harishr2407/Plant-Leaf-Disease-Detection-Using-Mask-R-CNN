from flask import Flask, request, render_template, redirect, url_for
import cv2
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

def extract_diseased_part(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([10, 50, 50])
    upper_bound = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    diseased_part = cv2.bitwise_and(image, image, mask=mask)
    return diseased_part

def preprocess_images(folder_paths, max_images_per_folder=20):
    orb = cv2.ORB_create()
    image_data = []

    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            continue

        folder_name = os.path.basename(folder_path)
        images_checked = 0

        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                image = cv2.imread(image_path)

                if image is None:
                    continue

                diseased_part = extract_diseased_part(image)
                diseased_gray = cv2.cvtColor(diseased_part, cv2.COLOR_BGR2GRAY)
                keypoints, descriptors = orb.detectAndCompute(diseased_gray, None)

                if descriptors is None:
                    continue

                image_data.append((folder_name, descriptors))
                images_checked += 1

                if images_checked >= max_images_per_folder:
                    break

    return image_data

def match_descriptors(target_descriptors, image_data):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    folder_match_counts = {}

    for folder_name, descriptors in image_data:
        matches = bf.match(target_descriptors, descriptors)
        match_count = len(matches)

        if folder_name not in folder_match_counts:
            folder_match_counts[folder_name] = 0
        folder_match_counts[folder_name] += match_count

    return folder_match_counts

def check_leaf_marks(target_image_path, image_data):
    target_image = cv2.imread(target_image_path)
    if target_image is None:
        return "Error: Target image not found."

    target_diseased_part = extract_diseased_part(target_image)
    target_diseased_gray = cv2.cvtColor(target_diseased_part, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(target_diseased_gray, None)

    if descriptors is None:
        return "Error: Unable to compute descriptors for target image."

    folder_match_counts = match_descriptors(descriptors, image_data)

    if not folder_match_counts:
        return "No match found in any folder."

    max_match_count = max(folder_match_counts.values())
    matching_folders = [folder for folder, count in folder_match_counts.items() if count == max_match_count]

    if matching_folders:
        return f"Target image matches leaf marks(s): {', '.join(matching_folders)}"
    else:
        return "No match found in any folder."

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            result = check_leaf_marks(file_path, image_data)
            result_image = 'uploads/' + file.filename  # Adjust as per your file storage configuration

            return render_template('result.html', result=result, result_image=result_image)
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/cereal')
def cereal():
    return render_template('cereal.html')
@app.route('/oil')
def oil():
    return render_template('oil.html')
@app.route('/fiber')
def fiber():
    return render_template('fiber.html')
@app.route('/fruit')
def fruit():
    return render_template('fruit.html')
@app.route('/veg')
def veg():
    return render_template('veg.html')
@app.route('/flower')
def flower():
    return render_template('flower.html')
@app.route('/root')
def root():
    return render_template('root.html')

@app.route('/pulse')
def pulse():
    return render_template('pulse.html')

if __name__ == '__main__':
    folder_paths = [
        r'C:/Users/anjan/leaf_disease_detection/database/Train/Healthy',
        r'C:/Users/anjan/leaf_disease_detection/database/Train/Powdery',
        r'C:/Users/anjan/leaf_disease_detection/database/Train/Rust'
    ]

    with ThreadPoolExecutor() as executor:
        image_data = executor.submit(preprocess_images, folder_paths).result()

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
