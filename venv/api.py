import time
from flask import Flask, request, redirect
import cv2
import imutils
from PIL import Image
import requests
import os


def _calculate_size(file,WIDTH_PIXEL_A4, HEIGHT_PIXEL_A4):
    """
    This function calculate the ratio
    between the size of A4 paper and 
    the image (file) provided. The ratio is
    a percentaje.
    Parameters
    ----------
    file : String, name of image
    WIDTH_PIXEL_A4 and HEIGHT_PIXEL_A4 (796 x 1123 pixeles)
        
    Returns:
        height ratio and weight ratio
    -------
    """

    image=cv2.imread(file)
    imge_info_shape = image.shape
    height = imge_info_shape[0]
    Width = imge_info_shape[1]
    
    #Orientiation verification    
    if Width > height:
        horizontal = True
        height_per_to_A4 = round((height/WIDTH_PIXEL_A4)*100,2)
        Width_per_to_A4 = round((Width/HEIGHT_PIXEL_A4)*100,2)
    else:
        horizontal = False   
        height_per_to_A4 = round((height/HEIGHT_PIXEL_A4)*100,2)
        Width_per_to_A4 = round((Width/WIDTH_PIXEL_A4)*100,2)

    return height_per_to_A4, Width_per_to_A4, image, horizontal


def _re_size_image(ratio_height, ratio_width, image, 
                   WIDTH_PIXEL_A4, HEIGHT_PIXEL_A4, 
                   horizontal):
    """
    This function re-size the image to
    A4 Paper
    Parameters
    ----------
    ratio_height : ratio height respect to A4 paper
    ratio_width : ratio weight respect to A4 paper
    image: Original file read in function _calculate_size
    WIDTH_PIXEL_A4 and HEIGHT_PIXEL_A4 (796 x 1123 pixeles)
    horizontal: True/False --> Is the image orientation
    
    NOTE: If horizontal is True, WIDTH_PIXEL_A4 = HEIGHT_PIXEL_A4
          and HEIGHT_PIXEL_A4 = WIDTH_PIXEL_A4.
          This is used for orientation A4 paper purposes
          and the new re-sized image
        
    Returns:
        re-sized image to A4 paper    
    """
    ratio = 100
    if horizontal == False:
    
        if (ratio_height <= ratio 
            and  ratio_width <=ratio):
            
            return image
        
        elif (ratio_height <= ratio 
            and  ratio_width >ratio):
            
            return imutils.resize(image, width=WIDTH_PIXEL_A4)
        
        elif (ratio_height > ratio 
            and  ratio_width <= ratio):
            
            return imutils.resize(image, height=HEIGHT_PIXEL_A4)    
        
        elif (ratio_height > ratio 
            and  ratio_width > ratio):
            
            img_new_1 = imutils.resize(image, width=WIDTH_PIXEL_A4)
            img_new_2 = imutils.resize(img_new_1, height=HEIGHT_PIXEL_A4)
            
            if img_new_2.shape[1]> WIDTH_PIXEL_A4:
                img_new_2 = imutils.resize(img_new_2, width=WIDTH_PIXEL_A4)         
            
            return img_new_2
    
        else:
            pass
    
    else:
        
        if (ratio_height <= ratio 
            and  ratio_width <=ratio):
            
            return image
        
        elif (ratio_height <= ratio 
            and  ratio_width >ratio):
            
            return imutils.resize(image, width=HEIGHT_PIXEL_A4)
        
        elif (ratio_height > ratio 
            and  ratio_width <= ratio):
            
            return imutils.resize(image, height=WIDTH_PIXEL_A4)    
        
        elif (ratio_height > ratio 
            and  ratio_width > ratio):
            
            img_new_1 = imutils.resize(image, width=HEIGHT_PIXEL_A4)
            img_new_2 = imutils.resize(img_new_1, height=WIDTH_PIXEL_A4)
            
            if img_new_2.shape[1]> WIDTH_PIXEL_A4:
                img_new_2 = imutils.resize(img_new_2, width=HEIGHT_PIXEL_A4)         
            
            return img_new_2
        
    
def _save_new_image(img, name, horizontal):
    """
    This function save de new image in the A4 paper
    
    Parameters
    ----------
    img : Obtain Original image from _calculate_size
    name : String to save the new image    
    horizontal: True/False orientantion of original image
        
    Returns:
        Save the new image re-sized in A4 Paper    
    """
    
    cv2.imwrite(name, img)
    
    if horizontal == True:
        im1 = Image.open('./paper_a4/A4_H.jpg')
    else:
        im1 = Image.open('./paper_a4/A4.jpg')
    im2 = Image.open('./resized/resized.jpg')
    im1.paste(im2)
    
    
    return im1.save('./results/final.jpg', quality=95)


def _know_diference(image_new, original_image):
    """
    This function callculate the diferene
    between the original image and new image in pixeles
    
    Parameters
    ----------
    image_new : New image without A4 paper
    original_image : Original image without re-sized    
            
    Returns:
        Dictionary with information to be used in
        re-sized image
    """
    i_new = image_new.shape
    i_original = original_image.shape
    
    diference_width = i_original[1] - i_new[1]
    diference_height = i_original[0] - i_new[0]
    
    return {"reduce_width": diference_width,
            "reduce_height": diference_height,
            "original_width": i_original[1],
            "original_height": i_original[0],
            "new_width": i_new[1],
            "new_height": i_new[0]}

def _run_main_re_size(ruta):
    """
    This function run all the functions and
    re-size the image
    """
    
    WIDTH_PIXEL_A4 = 796
    HEIGHT_PIXEL_A4 = 1123 
    

    file = ruta
    
    f1= _calculate_size(file, WIDTH_PIXEL_A4, HEIGHT_PIXEL_A4)
    f2 = _re_size_image(f1[0], f1[1], f1[2], WIDTH_PIXEL_A4, HEIGHT_PIXEL_A4, f1[3])
    f3 = _know_diference(image_new = f2, original_image = f1[2])
    print("Reducir ancho",f3["reduce_width"],"original-->",
          f3["original_width"], "Nuevo-->", f3["new_width"])
    
    print("Reducir alto",f3["reduce_height"], "original-->",
          f3["original_height"], "Nuevo-->", f3["new_height"])   
    
    _save_new_image(f2, "./resized/resized.jpg",f1[3])  

    os.startfile(os.getcwd()+os.sep+"results\\final.jpg")

    return f3


app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.strftime("%Y-%m-%d")}

@app.route('/image_info',methods=("POST", "GET"))
def get_image_info():
    if request.method == "POST":
        if request.form.get('email') == None:
            email= './images/paper.jpg'
        else:
            email=request.form.get('email')
        print(email)
        info = _run_main_re_size(email)
    return ("""
            <style>
            .content {
                max-width: 500px;
                margin:0 auto;
                
                }

                    body {
                    display:flex; flex-direction:column; justify-content:center;
                    min-height:100vh;
                    background-color: #f7f7f7;
                    }
            </style>

                <!DOCTYPE html>
                    <html>
                    <body class="content">

                    <h1 style="background-color:powderblue;">Información de imagen seleccionada</h1>
                    <h2>El nuevo tamaño de la imagen debera ser:</h2>
                        Ancho: wigth  pixeles<br></br><br></br>
                        Alto:  height  pixeles<br></br><br></br>

                    <h2>Al tamaño original se le debe restar:</h2>
                        Ancho: anchh_1  pixeles<br></br><br></br>
                        Alto:  allt_1  pixeles<br></br><br></br>
                    
                    <h2>El tamaño original es:</h2>
                        Ancho: origi_1  pixeles<br></br><br></br>
                        Alto:  ori_2  pixeles<br></br><br></br>                          
                    </body>
                </html>     
    """).replace("wigth",str(info['new_width'])).replace('height',str(info['new_height']))\
        .replace("anchh_1",str(info['reduce_width'])).replace('allt_1',str(info['reduce_height']))\
        .replace("origi_1",str(info['original_width'])).replace('ori_2',str(info['original_height']))

email=''
@app.route('/signup', methods = ['POST'])
def signup():   
    email = request.form.get('email')
    print("The email address is '" + email + "'")
    return email

