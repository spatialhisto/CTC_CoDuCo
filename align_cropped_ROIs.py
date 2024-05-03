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

        # align and save ROIs from background image
        for ch in range(len(channels)):
            channel = channels[ch]
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
