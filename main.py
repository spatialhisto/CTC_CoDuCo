import os
from PIL import Image
import zero_padding_renamer
import crop_align_images_pyStackReg
import align_cropped_ROIs
import copy_subfolder

Image.MAX_IMAGE_PIXELS = None

root_directory = f"W:/Analysis/Lilli Hofmann"
channels = ["DAPI", "Atto425", "Atto488", "Cy3", "TR", "Cy5", "Cy7"]

experiment = "exp17KP"
sample_list = ["64KP"]

BG_scan_available = True #is a background scan available for background subtraction (True/False)?

# TODO: create folder structure for CellProfiler analysis
print("create folder structure for CellProfiler analysis")
for sample in sample_list:
    print(f"sample {sample}")
    CP_output_folder = f"{root_directory}/{experiment}/CP_output_{sample}/"
    if not os.path.exists(CP_output_folder):
        print("path does not exist")
        os.makedirs(CP_output_folder)


# TODO: use zero padding renamer for ROI-mask-images
for sample in sample_list:
    ROI_path = f"{root_directory}/{experiment}/ROI_mask/{sample}/"
    zero_padding_renamer.zero_padding_renamer(ROI_path=ROI_path)


# TODO: crop and align images
for sample in sample_list:

    print(f"prepare cropping of sample {sample}")
    # TODO: path to input and output files
    in_channels_orig, in_channels_BG, in_DAPI_8x8, in_DAPI_BG_8x8, in_ROI_table, out_path, out_path_temp, out_path_BG = crop_align_images_pyStackReg.define_path(root_directory=root_directory, experiment=experiment, sample=sample)

    # TODO: create ROI list
    ROI_list, bounding_box_list = crop_align_images_pyStackReg.create_ROI_list(in_ROI_table=in_ROI_table)

    print(f"prealignment and cropping of sample {sample}")
    # TODO: crop and save original ROIs
    crop_align_images_pyStackReg.crop_orig_ROIs(channels=channels, in_channels=in_channels_orig, ROI_list=ROI_list, bounding_box_list=bounding_box_list, out_path=out_path)

    # TODO: image registration using pyStackReg rigid-body (rotation + translation) + cropping BG image ROIs
    if BG_scan_available:
        crop_align_images_pyStackReg.align_crop_BG_ROIs(in_DAPI_8x8=in_DAPI_8x8, in_DAPI_BG_8x8=in_DAPI_BG_8x8, out_path=out_path_temp, channels=channels, in_channels=in_channels_BG, ROI_list=ROI_list, bounding_box_list=bounding_box_list)

    # TODO: final alignment of cropped ROIs
        print(f"final alignment of cropped BG-ROIs of sample {sample}")
        align_cropped_ROIs.final_alignment(ROI_list=ROI_list, root_directory=root_directory, experiment=experiment, sample=sample, channels=channels, out_path=out_path_BG)


# TODO: if sample has >3000 ROIs, move files to subfolders
for sample in sample_list:
    copy_subfolder.move_to_subfolder(root_directory=root_directory, experiment=experiment, sample=sample, BG_scan_available=BG_scan_available)

