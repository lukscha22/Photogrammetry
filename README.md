This repository covers how to go from 2D images to a 3D model without any fancy equipment. All you need is a PC or laptop with a decent CPU and a smartphone. 

I reccommend reading everything first before starting to work, it's really not a long read.

Software requirements:
First off, you'll need to install CMake and Visual studio 22. Having git installed also makes things easier but it's not a neccessary. Exif tool is a tool that will come in handy if you are using your phone as a means to get images. Lastly you'll need a tool for viewing the model and meshes that will be generated. I used Cloud Compare but you can use anything simmilar.

Laying out the groundwork:
Start off going to openMVG and openMVS github pages and cloning those two repositories locally.  

After cloning use CMake to build and install the files that you cloned. There are insturctions on how to build both on their respective GitHub pages under the "build tutorial" sections.

There will potentially be problems with building. If you encounter any problems or errors, do a bit of google-ing to see if you acutally need the parts that are problmatic. You only need the essentials for this pipeline to work, so if you don't need something you can exclude it from the build.

Taking photos:
After that you need to take photos to use for the 3D reconstruction. There are a few things to look out for.
First find a position in your room/office with good lighting. Somewhere between a window and the artificial light source is what worked best for me (keep in mind it was sunny outside so the object was getting light from both sides).

Next find a smooth surface that you can put your object in front of, or one that you can put behind your object. Monochrome surface, color doesnt matter. I used the cover that i got my diploma in (navy blue-ish).

Lastly, you need pictures of the object from all angles. Usually you would move around the object and take pictures of it. I fount that there is too much room for human error that way, so you are going to do the opposite. You will put your phone in a fixed position in which it doesn't move when you tap the screen to take a photo. If you have earphones that have some sort of camera control funcionality it will make this step quite a bit easier. Position the phone so the camera captures only the object and the background surface, nothing else (except the surface below the object). After taking a photo, rotate the object so that at least 80-90% of the image matches with the last one. Check out the images folder to see how the images should look like.

Exif data management:
After taking the photos, google your phones focal length. For most phones its between 6-8 but you can google it just to be sure.

If you didn't already transfer your images to your pc, do it now. Check if the images have exif data by going into their properties, then details and under look under the Camera section. If your images have a camera make and model thats great, if not then you have a bit more work to do.

Once you have that info you will navigate to "...\openMVG\src\openMVG\exif\sensor_width_database\sensor_width_camera_database.txt". 

If your images have a make and model already then open the file and add them to the top of the file. Simmilar to "samsung Galaxy A53;7.6".

If not, open the text file and add your phone model and focal length to the top. It should be something simmilar to "samsung Galaxy A53;7.6". Then download exiftool. The easiest way that I used was to copy the images into the folder with exiftool.exe, then open cmd in that same folder and just run the command on every image you took. It takes a few minutes you only change the numbers in the cmd command.

The command .\exiftool.exe -Make="samsung" -Model="Galaxy A53" .\image_name.jpg

It's always a good idea to make a backup folder with these images if something goes wrong.

The pipeline:
After all of that is done you just have to edit the python script which I provided so it matches the filepaths to your image and bin files folders and you should be good to go. The pipeline should take about 20 - 30 minutes to do it's thing and I recommend not doing anything else on your PC in that time. After it finishes you should have all your .ply files which you can open and view in CloudCompare, or if something fails you can view the logs to see where exactly the problem occured so you can work on a fix.

Disclamer: these are the steps I took to reach the end solution, it's far from perfect but it's a start. I am not the author of any of these libraries or maker of any tools, I just used what I could find to come to a solution. If you have any problems with this or if you think there is a way to better or optimize the sloution feel free to contact me and we'll work something out. Also this is my first time taking a shot with photogrammetry so I will gladly take any construcitve criticism.

Links:

openMVG - https://github.com/openMVG/openMVG
openMVS - https://github.com/cdcseacave/openMVS
exiftool - https://exiftool.org
CMake - https://cmake.org
Cloud Compare - https://www.danielgm.net/cc/

Building openMVG - https://www.youtube.com/watch?v=khHSziC5Bcg&t=525s (This is the "first part" of the pipeline. The person in the video did a great job explaining the build with CMake so i reccomend watching the first part of the video if you run into trouble while building openMVG.)
