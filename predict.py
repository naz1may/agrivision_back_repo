#!/usr/bin/env python3
"""Apple Leaf Disease Detection - Analysis API"""

# Disable NNPACK before importing PyTorch
import os
os.environ['NNPACK_DISABLE'] = '1'  # Disable NNPACK entirely
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['PYTHONWARNINGS'] = 'ignore'

import warnings
warnings.filterwarnings('ignore')

import torch
from torchvision import transforms, models
from PIL import Image
import torch.nn as nn
import json
import sys

# ----- Configuration -----
MODEL_PATH = "apple_disease_model.pth"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
IMG_SIZE = 224  # Should match training size

# Pattern labels mapping
PATTERN_LABELS = {
    "healthy": "healthy",
    "scab": "scab",
    "rust": "rust",
    "powdery_mildew": "powdery_mildew",
    "frog_eye_leaf_spot": "frog_eye_leaf_spot",
    "scab_frog_eye_leaf_spot": "scab frog_eye_leaf_spot",
    "scab_frog_eye_leaf_spot_complex": "scab frog_eye_leaf_spot complex",
    "rust_frog_eye_leaf_spot": "rust frog_eye_leaf_spot",
    "rust_complex": "rust complex",
    "frog_eye_leaf_spot_complex": "frog_eye_leaf_spot complex",
    "powdery_mildew_complex": "powdery_mildew complex",
    "complex": "complex"
}

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_model():
    """Load trained model"""
    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)
    class_names = checkpoint.get('class_names', [])
    num_classes = len(class_names)
    
    model = models.mobilenet_v2()
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(DEVICE)
    model.eval()
    
    return model, class_names

def normalize_class_name(class_name):
    """Normalize class name"""
    return class_name.lower().replace(" ", "_").replace("-", "_")

def predict_single_image(image_path, model, class_names):
    """
    Predict disease for single image
    
    Returns:
        dict: {"label": str, "confidence": float, "visual_status": str}
    """
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        return {
            "label": "error",
            "confidence": 0.0,
            "visual_status": "error",
            "error": str(e)
        }
    
    img_tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        
    confidence, class_idx = torch.max(probabilities, 0)
    predicted_class = class_names[class_idx.item()]
    confidence_value = confidence.item()
    
    normalized_class = normalize_class_name(predicted_class)
    is_healthy = normalized_class == "healthy"
    visual_status = "healthy" if is_healthy else "diseased"
    pattern_label = PATTERN_LABELS.get(normalized_class, normalized_class)
    
    return {
        "label": pattern_label,
        "confidence": round(confidence_value, 4),
        "visual_status": visual_status
    }

def analyze(images_dir="./images_for_analysis"):
    """
    Analyze all images in specified directory
    
    Args:
        images_dir: Path to directory with images (default: ./images_for_analysis)
    
    Returns:
        list: List of dicts, one per image with format:
              [
                {
                  "filename": "image1.jpg",
                  "label": "scab",
                  "confidence": 0.9234,
                  "visual_status": "diseased"
                },
                ...
              ]
    
    Usage:
        # As standalone
        python predict.py
        
        # In your code
        from predict import analyze
        results = analyze("path/to/images")
        for result in results:
            print(result['label'], result['confidence'])
    """
    # Load model once
    model, class_names = load_model()
    
    # Get all image files
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    if not os.path.exists(images_dir):
        return {"error": f"Directory not found: {images_dir}"}
    
    image_files = [
        f for f in os.listdir(images_dir) 
        if os.path.splitext(f.lower())[1] in valid_extensions
    ]
    
    if not image_files:
        return {"error": f"No images found in {images_dir}"}
    
    # Process all images
    results = []
    for filename in image_files:
        image_path = os.path.join(images_dir, filename)
        prediction = predict_single_image(image_path, model, class_names)
        
        # Add filename to result
        result = {
            "filename": filename,
            **prediction
        }
        results.append(result)
    
    return results

def check_quality(images_dir="./images_for_analysis", csv_path="./dataset/train.csv"):
    """
    Check prediction quality against ground truth CSV
    
    Args:
        images_dir: Directory with images
        csv_path: CSV file with ground truth labels
    
    Returns:
        dict: Statistics about predictions
    
    Usage:
        python predict.py --check_quality
    """
    import pandas as pd
    
    # Load ground truth
    if not os.path.exists(csv_path):
        return {"error": f"CSV not found: {csv_path}"}
    
    df = pd.read_csv(csv_path)
    df['image'] = df['image'].str.strip()
    df['labels'] = df['labels'].str.strip()
    ground_truth = dict(zip(df['image'], df['labels']))
    
    # Get predictions
    results = analyze(images_dir)
    
    if isinstance(results, dict) and "error" in results:
        return results
    
    # Calculate statistics
    total = 0
    correct = 0
    class_correct = {}
    class_total = {}
    confusion_matrix = {}
    
    for result in results:
        filename = result['filename']
        
        if filename not in ground_truth:
            continue
            
        total += 1
        true_label = ground_truth[filename]
        pred_label = result['label']
        
        # Normalize for comparison
        true_norm = normalize_class_name(true_label)
        pred_norm = normalize_class_name(pred_label)
        
        is_correct = (true_norm == pred_norm)
        
        if is_correct:
            correct += 1
        
        # Per-class stats
        if true_label not in class_total:
            class_total[true_label] = 0
            class_correct[true_label] = 0
        
        class_total[true_label] += 1
        if is_correct:
            class_correct[true_label] += 1
        
        # Confusion matrix
        if true_label not in confusion_matrix:
            confusion_matrix[true_label] = {}
        if pred_label not in confusion_matrix[true_label]:
            confusion_matrix[true_label][pred_label] = 0
        confusion_matrix[true_label][pred_label] += 1
    
    # Build per-class accuracy
    per_class_accuracy = {}
    for class_name in sorted(class_total.keys()):
        acc = (class_correct[class_name] / class_total[class_name]) * 100
        per_class_accuracy[class_name] = {
            "correct": class_correct[class_name],
            "total": class_total[class_name],
            "accuracy": round(acc, 2)
        }
    
    # Find top misclassifications
    misclassifications = []
    for true_class in confusion_matrix:
        for pred_class in confusion_matrix[true_class]:
            if true_class != pred_class:
                count = confusion_matrix[true_class][pred_class]
                misclassifications.append({
                    "true_label": true_class,
                    "predicted_as": pred_class,
                    "count": count
                })
    
    misclassifications.sort(key=lambda x: x['count'], reverse=True)
    
    # Build quality report
    quality_report = {
        "total_images": total,
        "correct_predictions": correct,
        "incorrect_predictions": total - correct,
        "overall_accuracy": round((correct / total * 100) if total > 0 else 0, 2),
        "per_class_accuracy": per_class_accuracy,
        "top_misclassifications": misclassifications[:10]
    }
    
    return quality_report

def main():
    """Command-line interface"""
    
    if "--check_quality" in sys.argv:
        # Quality check mode
        images_dir = "./images_for_analysis"
        
        # Allow custom directory
        if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
            images_dir = sys.argv[2]
        
        quality = check_quality(images_dir)
        print(json.dumps(quality, indent=2))
    
    elif "--help" in sys.argv or "-h" in sys.argv:
        print("""
Apple Leaf Disease Detection API

Usage:
  python predict.py                    # Analyze images in ./images_for_analysis/
  python predict.py --check_quality    # Check quality against CSV
  
Returns JSON format:
  Normal mode: List of predictions for each image
  Quality mode: Statistics and accuracy report

Example in Python code:
  from predict import analyze
  results = analyze("./images_for_analysis")
  for result in results:
      print(f"{result['filename']}: {result['label']} ({result['confidence']:.2%})")
""")
    
    else:
        # Normal analysis mode - output pure JSON
        images_dir = "./images_for_analysis"
        
        # Allow custom directory
        if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
            images_dir = sys.argv[1]
        
        results = analyze(images_dir)
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()