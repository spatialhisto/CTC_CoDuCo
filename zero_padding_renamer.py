import os


def zero_padding_renamer(ROI_path):
    for filename in os.listdir(ROI_path):
        if filename.startswith("ROI_") and filename.endswith(".tiff"):
            prefix, num = filename[:-5].split('_')
            num = num.zfill(4)
            new_filename = prefix + "_" + num + ".tiff"
            os.rename(os.path.join(ROI_path, filename), os.path.join(ROI_path, new_filename))

#
# path = "W:/Analysis/Lilli Hofmann/exp70LB/ROI_mask/278LB/"
#
# for filename in os.listdir(path):
#     if filename.startswith("ROI_") and filename.endswith(".tiff"):
#         prefix, num = filename[:-5].split('_')
#         num = num.zfill(4)
#         new_filename = prefix + "_" + num + ".tiff"
#         os.rename(os.path.join(path, filename), os.path.join(path, new_filename))