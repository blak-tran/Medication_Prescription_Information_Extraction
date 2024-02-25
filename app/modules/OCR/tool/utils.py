import gdown
import re
import cv2
import numpy as np
import webcolors
import matplotlib
import matplotlib.pyplot as plt
from app.modules.OCR.modules.detection import draw_bbox
def download_weights(id_or_url, cached=None, md5=None, quiet=False):
    if id_or_url.startswith('http'):
        url = id_or_url
    else:
        url = 'https://drive.google.com/uc?id={}'.format(id_or_url)

    return gdown.cached_download(url=url, path=cached, md5=md5, quiet=quiet)


weight_url = {
    "pan_resnet18_default": "1GKs-NnezTc6WN0P_Zw7h6wYzRRZdJFKl" ,
    "pan_resnet18_sroie19": "1-QvIN0MrP28URQILYvLaF1G1eTx2oh8W" ,
    "transformerocr_mcocr": "1qpXp_-digz2HPTGY_GPdwstzGLhjC_ot",
    "transformerocr_default_vgg": "13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA",
    "transformerocr_default_resnet50": "12dTOZ9VP7ZVzwQgVvqBWz5JO5RXXW5NY",
    "transformerocr_default_resnet50_fpn": "12dTOZ9VP7ZVzwQgVvqBWz5JO5RXXW5NY",
    "transformerocr_config": "1xQqR9swWNCTLEa0ensPDT0HDBHTke3xT",
    "phobert_mcocr": "1v4GQPg4Jx5FWvqJ-2k9YCxEd6iFdlXXa"
}

def download_pretrained_weights(name, cached=None):
    return download_weights(weight_url[name], cached)
    
def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    def atoi(text):
        return int(text) if text.isdigit() else text

    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


STANDARD_COLORS = [
    'Crimson', 'LawnGreen' , 'DeepSkyBlue', 'Gold', 'DarkGrey', 'BlanchedAlmond', 'Bisque',
    'Aquamarine', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'Azure', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'AliceBlue', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]

def from_colorname_to_bgr(color):
    rgb_color = webcolors.name_to_rgb(color)
    result = (rgb_color.blue, rgb_color.green, rgb_color.red)
    return result

def standard_to_bgr(list_color_name):
    standard = []
    for i in range(len(list_color_name) - 36):  # -36 used to match the len(obj_list)
        standard.append(from_colorname_to_bgr(list_color_name[i]))
    return standard

color_list = standard_to_bgr(STANDARD_COLORS)

def find_highest_score_each_class(labels, probs, class_mapping):
    best_score = [0] * (len(class_mapping.keys()) -1) # exclude NONE class
    best_idx = [-1] * (len(class_mapping.keys()) - 1) # exclude NONE class
    for i, (label, prob) in enumerate(zip(labels, probs)):
        label_idx = class_mapping[label]
        if label_idx != class_mapping["NONE"]:
            if prob > best_score[label_idx]:
                best_score[label_idx] = prob
                best_idx[label_idx] = i
    return best_idx

def visualize(img, boxes, texts, img_name, class_mapping, labels=None, probs=None, visualize_best=False):
    """
    Visualize an image with its bounding boxes
    """
    # Ensure necessary conditions for visualize_best
    if visualize_best:
        assert labels is not None and probs is not None, "To visualize best, please provide labels and probs"

    # Basic setup for the figure
    dpi = matplotlib.rcParams['figure.dpi']
    height, width, depth = img.shape
    figsize = width / float(dpi), height / float(dpi)

    # Placeholder for best_score_idx if needed
    best_score_idx = []

    # Finding the highest score for each class if needed
    if visualize_best:
        best_score_idx = find_highest_score_each_class(labels, probs, class_mapping)

    fig, ax = plt.subplots(figsize=figsize)
    
    # Convert image color space if needed
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for i, box in enumerate(boxes):
        # Extract bounding box coordinates
        x_min, y_min, x_max, y_max = box.astype(int)

        # Define the rectangle patch and add it to the axes
        rect = matplotlib.patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        # Handling labels and probabilities for visualization
        if labels is not None and probs is not None and visualize_best:
            label = labels[i]
            prob = probs[i]
            score = np.round(prob, 3)
            label_text = f'{texts[i]}: {class_mapping[label]} | {score}'
            ax.text(x_min, y_min - 10, label_text, color='blue', fontsize=8)
        elif texts:
            # Just put the text if provided
            ax.text(x_min, y_min - 10, texts[i], color='blue', fontsize=8)

    # Display the image
    ax.imshow(img)
    plt.axis('off')
    plt.savefig(img_name, bbox_inches='tight')
    plt.close()
