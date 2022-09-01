import base64
import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_image_comparison import image_comparison as img_compare

# Set page title and favicon.
st.set_page_config(
    page_title="Magical Image Art", page_icon='🌟',
)

# Displaying local image with css
@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("bg_show.png")

page_bg_img = f"""
<style>

[data-testid="stSidebar"] > div:first-child {{
background: rgba(0,0,0,0);
background-image: url("data:image/png;base64,{img}");
background-size: 22% 99%;
background-position: left; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.write('## Magical Art Effects on Image using OpenCV 🧙‍♂️✨')
st.sidebar.write('')

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


uploaded = st.file_uploader("UPLOAD AN IMAGE")

if uploaded is not None:
    display_image = Image.open(uploaded)
#else:
    #st.write('')
#########################################################################
# FUNCTIONS FOR APPLYING VARIETY OF EFFECTS
def pop_art(original):
   
   original = np.array(original)
   
   # import the image as greyscale
   image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

   # set colours (BGR)
   background_colour = [247,19,217] #41, 212, 248
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
   multiplier = 35

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

   return st.image(blank_img)

########################################################################
def cartoon_style(original):
    image_1 = np.array(original)
    
    # applying effects --> sigma_s : Range between 0 to 200.
    # sigma_r : Range between 0 to 1.
    cartoon_image = cv2.stylization(image_1, sigma_s=150, sigma_r=0.25) 
    cartoon_image = Image.fromarray(cartoon_image)
    return cartoon_image

#######################################################################
def waterColor_style(original):
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

    image_sharp = Image.fromarray(image_sharp)
    return image_sharp

####################################################################################
# Render image-comparison
def image_slide(new_img):
    
    img_compare(
        img1=display_image,
        img2=new_img,
        label1="original",
        label2="new",
        width=800,
        show_labels=True,
        )
##################################################################################
# DISPLAYING RESULTS!

if st.button('See the Magic! 🎉'):
    tab1, tab2, tab3 = st.tabs(["CARTOON 😲", "POP ART 👀", "WATERCOLOR 🎨"])
    with tab1:
        st.write('### CARTOON STYLED IMAGE')
        cartoon_img = cartoon_style(display_image)
        image_slide(cartoon_img)
        
    with tab2:
        st.write('### POP ART IMAGE')
        pop_art(display_image)
        
    with tab3:
        st.write('### WATERCOLOR STYLED IMAGE')
        painting_img = waterColor_style(display_image)
        image_slide(painting_img)
        
