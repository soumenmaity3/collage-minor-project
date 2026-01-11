# ============================================================
# app.py - Streamlit Frontend for MedPredictAI
# ============================================================

import os
import json
import streamlit as st
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms

# ============================================================
# 1. GLOBAL TRANSFORMS (Pre-compiled for speed)
# ============================================================

BRAIN_TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

XRAY_TRANSFORM = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# ============================================================
# 2. MODEL LOADING HELPERS
# ============================================================

@st.cache_resource
def load_brain_model(model_path, num_classes):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet50(weights='IMAGENET1K_V1')
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    model = model.to(device)
    model.eval()
    torch.set_grad_enabled(False)
    return model, device

@st.cache_resource
def load_xray_model(model_path, num_classes):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.densenet121(weights='IMAGENET1K_V1')
    model.classifier = nn.Linear(model.classifier.in_features, num_classes)

    state_dict = torch.load(model_path, map_location=device, weights_only=True)
    state_dict.pop('classifier.weight', None)
    state_dict.pop('classifier.bias', None)

    model.load_state_dict(state_dict, strict=False)
    model = model.to(device)
    model.eval()
    torch.set_grad_enabled(False)
    return model, device

# ============================================================
# 3. PREDICTION FUNCTIONS
# ============================================================

def predict_brain_image(model, image, device):
    image_tensor = BRAIN_TRANSFORM(image.convert('RGB')).unsqueeze(0).to(device)
    with torch.inference_mode():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)

    predicted_idx = predicted_idx.item()
    confidence_score = float(confidence.item() * 100)
    probs_cpu = probabilities.cpu().numpy().flatten()

    predicted_label = 'Tumor Detected' if predicted_idx == 0 else 'No Tumor Detected'
    probabilities_dict = {
        'Tumor Present': float(probs_cpu[0] * 100),
        'No Tumor': float(probs_cpu[1] * 100)
    }

    return {
        'prediction': predicted_label,
        'confidence': confidence_score,
        'probabilities': probabilities_dict
    }

def predict_xray_image(model, image, device, class_names, threshold=0.25):
    image_tensor = XRAY_TRANSFORM(image).unsqueeze(0).to(device)
    with torch.inference_mode():
        outputs = model(image_tensor)
        probs = torch.sigmoid(outputs).cpu().numpy().flatten()

    predictions = [class_names[i] for i, p in enumerate(probs) if p > threshold]
    if not predictions:
        predictions = ["No Findings Detected"]

    probabilities_dict = {class_names[i]: float(probs[i] * 100)
                          for i in range(len(class_names))}

    return {
        'predictions': predictions,
        'probabilities': probabilities_dict
    }

# ============================================================
# 4. LOAD MODELS
# ============================================================

model_folder = os.path.dirname(os.path.abspath(__file__))

brain_model_path = os.path.join(model_folder, 'best_brain_model.pth')
brain_classes_path = os.path.join(model_folder, 'brain_class_names.json')
with open(brain_classes_path, 'r') as f:
    brain_class_names = json.load(f)
brain_model, brain_device = load_brain_model(brain_model_path, len(brain_class_names))

xray_model_path = os.path.join(model_folder, 'best_xray_model.pth')
xray_classes_path = os.path.join(model_folder, 'xray_class_names.json')
with open(xray_classes_path, 'r') as f:
    xray_class_names = json.load(f)
xray_model, xray_device = load_xray_model(xray_model_path, len(xray_class_names))

# ============================================================
# 5. STREAMLIT APP
# ============================================================

st.title("🩺 MedPredictAI - Brain & Chest Predictor")
st.markdown("Upload an image to get predictions for brain tumors or chest X-ray abnormalities.")

model_type = st.selectbox("Select Model Type", ["brain", "xray"])

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.button("Predict"):
        with st.spinner("Analyzing..."):
            if model_type == 'brain':
                result = predict_brain_image(brain_model, image, brain_device)
                st.success(f"Prediction: {result['prediction']}")
                st.write(f"Confidence: {result['confidence']:.2f}%")
                st.bar_chart(result['probabilities'])
            elif model_type == 'xray':
                result = predict_xray_image(xray_model, image, xray_device, xray_class_names)
                st.success(f"Predictions: {', '.join(result['predictions'])}")
                st.bar_chart(result['probabilities'])