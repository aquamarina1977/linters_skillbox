import os
from PIL import Image, ImageFilter

def blur_image(src_filename, dst_filename):
    src_path = os.path.join("uploads", src_filename)
    dst_path = os.path.join("uploads", dst_filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"File {src_path} not found.")

    with Image.open(src_path) as img:
        blurred_img = img.filter(ImageFilter.GaussianBlur(5))
        blurred_img.save(dst_path)
        print(f"Saved blurred image as {dst_path}")


