import random
import string
import numpy as np
from PIL import Image, ImageDraw
from django.core.files.images import get_image_dimensions

def generar_contraseña(size=6 , chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def recizing(path):
    img=Image.open(path)
    width, height = get_image_dimensions(img)
    #if img.height > 300 or img.width > 300:
    newsize = (300, 300)
    result= img.resize(newsize)
    result.save(path)
    return result

def cropping(path):
    
    result=recizing(path)
    img=result.convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    final=Image.fromarray(npImage)
    Image.fromarray(npImage).save(path)

    return final
