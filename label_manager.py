import os
import shutil
from typing import List, Tuple, Optional, Dict
from PyQt5.QtCore import QPointF
from utils import load_yolo_labels, save_yolo_labels
from shape import Shape

class LabelManager:
    """
    Manages the loading, saving, and state of labels for the Active Learning Tool.
    Handles the logic between source labels and temporary (edited) labels.
    """
    def __init__(self, temp_dir: str):
        self.temp_dir = temp_dir
        self.source_label_dir: Optional[str] = None
        self.class_names: List[str] = []
        
        # Ensure temp directory exists
        self.temp_labels_dir = os.path.join(self.temp_dir, "labels")
        os.makedirs(self.temp_labels_dir, exist_ok=True)

    def set_class_names(self, names: List[str]):
        self.class_names = names

    def set_source_label_dir(self, path: Optional[str]):
        self.source_label_dir = path

    def clear_temp_labels(self):
        """Removes all files in the temporary labels directory."""
        if os.path.exists(self.temp_labels_dir):
            shutil.rmtree(self.temp_labels_dir)
            os.makedirs(self.temp_labels_dir, exist_ok=True)

    def get_label_path(self, img_path: str) -> Tuple[Optional[str], bool]:
        """
        Determines the path to the label file for a given image.
        Prioritizes the temporary directory over the source directory.
        
        Returns:
            Tuple[Optional[str], bool]: (Path to label file, is_temporary)
        """
        txt_filename = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
        temp_path = os.path.join(self.temp_labels_dir, txt_filename)
        
        if os.path.exists(temp_path):
            return temp_path, True
            
        if self.source_label_dir:
            source_path = os.path.join(self.source_label_dir, txt_filename)
            if os.path.exists(source_path):
                return source_path, False
                
        return None, False

    def load_labels(self, img_path: str, img_dims: Tuple[int, int]) -> List[Shape]:
        """Loads labels for a specific image."""
        if not self.class_names:
            return []

        img_w, img_h = img_dims
        label_path, _ = self.get_label_path(img_path)
        
        if label_path:
            try:
                return load_yolo_labels(label_path, img_w, img_h, self.class_names)
            except Exception as e:
                print(f"Error loading labels from {label_path}: {e}")
                return []
        return []

    def save_labels(self, img_path: str, shapes: List[Shape], img_dims: Tuple[int, int]):
        """Saves the current shapes to the temporary directory."""
        if not self.class_names:
            return

        img_w, img_h = img_dims
        txt_filename = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
        save_path = os.path.join(self.temp_labels_dir, txt_filename)
        
        try:
            save_yolo_labels(save_path, shapes, img_w, img_h, self.class_names)
        except Exception as e:
            print(f"Error saving labels to {save_path}: {e}")

    def delete_label(self, img_path: str):
        """Deletes the label file associated with the image from both temp and source."""
        txt_filename = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
        
        # Delete from temp
        temp_path = os.path.join(self.temp_labels_dir, txt_filename)
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError as e:
                print(f"Error removing temp label {temp_path}: {e}")

        # Delete from source
        if self.source_label_dir:
            source_path = os.path.join(self.source_label_dir, txt_filename)
            if os.path.exists(source_path):
                try:
                    os.remove(source_path)
                except OSError as e:
                    print(f"Error removing source label {source_path}: {e}")

    def import_labels_from_dir(self, source_dir: str, image_paths: List[str]):
        """
        imports labels from a directory. Currently just sets the source dir,
        but implies clearing temp if a fresh 'upload' is desired (handled by caller typically).
        """
        self.set_source_label_dir(source_dir)

    def export_labels(self, dest_dir: str, image_paths: List[Tuple[str, Tuple[int, int]]], filter_classes: Optional[List[str]] = None) -> int:
        """
        Exports labels to a destination directory, optionally filtering classes.
        Returns the number of exported files.
        """
        os.makedirs(dest_dir, exist_ok=True)
        count = 0
        
        export_classes = filter_classes if filter_classes is not None else self.class_names

        for img_path, (img_w, img_h) in image_paths:
            # Load shapes (from temp or source)
            shapes = self.load_labels(img_path, (img_w, img_h))
            
            # Filter
            shapes_to_export = [s for s in shapes if s.label in export_classes]
            
            if shapes_to_export:
                txt_filename = os.path.splitext(os.path.basename(img_path))[0] + ".txt"
                dest_path = os.path.join(dest_dir, txt_filename)
                save_yolo_labels(dest_path, shapes_to_export, img_w, img_h, export_classes)
                count += 1
                
        return count
