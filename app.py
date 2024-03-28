import streamlit as st
import cv2
import os
import shutil

def eliminate_bad_photos(directory, min_quality=80):
    total_images = 0
    good_images = []

    if directory.lower().endswith(('.png', '.jpg', '.jpeg', '.zip', '.rar', '.7z')):
        directory = os.path.dirname(directory)

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(directory, filename)
            img = cv2.imread(img_path)
            total_images += 1

            if img is not None:
                quality = cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()

                if quality > min_quality:
                    good_images.append((filename, quality))

    return good_images

def download_best_photos(directory, good_images):
    best_photos_dir = os.path.join(directory, 'best_photos')
    if not os.path.exists(best_photos_dir):
        os.makedirs(best_photos_dir)

    for name, quality in good_images:
        src = os.path.join(directory, name)
        dst = os.path.join(best_photos_dir, name)
        shutil.copy(src, dst)

# Add a background color and some padding
st.title("Image Processing Tool")

directory = st.text_input('Enter the directory link or select a photo/compressed file to search for images: ')
min_quality = st.slider('Minimum Quality', min_value=0, max_value=100, value=80)

if st.button('Process Images'):
    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]

    if os.path.isfile(directory):
        directory = os.path.dirname(directory)

    good_images = eliminate_bad_photos(directory, min_quality)
    download_best_photos(directory, good_images)
    st.write(f'Best photos saved in "{os.path.join(directory, "best_photos")}"')
