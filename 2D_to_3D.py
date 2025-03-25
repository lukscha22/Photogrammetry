OPENMVG_SFM_BIN = ".../openMVG/bin"
OPENMVS_BIN = ".../openMVS/build/bin/vc17/x64/Release"

CAMERA_SENSOR_WIDTH_DIRECTORY = ".../openMVG/src/openMVG/exif/sensor_width_database"

import os
import subprocess


def get_parent_dir(directory):
    return os.path.dirname(directory)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

input_eval_dir = ".../images"
output_eval_dir = ".../images/output"
if not os.path.exists(output_eval_dir):
  os.mkdir(output_eval_dir)

input_dir = input_eval_dir
output_dir = output_eval_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

matches_dir = os.path.join(output_dir, "matches")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")


if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)

print ("1. Intrinsics analysis")
pIntrisics = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),
     "-i", input_dir,
     "-o", matches_dir,
     "-d", camera_file_params,
     "-c", "3",
     "-f", "1000"] )
pIntrisics.wait()

print ("2. Compute features")
pFeatures = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),
     "-i", matches_dir+"/sfm_data.json",
     "-o", matches_dir,
     "-m", "SIFT",
     "-f" , "1"] )
pFeatures.wait()

print ("3. Compute matches")
pMatches = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),
     "-i", matches_dir+"/sfm_data.json",
     "-o", matches_dir+"/matches.putative.bin",
     "-f", "1",
     "-n", "ANNL2"] )
pMatches.wait()

print ("4. Filter matches" )
pFiltering = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GeometricFilter"),
     "-i", matches_dir+"/sfm_data.json",
     "-m", matches_dir+"/matches.putative.bin" ,
     "-g" , "f" ,
     "-o" , matches_dir+"/matches.f.bin" ] )
pFiltering.wait()

reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")

print ("5. Do Incremental/Sequential reconstruction")
pRecons = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfM"),
     "--sfm_engine", "INCREMENTAL",
     "--input_file", matches_dir+"/sfm_data.json",
     "--match_dir", matches_dir,
     "--output_dir", reconstruction_dir] )
pRecons.wait()

print ("6. Colorize Structure")
pRecons = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),
     "-i", reconstruction_dir+"/sfm_data.bin",
     "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()

print ("7. Structure from Known Poses (robust triangulation)")
pRecons = subprocess.Popen(
    [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),
     "-i", reconstruction_dir+"/sfm_data.bin",
     "-m", matches_dir,
     "-o", os.path.join(reconstruction_dir,"robust.ply")] )
pRecons.wait()


print("8. Convert openMVG output to OpenMVS format")
scene_mvs = os.path.join(output_dir, "scene.mvs")
pConversion = subprocess.Popen([
    os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2openMVS"),
    "-i", os.path.join(reconstruction_dir, "sfm_data.bin"),
    "-d", input_dir,
    "-o", scene_mvs
])
pConversion.wait()


print("9. Densify Point Cloud")
scene_dense_mvs  = os.path.join(output_dir, "scene_dense.mvs")
pDensify = subprocess.Popen([
    os.path.join(OPENMVS_BIN, "DensifyPointCloud.exe"),
    scene_mvs,
    "--working-folder", output_dir,
    "--output-file", scene_dense_mvs
])
pDensify.wait()


print("10. Reconstruct Mesh")
scene_mesh_ply = os.path.join(output_dir, "scene_mesh.ply")
pMesh = subprocess.Popen([
    os.path.join(OPENMVS_BIN, "ReconstructMesh.exe"),
    scene_dense_mvs,
    "--working-folder", output_dir,
    "--output-file", os.path.join(output_dir, "scene_mesh.mvs"),
    "--export-type", "ply"
])
pMesh.wait()


print("11. Refine Mesh")
scene_mesh_refine_mvs = os.path.join(output_dir, "scene_mesh_refine.mvs")
pRefine = subprocess.Popen([
    os.path.join(OPENMVS_BIN, "RefineMesh.exe"),
    scene_dense_mvs,
    "--mesh-file", scene_mesh_ply,
    "--working-folder", output_dir,
    "--output-file", scene_mesh_refine_mvs
])
pRefine.wait()


print("12. Texture Mesh")
scene_mesh_textured_mvs = os.path.join(output_dir, "scene_mesh_textured.mvs")
scene_mesh_refine_ply   = os.path.join(output_dir, "scene_mesh_refine.ply")
pTexture = subprocess.Popen([
    os.path.join(OPENMVS_BIN, "TextureMesh.exe"),
    scene_dense_mvs,
    "--mesh-file", scene_mesh_refine_ply,
    "--working-folder", output_dir,
    "--output-file", scene_mesh_textured_mvs
])
pTexture.wait()

print("3D Reconstruction Pipeline Completed!")


