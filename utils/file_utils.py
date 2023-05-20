import os


IMAGE_EXTENSIONS = ("jpg", "jpeg", "png")


def find_files(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # file_path = os.path.join(root, file)
            # print(file_path)
            file_list.append(file)

    return file_list
