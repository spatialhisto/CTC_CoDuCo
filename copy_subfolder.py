import math
import os
import shutil
import pandas


def move_to_subfolder(root_directory, experiment, sample):

    # pathname for potential subfolders
    subfolder_1 = f"{root_directory}/{experiment}/ROI_full_res/{sample}/{sample}_1-3000/"
    subfolder_2 = f"{root_directory}/{experiment}/ROI_full_res/{sample}/{sample}_3001-6000/"
    subfolder_3 = f"{root_directory}/{experiment}/ROI_full_res/{sample}/{sample}_6001-9000/"
    subfolder_4 = f"{root_directory}/{experiment}/ROI_full_res/{sample}/{sample}_9001-12000/"
    subfolder_list = [subfolder_1, subfolder_2, subfolder_3, subfolder_4]

    BG_subfolder_1 = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/{sample}_BG_1-3000/"
    BG_subfolder_2 = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/{sample}_BG_3001-6000/"
    BG_subfolder_3 = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/{sample}_BG_6001-9000/"
    BG_subfolder_4 = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/{sample}_BG_9001-12000/"
    BG_subfolder_list = [BG_subfolder_1, BG_subfolder_2, BG_subfolder_3, BG_subfolder_4]

    # path to ROI input table
    in_ROI_table = f"{root_directory}/{experiment}/ROI_mask/{sample}/MyExpt_ROI.csv"

    ROI_table = pandas.read_csv(in_ROI_table)
    ROI_count = len(ROI_table)

    if ROI_count > 3000:

        subfolder_count = math.ceil(ROI_count / 3000)
        for num in range(subfolder_count):
            if not os.path.exists(subfolder_list[num]):
                os.makedirs(subfolder_list[num])
            if not os.path.exists(BG_subfolder_list[num]):
                os.makedirs(BG_subfolder_list[num])

        for filename in os.listdir(f"{root_directory}/{experiment}/ROI_full_res/{sample}/"):
            if filename.endswith(".tif"):
                print(f"filename: {filename}")

                # original scan filename structure
                channel, ROI, num = filename[:-4].split('_')
                source = f"{root_directory}/{experiment}/ROI_full_res/{sample}/{filename}"

                if int(num) < 3001:
                    destination = subfolder_1 + filename
                elif int(num) < 6001:
                    destination = subfolder_2 + filename
                elif int(num) < 9001:
                    destination = subfolder_3 + filename
                else:
                    destination = subfolder_4 + filename

                print(f"source: {source}")
                print(f"source: {destination}")
                shutil.move(source, destination)

        for filename in os.listdir(f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/"):
            if filename.endswith(".tif"):
                print(f"filename: {filename}")
                # original scan filename structure
                BG, channel, ROI, num, alignment = filename[:-4].split('_')
                source = f"{root_directory}/{experiment}/ROI_full_res/{sample}_BG/{filename}"

                if int(num) < 3001:
                    destination = BG_subfolder_1 + filename
                elif int(num) < 6001:
                    destination = BG_subfolder_2 + filename
                elif int(num) < 9001:
                    destination = BG_subfolder_3 + filename
                else:
                    destination = BG_subfolder_4 + filename

                shutil.move(source, destination)


# root_directory = f"W:/Analysis/Lilli Hofmann"
# experiment = "exp82LB"
# sample_list = ["422LB"]
#
# for sample in sample_list:
#     move_to_subfolder(root_directory=root_directory, experiment=experiment, sample=sample)


########################################
############# old version ##############
########################################
#
# for scan in sample_scans:
#     path = f"W:/Analysis/Lilli Hofmann/{experiment}/ROI_full_res/{scan}/"
#     subfolder_1 = f"W:/Analysis/Lilli Hofmann/{experiment}/ROI_full_res/{scan}/{scan}_1-3000/"
#     # subfolder_2 = f"W:/Analysis/Lilli Hofmann/{experiment}/ROI_full_res/{scan}/{scan}_3001-end/"
#     subfolder_2 = f"W:/Analysis/Lilli Hofmann/{experiment}/ROI_full_res/{scan}/{scan}_3001-6000/"
#     # subfolder_3 = f"W:/Analysis/Lilli Hofmann/{experiment}/ROI_full_res/{scan}/{scan}_6000-end/"
#
#
#     if not os.path.exists(subfolder_1):
#         os.makedirs(subfolder_1)
#     if not os.path.exists(subfolder_2):
#         os.makedirs(subfolder_2)
#     # if not os.path.exists(subfolder_3):
#     #     os.makedirs(subfolder_3)
#     print("directories exist")
#
#
#     for filename in os.listdir(path):
#
#
#         if filename.endswith(".tif"):
#             print(f"filename: {filename}")
#             source = path + filename
#             print(f"source: {source}")
#
#             if "BG" in scan:
#                 # BG scan filename structure
#                 BG, channel, ROI, num, alignment = filename[:-4].split('_')
#             else:
#                 # original scan filename structure
#                 channel, ROI, num = filename[:-4].split('_')
#
#
#             if int(num) > 3000:
#                 print(f"filename: {filename}")
#                 print(f"number: {num}")
#
#
#                 if int(num) < 3001:
#                     destination = subfolder_1 + filename
#                 elif int(num) < 6001:
#                     destination = subfolder_2 + filename
#                 # else:
#                 #     destination = subfolder_3 + filename
#
#                 print(destination)
#                 shutil.copy(source, destination)
#
