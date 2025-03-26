import streamlit as st
import os.path
import pathlib
import sys
import shutil
from uuid import uuid4
from osgeo import gdal

CLOUD_EMOJI_URL = "https://em-content.zobj.net/source/apple/354/cloud_2601-fe0f.png"

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

uploaded_file = None

def readFile(uploaded_file):
    """ Returns GDAL Dataset from the uploaded file"""
    mmap_name = '/vsimem/'+uuid4().hex
    gdal.FileFromMemBuffer(mmap_name, uploaded_file.read())
    ds = gdal.Open(mmap_name, 1)
    return ds

def createOverview(ds):
    """ Creates Overview of the TIFF """
    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'LZW')
    ds.BuildOverviews('AVERAGE', [2, 4, 8, 16, 32, 64, 128, 256])
    return ds

def createCOG(in_ds, DOWNLOADS_PATH, filename):
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(str(DOWNLOADS_PATH / filename), in_ds, options=["TILED=YES", "COMPRESS=LZW", "COPY_SRC_OVERVIEWS=YES"])

STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'
DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")

uploaded_file = st.file_uploader("Choose the GeoTIFF file", type=['tif','tiff'])
if uploaded_file is not None:
    if st.button('Create COG'):
        try:
            shutil.rmtree(str(DOWNLOADS_PATH)) #removing folder
        except OSError:
            pass

        if not DOWNLOADS_PATH.is_dir():
            DOWNLOADS_PATH.mkdir()

        with st.spinner('Generating Cloud Optimized GeoTIFF...'):
            ds = readFile(uploaded_file) # Creating a GDAL Dataset
            filename = 'cog_' + uploaded_file.name # Defining the name of the file

            ds = createOverview(ds)
            st.info('Overviews are created')

            createCOG(ds, DOWNLOADS_PATH, filename)
            st.success("✅ **Cloud Optimized GeoTIFF is created**.")

            with open(DOWNLOADS_PATH / filename, "rb") as f:
                data = f.read()

            st.download_button(
                label="📥 Download COG",
                data=data,
                file_name=filename,
                mime="image/tiff"
            )

"""
---
[![Follow](https://img.shields.io/twitter/follow/mykolakozyr?style=social)](https://www.twitter.com/mykolakozyr)
[![Follow](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin&labelColor=blue)](https://www.linkedin.com/in/mykolakozyr/)

## Details
The app creates the [Cloud Optimized GeoTIFF (COG)](https://www.cogeo.org/) from the GeoTIFF file. 
The implementation designed to be as simple as possible. 
The COG Creation code is mainly based on [the article](https://medium.com/@saxenasanket135/cog-overview-and-how-to-create-and-validate-a-cloud-optimised-geotiff-b39e671ff013) by [Sanket Saxena](https://medium.com/@saxenasanket135) with [PyGDAL specifics](https://stackoverflow.com/a/50949172).

The outcome of the creator is the Cloud Optimized GeoTIFF: 
- Overviews built with the following parameters: `'AVERAGE', [2, 4, 8, 16, 32, 64, 128, 256]`
- COG built with the following parameters: `"TILED=YES", "COMPRESS=LZW", "COPY_SRC_OVERVIEWS=YES"`
"""

with st.expander("Quality Assurance"):
    st.write("✅ Tested on Google Chrome Version 97.0.4692.99.")
    st.write(":warning: Opens COG file in the new tab in Safari Version 14.1 (15611.1.21.161.7, 15611).")
    st.write("⛔️ Not working if the filename has blanks. See [issue](https://github.com/mykolakozyr/cogcreator/issues/1).")
    st.write("✅ Removes the file from the static folder once creating the next COG.")
    st.write("✅ Generates [valid](https://share.streamlit.io/mykolakozyr/cogvalidator/main/app/app.py) Cloud Optimized GeoTIFF.")

with st.expander("Known Limitations"):
    st.write(":warning: Max file size to upload is 200MB.")
    st.write(":warning: Overview levels are hardcoded to [2, 4, 8, 16, 32, 64, 128, 256].")
    st.write(":warning: LZW Compression is hardcoded.")
    st.write(":warning: Supports only TIF(F) files as an input.")
    st.write(":warning: Hardcoded code for no BIGTIFF support.")
    st.write(":warning: Uses a [dirty hack](https://github.com/streamlit/streamlit/issues/400#issuecomment-648580840) to download data — now replaced by `st.download_button`. 🎉")
