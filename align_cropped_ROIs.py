import gc
import numpy as np
from pystackreg import StackReg, util
from skimage import io


def final_alignment(ROI_list, root_directory, experiment, sample, channels, out_path):
    for i in range(len(ROI_list)):
        max_digits = len(str(len(ROI_list)))
        i_digits = len(str(ROI_list[i]))
        prefix = ""
        for dig in range(max_digits - i_digits):
            prefix = prefix + "0"

        print(f"ref: {root_directory}/{experiment}/ROI_full_res/{sample}/DAPI_ROI_{prefix}{ROI_list[i]}.tif")
        print((f"mov: {root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif"))

        reference_image = io.imread(
            f"{root_directory}/{experiment}/ROI_full_res/{sample}/DAPI_ROI_{prefix}{ROI_list[i]}.tif")
        moving_image = io.imread(
            f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif")

        sr = StackReg(StackReg.RIGID_BODY)

        print("register")
        # register 2nd image to 1st
        sr.register(reference_image[:, :], moving_image[:, :])
        print(sr.get_matrix())

        del reference_image, moving_image
        gc.collect()

        # TODO: align and save ROIs from background image
        for ch in range(len(channels)):
            channel = channels[ch]
            # print(f"open {channel} BG_ROI {prefix}{ROI_list[i]} as np array")
            print(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_{channel}_ROI_{prefix}{ROI_list[i]}.tif")
            BG_ROI = io.imread(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_{channel}_ROI_{prefix}{ROI_list[i]}.tif")
            BG_ROI = BG_ROI.astype(np.float)
            # print("use the transformation from the above registration")
            BG_ROI_aligned = sr.transform(BG_ROI[:, :])
            # print("convert")
            BG_ROI_aligned_16 = util.to_uint16(BG_ROI_aligned)

            # print(f"save aligned ROI: {out_path}BG_{channel}_ROI_{prefix}{ROI_list[i]}_py2xAligned.tif")
            io.imsave(f"{out_path}BG_{channel}_ROI_{prefix}{ROI_list[i]}_py2xAligned.tif", BG_ROI_aligned_16)

            del BG_ROI, BG_ROI_aligned, BG_ROI_aligned_16
            gc.collect()



#########################################################

# import gc
# import os
# import pandas
# from PIL import Image
# import numpy as np
# from skimage.registration import phase_cross_correlation
# from skimage.transform import SimilarityTransform, warp
# from skimage.util import img_as_uint
# from pystackreg import StackReg, util
# from skimage import io
#
#
# Image.MAX_IMAGE_PIXELS = None
#
#
# experiment = "exp70LB"
# root_directory = f"W:/Analysis/Lilli Hofmann"
# sample_list = ["274LB", "276LB", "278LB"]
# #sample_list = ["228LB", "229LB", "230LB", "231LB", "232LB", "233LB", "234LB", "235LB", "236LB", "237LB"]
# channels = ["DAPI", "Atto425", "Atto488", "Cy3", "TR", "Cy5", "Cy7"]
#
#
# for sample in sample_list:
#     print(f"processing sample {sample}")
#     in_ROI_table = f"{root_directory}/{experiment}/ROI_mask/{sample}/MyExpt_ROI.csv"
#
#     # out_path = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_py2xAligned/"
#     # out_path = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_DAPI_restained_pyStackReg_py2x/"
#     out_path_BG = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/"
#     if not os.path.exists(out_path_BG):
#         os.makedirs(out_path_BG)
#
#     # TODO: create ROI list
#     ROI_table = pandas.read_csv(in_ROI_table)
#     # print(ROI_table.head())
#     # ROI_table["width"] = ROI_table["AreaShape_BoundingBoxMaximum_X"] - ROI_table["AreaShape_BoundingBoxMinimum_X"]
#     # ROI_table["height"] = ROI_table["AreaShape_BoundingBoxMaximum_Y"] - ROI_table["AreaShape_BoundingBoxMinimum_Y"]
#     # ROI_table["area"] = ROI_table["width"] * ROI_table["height"]
#     # print(ROI_table.head())
#
#     ROI_list = []
#     print("create ROI list")
#     for index, row in ROI_table.iterrows():
#         ROI_num = row.ObjectNumber
#         ROI_list.append(ROI_num)
#         print(len(ROI_list))
#
#     for i in range(len(ROI_list)):
#         max_digits = len(str(len(ROI_list)))
#         i_digits = len(str(ROI_list[i]))
#         prefix = ""
#         for dig in range(max_digits - i_digits):
#             prefix = prefix + "0"
#
#         print(f"ref: {root_directory}/{experiment}/ROI_full_res/{sample}/DAPI_ROI_{prefix}{ROI_list[i]}.tif")
#         # print((f"mov: {root_directory}/{experiment}/ROI_full_res/{sample}_BG_DAPI_restained_pyStackReg/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif"))
#         print((f"mov: {root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif"))
#
#         reference_image = io.imread(f"{root_directory}/{experiment}/ROI_full_res/{sample}/DAPI_ROI_{prefix}{ROI_list[i]}.tif")
#         # moving_image = np.array(Image.open(f"{root_directory}/{experiment}/ROI_full_res/{sample}/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif"))
#         # moving_image = io.imread(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_DAPI_restained_pyStackReg/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif")
#         moving_image = io.imread(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_DAPI_ROI_{prefix}{ROI_list[i]}.tif")
#
#         sr = StackReg(StackReg.RIGID_BODY)
#
#         print("register")
#         # register 2nd image to 1st
#         sr.register(reference_image[:, :], moving_image[:, :])
#         print(sr.get_matrix())
#
#
#         # print("phase_cross_correlation")
#         # shifts, error, phasediff = phase_cross_correlation(reference_image=reference_image,
#         #                                                    moving_image=moving_image, upsample_factor=1,
#         #                                                    space="real", return_error=True, reference_mask=None,
#         #                                                    moving_mask=None, overlap_ratio=0.7, normalization="phase")
#         # shift_y = shifts[0] * -1
#         # shift_x = shifts[1] * -1
#         # print(f"{sample}: shift_x {shift_x}, shift_y {shift_y}")
#         # tform = SimilarityTransform(translation=(shift_x, shift_y))
#
#         del reference_image, moving_image
#         gc.collect()
#
#         # TODO: align and save ROIs from background image
#         for ch in range(len(channels)):
#             channel = channels[ch]
#             # input = in_channels_BG[i]
#             print(f"open {channel} BG_ROI {prefix}{ROI_list[i]} as np array")
#             print(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_{channel}_ROI_{prefix}{ROI_list[i]}.tif")
#             # BG_ROI = np.array(Image.open(f"{root_directory}/{experiment}/ROI_full_res/{sample}/BG_{channel}_ROI_{prefix}{ROI_list[i]}.tif"))
#             BG_ROI = io.imread(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG_temp/BG_{channel}_ROI_{prefix}{ROI_list[i]}.tif")
#             BG_ROI = BG_ROI.astype(np.float)
#             print("use the transformation from the above registration")
#             BG_ROI_aligned = sr.transform(BG_ROI[:, :])
#             print("convert")
#             BG_ROI_aligned_16 = util.to_uint16(BG_ROI_aligned)
#
#             print(f"save aligned ROI: {out_path_BG}BG_{channel}_ROI_{prefix}{ROI_list[i]}_py2xAligned.tif")
#             io.imsave(f"{out_path_BG}BG_{channel}_ROI_{prefix}{ROI_list[i]}_py2xAligned.tif", BG_ROI_aligned_16)
#
#             del BG_ROI, BG_ROI_aligned, BG_ROI_aligned_16
#             gc.collect()
