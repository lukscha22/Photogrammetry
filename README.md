This repository contains instructions on how to create 3D models from 2D images using only a PC or laptop with a decent CPU and a smartphone. No fancy equipment required.

->Software Requirements
CMake

Visual Studio 2022

Git 

ExifTool (useful for managing image metadata)

3D model viewer (e.g., Cloud Compare)

->Setup
Clone the openMVG and openMVS repositories from GitHub.

Use CMake to build and install the cloned files. Follow the "build tutorial" sections on their respective GitHub pages.

If you encounter build problems, research whether you need the problematic components. You only need the essentials for this pipeline to work.

->Taking Photos
Find a well-lit location, ideally between a window and an artificial light source.

Use a smooth, monochrome surface as a background.

Capture images of the object from all angles:

Fix your phone in a stable position.

Rotate the object between shots, ensuring 80-90% overlap between consecutive images.

Capture only the object and background surface.

->Managing EXIF Data
Find your phone's focal length (usually between 6-8mm).

Transfer images to your PC.

Check for existing EXIF data in image properties.

If EXIF data is present:

Add camera make and model to "...\openMVG\src\openMVG\exif\sensor_width_database\sensor_width_camera_database.txt".

If EXIF data is missing:

Add your phone model and focal length to the database file.

Use ExifTool to add make and model to each image:

.\exiftool.exe -Make="samsung" -Model="Galaxy A53" .\image_name.jpg

->Running the Pipeline
Edit the provided Python script to match your image and bin file folder paths.

Run the script (takes about 20-30 minutes).

View the resulting .ply files in CloudCompare or your preferred 3D viewer.

->Troubleshooting
If the pipeline fails, check the logs to identify the problem area and work on a fix.

->Disclaimer
This guide provides a starting point for photogrammetry using freely available tools. It may not be perfect but offers a foundation for further exploration and optimization.

Useful Links:
openMVG - https://github.com/openMVG/openMVG 
openMVS - https://github.com/cdcseacave/openMVS 
exiftool - https://exiftool.org CMake - https://cmake.org 
Cloud Compare - https://www.danielgm.net/cc/

For any issues or suggestions for improvement, feel free to reach out
