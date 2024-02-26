import os
import cv2
import argparse
import torch
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
from app.modules.OCR.modules import Preprocess, Detection, OCR, Retrieval, Correction
from app.modules.OCR.modules.detection.utils.util import order_points_clockwise
from app.modules.OCR.tool.config import Config
from app.modules.OCR.tool.utils import natural_keys, visualize, find_highest_score_each_class
import time
import shutil
from app.core.utils import load_environments
from mmocr.apis import MMOCRInferencer
import mmocr

load_environments()
config = Config('app/modules/OCR/tool/config/configs.yaml')
TEMP_ROOT_PATH = os.getenv("temp_path")


class APP_SCANNER:
    def __init__(self, config) -> None:
        self.do_retrieve = False
        self.find_best_rotation = True
        self.debug = True
        self.load_config(config)
        self.make_cache_folder()
        self.init_modules()

    def load_config(self, config):
        self.det_weight = config.det_weight
        self.ocr_weight = config.ocr_weight
        self.det_config = config.det_config
        self.ocr_config = config.ocr_config
        self.bert_weight = config.bert_weight
        self.class_mapping = {k: v for v, k in enumerate(config.retr_classes)}
        self.idx_mapping = {v: k for k, v in self.class_mapping.items()}
        self.dictionary_path = config.dictionary_csv
        self.retr_mode = config.retr_mode
        self.correction_mode = config.correction_mode

    def make_cache_folder(self):
        self.cache_folder = os.path.join(TEMP_ROOT_PATH, 'ocr_cache')
        os.makedirs(self.cache_folder, exist_ok=True)
        self.preprocess_cache = os.path.join(
            self.cache_folder, "preprocessed.jpg")
        self.detection_cache = os.path.join(self.cache_folder, "detected.jpg")
        self.crop_cache = os.path.join(self.cache_folder, 'crops')
        self.final_output = os.path.join(TEMP_ROOT_PATH, 'result.jpg')
        self.retr_output = os.path.join(TEMP_ROOT_PATH, 'result.txt')

    def init_modules(self):
        # self.det_model = Detection(
        #     config_path=self.det_config,
        #     weight_path=self.det_weight)
        
        self.det_model = MMOCRInferencer(det='DBNet', device='cuda:0')
        self.ocr_model = OCR(
            config_path=self.ocr_config,
            weight_path=self.ocr_weight)
        self.preproc = Preprocess(
            det_model=self.det_model,
            ocr_model=self.ocr_model,
            find_best_rotation=self.find_best_rotation)

        if self.dictionary_path is not None:
            self.dictionary = {}
            df = pd.read_csv(self.dictionary_path)
            for id, row in df.iterrows():
                self.dictionary[row.text.lower()] = row.lbl
        else:
            self.dictionary = None

        self.correction = Correction(
            dictionary=self.dictionary,
            mode=self.correction_mode)

        if self.do_retrieve:
            self.retrieval = Retrieval(
                self.class_mapping,
                dictionary=self.dictionary,
                mode=self.retr_mode,
                bert_weight=self.bert_weight)

    def tracking_data(self, img):
        # Document extraction
        # img1 = self.preproc(img)
        start_time = time.time()
        print("Starting detect boxes: ")
        det_results = self.det_model(img, show=False)
        det_polygons = det_results["predictions"][0]['det_polygons']
        boxes = []
       
        det_polygons_sorted =  mmocr.utils.sort_points(det_polygons)
        for polygon in det_polygons_sorted:
            bbox = mmocr.utils.poly2bbox(polygon)
            boxes.append(bbox)

        boxes = self.sort_boxes(boxes)
        
        if self.cache_folder is None:
            assert self.cache_folder, "Please specify output_path"
        else:
            output_path_crop = os.path.join(self.cache_folder, 'crops')
            if os.path.exists(output_path_crop):
                shutil.rmtree(output_path_crop)
                os.mkdir(output_path_crop)
        
        print("Drawing and croppng image...")
        img1 = self.draw_bbox(img, boxes)
        
        self.crop_box(img, boxes, output_path_crop)

        saved_img = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.preprocess_cache, saved_img)

        # boxes, img2 = self.det_model(
        #     img,
        #     crop_region=True,
        #     return_result=True,
        #     output_path=self.cache_folder)
        # saved_img = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
        # cv2.imwrite(self.detection_cache, saved_img)
        # else:
        #     boxes = self.det_model(
        #         img,
        #         crop_region=True,
        #         return_result=False,
        #         output_path=self.cache_folder)

        img_paths = os.listdir(self.crop_cache)
        img_paths.sort(key=natural_keys)
        img_paths = [os.path.join(self.crop_cache, i) for i in img_paths]

        print("OCR... ")
        texts = self.ocr_model.predict_folder(img_paths, return_probs=False)
        texts = self.correction(texts, return_score=False)

        if self.do_retrieve:
            preds, probs = self.retrieval(texts)
        else:
            preds, probs = None, None

        visualize(
            img1, boxes, texts,
            img_name=self.final_output,
            class_mapping=self.class_mapping,
            labels=preds, probs=probs,
            visualize_best=self.do_retrieve)
        end_time = time.time()
        print("Time inference: ", end_time - start_time)
        return self.final_output, texts
    def draw_bbox(self, img_path, result, color=(255, 0, 0), thickness=2):
        if isinstance(img_path, str):
            img = cv2.imread(img_path)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img = img_path.copy()
        
        for box in result:
            box = box.astype(int)
            # Define points as top-left, top-right, bottom-right, bottom-left
            tl, tr, br, bl = (box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])
            
            # Draw lines between the points
            cv2.line(img, tl, tr, color, thickness)
            cv2.line(img, tr, br, color, thickness)
            cv2.line(img, br, bl, color, thickness)
            cv2.line(img, bl, tl, color, thickness)
            
        return img
    
    def sort_boxes(self, boxes):
        # First, sort by the top y-coordinate to ensure we process top-to-bottom
        boxes_sorted_by_y = sorted(boxes, key=lambda box: box[1])
        
        # Now, sort each line by the x-coordinate
        sorted_boxes = []
        current_line = []
        line_threshold = 10  # Threshold to consider boxes are in the same line
        
        for box in boxes_sorted_by_y:
            if not current_line:
                current_line.append(box)
            else:
                # If the vertical distance between boxes is small enough, consider them as the same line
                if abs(box[1] - current_line[-1][1]) <= line_threshold:
                    current_line.append(box)
                else:
                    # Sort the current line by x-coordinate and add to the sorted list, then start a new line
                    sorted_boxes.extend(sorted(current_line, key=lambda box: box[0]))
                    current_line = [box]
        
        # Don't forget to add the last line after sorting
        sorted_boxes.extend(sorted(current_line, key=lambda box: box[0]))

        return sorted_boxes
    
    def crop_box(self, img, boxes, out_folder, sort=True):
        h, w, c = img.shape

        # Ensure the output folder exists
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        for i, box in enumerate(boxes):
            box_name = os.path.join(out_folder, f"{i}.png")

            # Convert box coordinates to integers and ensure they are within image dimensions
            x_min, y_min, x_max, y_max = box.astype(int)
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(w, x_max)
            y_max = min(h, y_max)

            # Crop the image based on the box coordinates
            cropped_img = img[y_min:y_max, x_min:x_max]

            # Save the cropped image
            try:
                cv2.imwrite(box_name, cropped_img)
            except Exception as e:
                print(f"Error saving {box_name}: {e}")

        return boxes

    
    
app_scanner = APP_SCANNER(config)

