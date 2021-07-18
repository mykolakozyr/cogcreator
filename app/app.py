import streamlit as st
import os.path
import sys
import base64
from urllib.parse import urlparse
import struct
from uuid import uuid4
from osgeo import gdal
from io import BytesIO
from PIL import Image

#import validate_cloud_optimized_geotiff as creator

CLOUD_EMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/cloud_2601-fe0f.png"


# Set page title and favicon.
st.set_page_config(
    page_title="COG Creator", 
    page_icon=CLOUD_EMOJI_URL
)

# Display header.
st.markdown("<br>", unsafe_allow_html=True)
st.image(CLOUD_EMOJI_URL, width=80)

"""
# Cloud Optimized GeoTIFF Creator
"""
# source = st.radio("Select the source of your Cloud Optimized GeoTIFF",('Local file', 'Link to remote file'))

uploaded_file = None
# cog_link = None

# def is_file_url(url):
#     path = urlparse(cog_link)
#     filename = os.path.basename(path.path)
#     if '.' not in filename:
#         return False
#     ext = filename.rsplit('.', 1)[-1]
#     return ext in {'tiff', 'tif'}


# def is_url(url):
#   try:
#     path = urlparse(cog_link)
#     return all([path.scheme, path.netloc])
#   except ValueError:
#     return False

def readURL(url):
    """ Returns GDAL Dataset from the link"""
    vsiurl = '/vsicurl/' + url
    ds = gdal.OpenEx(vsiurl)
    return ds

def readFile(uploaded_file):
    """ Returns GDAL Dataset from the uploaded file"""
    mmap_name = '/vsimem/'+uuid4().hex
    st.write(mmap_name)
    gdal.FileFromMemBuffer(mmap_name, uploaded_file.read())
    ds = gdal.Open(mmap_name)
    return ds

def createOverview(ds):
    """ Creates Overview of the TIFF """
    #gdal.SetConfigOption('COMPRESS_OVERVIEW', 'DEFLATE')
    ds.BuildOverviews('AVERAGE', [4, 8, 16, 32, 64, 128])
    return ds

def createCOG(in_ds):
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.CreateCopy('/vsimem/in_memory_output.tif', in_ds, options=["TILED=YES", "COMPRESS=LZW", "COPY_SRC_OVERVIEWS=YES"])
    return out_ds

def get_image_download_link(img):
    """Generates a link allowing the PIL image to be downloaded
    in:  PIL image
    out: href string
    """
    buffered = BytesIO()
    img.imsave(buffered, format="TIFF")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/tiff;base64,{img_str}">Download result</a>'
    return href

# if source == 'Local file':
uploaded_file = st.file_uploader("Choose a TIFF file", type=['tif','tiff'])
if uploaded_file is not None:
    if st.button('Create COG'):
        with st.spinner('Creating your COG file...'):
            ds = readFile(uploaded_file)
            filename = uploaded_file.name
            st.write(filename)

            ds = createOverview(ds)
            st.write('Overviews created')

            cog_ds = createCOG(ds)
            st.write('COG created')
            st.write(type(cog_ds))
            
            st.markdown(get_image_download_link(cog_ds.ReadAsArray()), unsafe_allow_html=True)


# elif source == 'Link to remote file':
#     cog_link = st.text_input("Insert a URL of your COG file")
#     if cog_link is not '':
#         if st.button('Validate'):
#             if is_url(cog_link) is True: # Checking if the text input is the link
#                 if is_file_url(cog_link) is True: # Checking if the link pointing on GeoTIFF file
#                     with st.spinner('Validating your file...'):
#                         ds = validator.readURL(cog_link)
#                         a = urlparse(cog_link)
#                         filename = os.path.basename(a.path)    
#                         validator.main_validate(ds, filename)
#                 else:
#                     st.error('The file extension is not GeoTIFF.')
#             else:
#                 st.error('The link is not valid.')

"""
---
[![Follow](https://img.shields.io/twitter/follow/mykolakozyr?style=social)](https://www.twitter.com/mykolakozyr)
&nbsp[![Follow](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/mykolakozyr/)
&nbsp[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/mykolakozyr)

## Details
The implementation designed to be as simple as possible. The validation code used is the one shared on [COG Developers Guide](https://www.cogeo.org/developers-guide.html) linking to [this source code](https://github.com/OSGeo/gdal/blob/master/gdal/swig/python/gdal-utils/osgeo_utils/samples/validate_cloud_optimized_geotiff.py) by [Even Rouault](https://twitter.com/EvenRouault).
"""

col1, col2 = st.beta_columns([2,1])

with col1.beta_expander("Quality Assurance"):
    st.write("✅ Tested on Google Chrome Version 91.0.4472.114.")
    st.write("✅ File with no .tif or .tiff extensions could not be uploaded.")
    st.write("✅ COG uploaded locally is successfully validated.")
    st.write("✅ Broken links are not valid.")
    st.write("✅ Links with no extension are not valid.")
    st.write("✅ Links with no not .tif ot .tiff extensions are not valid.")
    st.write("✅ COG stored on AWS is successfully validated.")
    st.write("✅ Non-COG file returns Not Valid COG error.")
    st.write("✅ Information about size of IFD headers returned.")
    st.write(":warning: Uploaded file is not displayed once changed options after file was uploaded.")
with col2.beta_expander("Known Limitations"):
    st.write(":warning: Max file size to upload is 200MB")