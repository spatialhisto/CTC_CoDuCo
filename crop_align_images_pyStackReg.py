import gc
import os
import pandas
import pystackreg.util
from PIL import Image
import numpy as np
from pystackreg import StackReg
from skimage import io


# TODO: path to input and output files

def define_path(root_directory, experiment, sample):

    # path to original images
    in_DAPI = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_DAPI_mono.tif"
    in_ATTO425 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_Atto425 SS440.tif"
    in_ATTO488 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_FITC SS488.tif"
    in_CY3 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_Cy3 SS546.tif"
    in_TR = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_TxRed SS blue.tif"
    in_CY5 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_Cy5.tif"
    in_CY7 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01_Cy7.tif"
    in_channels_orig = [in_DAPI, in_ATTO425, in_ATTO488, in_CY3, in_TR, in_CY5, in_CY7]

    # path to BG images
    in_DAPI_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_DAPI_mono.tif"
    in_ATTO425_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_Atto425 SS440.tif"
    in_ATTO488_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_FITC SS488.tif"
    in_CY3_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_Cy3 SS546.tif"
    in_TR_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_TxRed SS blue.tif"
    in_CY5_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_Cy5.tif"
    in_CY7_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_Cy7.tif"
    in_channels_BG = [in_DAPI_BG, in_ATTO425_BG, in_ATTO488_BG, in_CY3_BG, in_TR_BG, in_CY5_BG, in_CY7_BG]

    # path to 8x8 binned images that are used for registration to get a transformation matrix
    in_DAPI_8x8 = f"{root_directory}/{experiment}/8x8_binned/{sample}.vsi.Collection/{sample}_40x_EFI_01_DAPI_mono.tif"
    in_DAPI_BG_8x8 = f"{root_directory}/{experiment}/8x8_binned/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01_DAPI_mono.tif"

    # path to ROI input table
    in_ROI_table = f"{root_directory}/{experiment}/ROI_mask/{sample}/MyExpt_ROI.csv"

    # create output folders
    out_path = f"{root_directory}/{experiment}/ROI_full_res/{sample}/"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_path_temp = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/"
    if not os.path.exists(out_path_temp):
        os.makedirs(out_path_temp)
    out_path_BG = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/"
    if not os.path.exists(out_path_BG):
        os.makedirs(out_path_BG)

    return in_channels_orig, in_channels_BG, in_DAPI_8x8, in_DAPI_BG_8x8, in_ROI_table, out_path, out_path_temp, out_path_BG


# TODO: create ROI list
def create_ROI_list(in_ROI_table):
    ROI_table = pandas.read_csv(in_ROI_table)
    ROI_list = []
    bounding_box_list = []
    print("create ROI and bounding box list")
    for index, row in ROI_table.iterrows():
        ROI_num = row.ObjectNumber
        ROI_list.append(ROI_num)
        bounding_box = (row.AreaShape_BoundingBoxMinimum_X * 8,
                          row.AreaShape_BoundingBoxMinimum_Y * 8,
                          row.AreaShape_BoundingBoxMaximum_X * 8,
                          row.AreaShape_BoundingBoxMaximum_Y * 8)

        bounding_box_list.append(bounding_box)

    return ROI_list, bounding_box_list


# TODO: crop and save ROIs
def crop_orig_ROIs(channels, in_channels, ROI_list, bounding_box_list, out_path):
    for i in range(len(channels)):
        channel = channels[i]
        input = in_channels[i]

        print(f"open {channel} full_scan as np array")
        full_scan = np.array(Image.open(input))

        print("crop ROIs")
        for i in range(len(ROI_list)):
            max_digits = len(str(len(ROI_list)))
            i_digits = len(str(ROI_list[i]))
            prefix = ""
            for dig in range(max_digits - i_digits):
                prefix = prefix + "0"

            cropped_ROI = full_scan[bounding_box_list[i][1]:bounding_box_list[i][3],
                          bounding_box_list[i][0]:bounding_box_list[i][2]]
            Image.fromarray(cropped_ROI).save(f"{out_path}{channel}_ROI_{prefix}{ROI_list[i]}.tif", format="TIFF")

            del cropped_ROI
        del full_scan
        gc.collect()


# TODO: image registration using pyStackReg rigid-body (rotation + translation) + cropping BG image ROIs
def align_crop_BG_ROIs(in_DAPI_8x8, in_DAPI_BG_8x8, out_path, channels, in_channels, ROI_list, bounding_box_list):
    # 8x8 binned images are used for registration to get a transformation matrix
    print("loading images for registration")

    reference_image = io.imread(in_DAPI_8x8)
    moving_image = io.imread(in_DAPI_BG_8x8)

    sr = StackReg(StackReg.RIGID_BODY)

    print("register")
    # register 2nd image to 1st
    sr.register(reference_image[:, :], moving_image[:, :])

    matrix = sr.get_matrix()
    print(sr.get_matrix())
    matrix_df = pandas.DataFrame(matrix)
    matrix_df.to_csv(path_or_buf=f"{out_path}transformation_matrix_8x8.csv", index=False)

    ###########################################################################
    print("try to create and save an overlay of the alignment (8x8 binned images)")
    moving_image_aligned = sr.transform(moving_image[:, :])
    reference_image = reference_image / 65536
    moving_image_aligned = moving_image_aligned / 65536

    ydim, xdim = reference_image.shape

    temp_image_ref = np.zeros((ydim, xdim, 3), dtype=np.float32)
    RGB_mapping_ref = [0, 255, 0]
    for c in range(0, 3):
        temp_image_ref[..., c] += reference_image * RGB_mapping_ref[c]
    temp_image_ref = temp_image_ref / np.max(temp_image_ref) * 255

    temp_image_mov = np.zeros((ydim, xdim, 3), dtype=np.float32)
    RGB_mapping_mov = [255, 0, 0]
    for c in range(0, 3):
        temp_image_mov[..., c] += moving_image_aligned * RGB_mapping_mov[c]
    temp_image_mov = temp_image_mov / np.max(temp_image_mov) * 255

    multiplex_image = temp_image_ref + temp_image_mov
    image_rgb = Image.fromarray(multiplex_image.astype(np.uint8))
    image_rgb.save(f"{out_path}alignment_DAPI_8x8.png")
    print("alignment image saved as png")
    ##########################################################################

    # upscale the transformation matrix to full-resolution images
    upscaling = np.array([1., 1., 8., 1., 1., 8., 1., 1., 1.]).reshape((3, 3))
    upscaled_matrix = matrix * upscaling
    sr.set_matrix(upscaled_matrix)
    print(sr.get_matrix())
    matrix_upscaled_df = pandas.DataFrame(upscaled_matrix)
    matrix_upscaled_df.to_csv(path_or_buf=f"{out_path}transformation_matrix_full-res.csv", index=False)

    del reference_image, moving_image, moving_image_aligned, temp_image_ref, temp_image_mov, multiplex_image, image_rgb
    gc.collect()

    # TODO: crop and save ROIs from background image
    for i in range(len(channels)):
        channel = channels[i]
        input = in_channels[i]
        print(f"BG {channel}")
        print("open full_scan as np array")
        full_scan = io.imread(input)
        full_scan = full_scan.astype(np.float)
        print(sr.get_matrix())
        print("use the transformation from the above registration")
        full_scan_aligned = sr.transform(full_scan[:, :])
        print("convert")
        full_scan_aligned_16 = pystackreg.util.to_uint16(full_scan_aligned)

        print("crop ROIs")
        for i in range(len(ROI_list)):
            max_digits = len(str(len(ROI_list)))
            i_digits = len(str(ROI_list[i]))
            prefix = ""
            for dig in range(max_digits - i_digits):
                prefix = prefix + "0"

            cropped_ROI = full_scan_aligned_16[bounding_box_list[i][1]:bounding_box_list[i][3],
                          bounding_box_list[i][0]:bounding_box_list[i][2]]
            io.imsave(f"{out_path}BG_{channel}_ROI_{prefix}{ROI_list[i]}.tif", cropped_ROI)

            del cropped_ROI
        del full_scan, full_scan_aligned, full_scan_aligned_16
        gc.collect()
