import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def compress_image(image, max_width=1200, quality=80):
    """
    Compresses and resizes an image using PIL/Pillow.
    Returns a Django ContentFile that can be saved directly into an ImageField.
    """
    if not image:
        return None
        
    img = Image.open(image)
    
    # Convert RGBA to RGB (to allow JPEG saving)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        # Create a white background for transparent images
        background = Image.new('RGB', img.size, (255, 255, 255))
        try:
            background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        except IndexError:
            # Fallback if transparency mask doesn't align
            background.paste(img)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Resize image if it exceeds max width
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
    # Compress and save to buffer
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=quality, optimize=True)
    img_io.seek(0)
    
    # Get original filename and change extension to .jpg
    original_name = os.path.basename(image.name)
    name_without_ext, _ = os.path.splitext(original_name)
    new_filename = f"{name_without_ext}.jpg"
    
    return ContentFile(img_io.read(), name=new_filename)
