import cv2
import numpy as np
from PIL import Image
import streamlit as st
#from streamlit_image_comparison import image_comparison as img_compare

# Set page title and favicon.
st.set_page_config(
    page_title="Magical Image Art", page_icon='🌟',
)

st.write('## Magical Art Effects on Image using OpenCV 🧙‍♂️✨')
with st.sidebar:
    bg = Image.open('bg_show.png')
    st.image(bg, width=327)

"""
[![Star](https://img.shields.io/github/stars/ShruAgarwal/Magical_Image_Art.svg?logo=github&style=social)](https://github.com/ShruAgarwal/Magical_Image_Art)
[![Follow](https://img.shields.io/twitter/follow/Shru_explores?style=social)](https://www.twitter.com/Shru_explores)
"""

with st.expander("⭐ HIGHLIGHTS OF THE APP"):
    st.write("""This app can convert & apply three different effects on an Image,
             i.e, `pop/dotted art`, `water color art` & `cartoon style art`.
             \nAll the above effects are given using two python libraries -- *OPENCV & NUMPY* 🤯
             \n 👈 *Sidebar (in left) is an illustration of effects applied onto images*
             \nHope you'll like it! 🙌

                 """)



def upload_img():
    uploaded = st.file_uploader("UPLOAD AN IMAGE")
    if uploaded is not None:
         display = Image.open(uploaded)
         st.write('### Original Image')
         st.image(display)
         
         return display
    #else:
        #st.write('Please')
#########################################################################
# FUNCTIONS FOR APPLYING VARIETY OF EFFECTS
def pop_art(original):
   
  try:
        original = np.array(original)
   
        # import the image as greyscale
        image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

        # set colours (BGR)
        background_colour = [247,19,217] 
        dots_colour = (13, 10, 52) 

        # set the max dots (on the longest side of the image)
        max_dots = 180
    
        # extract dimensions
        image_height, image_width = image.shape

        # down size to number of dots
        if image_height == max(image_height,image_width):
            downsized_image = cv2.resize(image,(int(image_height*(max_dots/image_width)),max_dots))
        else:
            downsized_image = cv2.resize(image,(max_dots,int(image_height*(max_dots/image_width))))

        # extract dimensions of new image
        downsized_image_height, downsized_image_width = downsized_image.shape

        # final image size
        multiplier = 30

        # set the size of our blank canvas
        blank_img_height = downsized_image_height * multiplier
        blank_img_width = downsized_image_width * multiplier

        # set the padding value so the dots start in frame (rather than being off the edge)
        padding = int(multiplier/2)

        # create canvas containing just the background colour
        blank_img = np.full(((blank_img_height),(blank_img_width),3), background_colour,dtype=np.uint8)

        # run through each pixel and draw the circle on our blank canvas
        for y in range(0,downsized_image_height):
            for x in range(0,downsized_image_width):
                cv2.circle(blank_img,(((x*multiplier)+padding),((y*multiplier)+padding)), int((0.6 * multiplier) * ((255-downsized_image[y][x])/255)), dots_colour, -1)
    
    except cv2.error as error:
        st.warning("[Error]: {}".format(error))
    else:
        return st.image(blank_img)

########################################################################
def cartoon_style(original):
    try:
        image_1 = np.array(original)

        # Convert the input image to gray scale
        gray = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)

        # Perform adaptive threshold
        edges  = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 8)

        # Smooth the result
        blurred = cv2.medianBlur(image_1, 3)

        # Combine the result and edges to get final cartoon effect
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    
    except cv2.error as error:
        st.warning("[Error]: {}".format(error))
    else: 
        return st.image(cartoon)

#######################################################################
def waterColor_style(original):
    try:
        image_2 = np.array(original)
     
        # Resize the image
        image_resized = cv2.resize(image_2, None, fx=0.5, fy=0.5)

        # Clearing the impurities
        image_cleared = cv2.medianBlur(image_resized, 3)
        image_cleared = cv2.medianBlur(image_cleared, 3)
        image_cleared = cv2.medianBlur(image_cleared, 3)
        image_cleared = cv2.edgePreservingFilter(image_cleared, sigma_s=6)

        # Bilateral Image filtering
        image_filtered = cv2.bilateralFilter(image_cleared, 3, 10, 5)

        for i in range(2):
            image_filtered = cv2.bilateralFilter(image_filtered, 3, 20, 10)

        for i in range(3):
            image_filtered = cv2.bilateralFilter(image_filtered, 5, 30, 10)

        # Final part -- Sharpening the image
        gaussian_mask = cv2.GaussianBlur(image_filtered, (7,7), 2)
        image_sharp = cv2.addWeighted(image_filtered, 1.5, gaussian_mask, -0.5, 0)
        image_sharp = cv2.addWeighted(image_sharp, 1.4, gaussian_mask, -0.2, 10)
        #image_sharp = Image.fromarray(image_sharp)

    except cv2.error as error:
        st.warning("[Error]: {}".format(error))
    else:
        return st.image(image_sharp)

##################################################################################
# DISPLAYING RESULTS!
display_image = upload_img()

if st.button('See the Magic! 🎉'):
    tab1, tab2, tab3 = st.tabs(["CARTOON 😲", "POP ART 👀", "WATERCOLOR 🎨"])
    with tab1:
        st.write('### CARTOON STYLED IMAGE')
        cartoon_style(display_image)
        
    with tab2:
        st.write('### POP ART IMAGE')
        pop_art(display_image)
        
    with tab3:
        st.write('### WATERCOLOR STYLED IMAGE')
        waterColor_style(display_image)
        
        
