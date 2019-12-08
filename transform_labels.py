import os

clazz = "beer"
label_folder = "beer_learning/Label"
output_file = "beer_learning/labels.csv"


def get_labels(file_path):
    file_id = filename.split(".")[0]
    img_file = "img/" + file_id + ".jpg"
    ret = []
    with open(file_path) as fr:
        for line in fr.readlines():
            splits = line.split()
            splits.pop(0)  # remove label
            splits = [str(int(float(x))) for x in splits] # to int
            splits.insert(0, img_file)  # insert image file
            splits.append(clazz)  # add label
            ret.append(",".join(splits) + "\n")

    return ret


with open(output_file, "w") as fw:
    for filename in os.listdir(label_folder):
        file_path = os.path.join(label_folder, filename)

        lines = get_labels(file_path)
        fw.writelines(lines)