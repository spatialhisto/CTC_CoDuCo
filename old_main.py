from pystackreg import StackReg
from skimage import io
import numpy as np

###

experiment = "exp59LB"
root_directory = f"W:/Analysis/Lilli Hofmann"
sample_list = ["237LB"]
#sample_list = ["228LB", "229LB", "230LB", "231LB", "232LB", "233LB", "234LB", "235LB", "236LB", "237LB"]
channels = ["DAPI", "Atto425", "Atto488", "Cy3", "TR", "Cy5", "Cy7"]


for sample in sample_list:
    print(f"processing sample {sample}")

    # TODO: path to input and output files
    in_DAPI = f"{root_directory}/{experiment}/8x8_binned/{sample}.vsi.Collection/{sample}_Layer0-40x_EFI_01/{sample}_Layer0-40x_EFI_01_CH0-DAPI_mono.tif"
    # in_DAPI = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH0-DAPI_mono.tif"
    # in_ATTO425 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH3-Atto425 SS440.tif"
    # in_ATTO488 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH4-FITC SS488.tif"
    # in_CY3 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH5-Cy3 SS546.tif"
    # in_TR = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH6-TxRed SS blue.tif"
    # in_CY5 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH1-Cy5.tif"
    # in_CY7 = f"{root_directory}/{experiment}/full_res/{sample}.vsi.Collection/{sample}_40x_EFI_01/{sample}_40x_EFI_01_CH2-Cy7.tif"
    # in_channels = [in_DAPI, in_ATTO425, in_ATTO488, in_CY3, in_TR, in_CY5, in_CY7]

    # in_DAPI_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH0-DAPI_mono.tif"
    # in_ATTO425_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH3-Atto425 SS440.tif"
    # in_ATTO488_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH4-FITC SS488.tif"
    # in_CY3_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH5-Cy3 SS546.tif"
    # in_TR_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH6-TxRed SS blue.tif"
    # in_CY5_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH1-Cy5.tif"
    # in_CY7_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG.vsi.Collection/{sample}_BG_40x_EFI_01/{sample}_BG_40x_EFI_01_CH2-Cy7.tif"
    # in_channels_BG = [in_DAPI_BG, in_ATTO425_BG, in_ATTO488_BG, in_CY3_BG, in_TR_BG, in_CY5_BG, in_CY7_BG]
    #

    # BG with DAPI restaining
    in_DAPI_BG = f"{root_directory}/{experiment}/8x8_binned/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH0-DAPI_mono.tif"
    # in_ATTO425_BG = f"{root_directory}/{experiment}/8x8_binned/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH3-Atto425 SS440.tif"
    in_DAPI_BG_full_res = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH0-DAPI_mono.tif"

    # in_DAPI_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH0-DAPI_mono.tif"
    # in_ATTO425_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH3-Atto425 SS440.tif"
    # in_ATTO488_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH4-FITC SS488.tif"
    # in_CY3_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH5-Cy3 SS546.tif"
    # in_TR_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH6-TxRed SS blue.tif"
    # in_CY5_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH1-Cy5.tif"
    # in_CY7_BG = f"{root_directory}/{experiment}/full_res/{sample}_BG_DAPI_restained_30min.vsi.Collection/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min/{sample}_BG_DAPI_restained_30min_BG_DAPI_restained_30min_CH2-Cy7.tif"
    # in_channels_BG = [in_DAPI_BG, in_ATTO425_BG, in_ATTO488_BG, in_CY3_BG, in_TR_BG, in_CY5_BG, in_CY7_BG]

    # out_path = f"{root_directory}/{experiment}/ROI_full_res/{sample}/"
    out_path = f"{root_directory}/{experiment}/full_res/{sample}_pyStackReg_align/"


    ###
    print("read img0")
    img0 = io.imread(in_DAPI) # 3 dimensions : frames x width x height
    print("read img1")
    img1 = io.imread(in_DAPI_BG) # same shape as img0
    # img0.shape: frames x width x height (3D)
    sr = StackReg(StackReg.RIGID_BODY)

    print("register")
    # register 2nd image to 1st
    sr.register(img0[:, :], img1[:, :])
    matrix = sr.get_matrix()
    print(sr.get_matrix())

    upscaling = np.array([1., 1., 8., 1., 1., 8., 1., 1., 1.]).reshape((3,3))
    upscaled_matrix = matrix * upscaling

    sr.set_matrix(upscaled_matrix)
    print(sr.get_matrix())


    print("use transformation")
    # # use the transformation from the above registration to register another frame
    # out = sr.transform(img1[:,:])
    # print(type(out))
    # # print(out.shape())
    # print("save transformed image")
    # io.imsave(f"{out_path}DAPI_pyStackReg_aligned.tif", out)

    # use the transformation from the above registration to register another frame
    print("read img2")
    img2 = io.imread(in_DAPI_BG_full_res)  # different shape as img0
    out_DAPI_full_res = sr.transform(img2[:,:])
    print(type(out_DAPI_full_res))
    # print(out_atto425.shape())
    print("save transformed image img2")
    io.imsave(f"{out_path}DAPI_pyStackReg_aligned_upscaling.tif", out_DAPI_full_res)