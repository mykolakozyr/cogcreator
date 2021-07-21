# Cloud Optimized GeoTIFF Creator
Simple [Cloud Optimized GeoTIFF](https://www.cogeo.org/) Creator. Just upload a GeoTIFF file and click "Create COG". The app would build a Cloud Optimized GeoTIFF so you can download it.

![COG Creator Demo](https://cogviewerapp.s3.eu-central-1.amazonaws.com/cogcreator.gif)

## Details
The implementation designed to be as simple as possible. The COG Creation code is mainly based on [the article](https://medium.com/@saxenasanket135/cog-overview-and-how-to-create-and-validate-a-cloud-optimised-geotiff-b39e671ff013) by [Sanket Saxena](https://medium.com/@saxenasanket135) with [PyGDAL specifics](https://stackoverflow.com/a/50949172).

The outcome of the creator is the Cloud Optimized GeoTIFF: 
- Overviews built with the following parameters: `'AVERAGE', [2, 4, 8, 16, 32, 64, 128, 256]`
- COG build with the following parameters: `"TILED=YES", "COMPRESS=LZW", "COPY_SRC_OVERVIEWS=YES"`

### Quality Assurance
- ✅ Tested on Google Chrome Version 91.0.4472.114.
- :warning: Opens COG file in the new tab in Safari Version 14.1 (15611.1.21.161.7, 15611).
- ✅ Removes the file from the static folder once creating the next COG.
- ✅ Generates [valid](https://share.streamlit.io/mykolakozyr/cogvalidator/main/app/app.py) Cloud Optimized GeoTIFF.
### Known Limitations
- :warning: Max file size to upload is 200MB.
- :warning: Overview levels are hardcoded to [2, 4, 8, 16, 32, 64, 128, 256].
- :warning: LZW Compression is hardcoded.
- :warning: Supports only TIF(F) files as an input.
- :warning: Hardcoded code for no BIGTIFF support.
- :warning: Uses a [dirty hack](https://github.com/streamlit/streamlit/issues/400#issuecomment-648580840) to download data.
- :warning: requirements.txt should be reviewed and cleaned.
