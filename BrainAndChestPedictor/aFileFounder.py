"""
Model File Checker and Path Configuration
Run this first to find your model files and update paths
"""

import os
import json

def find_files(filename, search_path='.'):
    """Search for files in directory and subdirectories."""
    results = []
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            results.append(os.path.join(root, filename))
    return results

def check_current_directory():
    """Check what files are in the current directory."""
    print("=" * 60)
    print("📂 CURRENT DIRECTORY CONTENTS")
    print("=" * 60)
    current_dir = os.getcwd()
    print(f"Current Directory: {current_dir}\n")
    
    files = os.listdir(current_dir)
    print("Files found:")
    for f in files:
        if os.path.isfile(f):
            size = os.path.getsize(f) / (1024*1024)  # MB
            print(f"  ✓ {f} ({size:.2f} MB)")
        else:
            print(f"  📁 {f}/")
    print()

def search_for_models():
    """Search for model files in current and parent directories."""
    print("=" * 60)
    print("🔍 SEARCHING FOR MODEL FILES")
    print("=" * 60)
    
    required_files = [
        'best_brain_model.pth',
        'brain_class_names.json',
        'best_xray_model.pth',
        'xray_class_names.json'
    ]
    
    found_files = {}
    
    for filename in required_files:
        print(f"\nSearching for: {filename}")
        results = find_files(filename, '.')
        
        if results:
            print(f"  ✅ Found at:")
            for path in results:
                print(f"     {os.path.abspath(path)}")
            found_files[filename] = os.path.abspath(results[0])
        else:
            print(f"  ❌ Not found in current directory tree")
            found_files[filename] = None
    
    return found_files

def check_from_screenshot_path():
    """Check the path from your screenshot."""
    screenshot_path = r"C:\Users\sm803\OneDrive\Desktop\Data Science\BrainAndChestPedictor"
    
    print("\n" + "=" * 60)
    print("📸 CHECKING PATH FROM YOUR SCREENSHOT")
    print("=" * 60)
    print(f"Path: {screenshot_path}\n")
    
    if os.path.exists(screenshot_path):
        print("✅ Directory exists!")
        print("\nFiles in this directory:")
        try:
            files = os.listdir(screenshot_path)
            for f in files:
                full_path = os.path.join(screenshot_path, f)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path) / (1024*1024)
                    print(f"  ✓ {f} ({size:.2f} MB)")
                else:
                    print(f"  📁 {f}/")
        except PermissionError:
            print("  ⚠️  Permission denied")
    else:
        print("❌ Directory not found")
    
    return screenshot_path

def create_updated_app_config(found_files):
    """Create configuration with correct paths."""
    print("\n" + "=" * 60)
    print("⚙️  CONFIGURATION")
    print("=" * 60)
    
    config = {}
    all_found = True
    
    for filename, path in found_files.items():
        if path:
            config[filename] = path
            print(f"✅ {filename}")
            print(f"   → {path}")
        else:
            print(f"❌ {filename} - NOT FOUND")
            all_found = False
    
    if all_found:
        print("\n✅ All files found! You can proceed with the API.")
        return config
    else:
        print("\n⚠️  Some files are missing. Please locate them first.")
        return None

def generate_updated_app():
    """Generate app.py with absolute paths."""
    print("\n" + "=" * 60)
    print("📝 GENERATING UPDATED APP.PY")
    print("=" * 60)
    
    # From your screenshot, use this base path
    base_path = r"C:\Users\sm803\OneDrive\Desktop\Data Science\BrainAndChestPedictor"
    
    code = f'''"""
FastAPI Backend with ABSOLUTE PATHS for your setup
"""

import os
import json
import io
from typing import Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# =============================================================================
# ABSOLUTE PATHS - UPDATE THESE TO YOUR ACTUAL PATHS
# =============================================================================

BASE_PATH = r"{base_path}"

MODEL_PATHS = {{
    'brain_model': os.path.join(BASE_PATH, 'best_brain_model.pth'),
    'brain_classes': os.path.join(BASE_PATH, 'brain_class_names.json'),
    'xray_model': os.path.join(BASE_PATH, 'best_xray_model.pth'),
    'xray_classes': os.path.join(BASE_PATH, 'xray_class_names.json')
}}

# Rest of the app code remains the same...
'''
    
    print(f"Base path set to: {base_path}")
    print("\nSave this configuration to your app.py file")
    
    return code

def main():
    """Main diagnostic function."""
    print("\n" + "=" * 70)
    print(" " * 15 + "🏥 MODEL FILE DIAGNOSTIC TOOL")
    print("=" * 70 + "\n")
    
    # Step 1: Check current directory
    check_current_directory()
    
    # Step 2: Search for models
    found_files = search_for_models()
    
    # Step 3: Check screenshot path
    screenshot_path = check_from_screenshot_path()
    
    # Step 4: Create config
    config = create_updated_app_config(found_files)
    
    # Step 5: Recommendations
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if config:
        print("""
1. ✅ All files found! 
2. Copy the model files to the same directory as app.py
3. Or update app.py with the paths shown above
        """)
    else:
        print(f"""
1. Navigate to: {screenshot_path}
2. Check if these files exist:
   - best_brain_model.pth
   - brain_class_names.json
   - best_xray_model.pth
   - xray_class_names.json

3. Either:
   Option A: Copy all files to where app.py is
   Option B: Update app.py with absolute paths (see below)
        """)
    
    # Generate updated app
    print("\n" + "=" * 60)
    print("🔧 QUICK FIX OPTIONS")
    print("=" * 60)
    print("""
OPTION 1: Copy files to app.py directory
-----------------------------------------
cd "C:\\Users\\sm803\\OneDrive\\Desktop\\Data Science\\BrainAndChestPedictor"
# Then copy all .pth and .json files to where app.py is

OPTION 2: Use absolute paths in app.py
---------------------------------------
Update the paths in app.py's initialize_models() function:

brain_model_path = r'C:\\Users\\sm803\\OneDrive\\Desktop\\Data Science\\BrainAndChestPedictor\\best_brain_model.pth'
brain_classes_path = r'C:\\Users\\sm803\\OneDrive\\Desktop\\Data Science\\BrainAndChestPedictor\\brain_class_names.json'
xray_model_path = r'C:\\Users\\sm803\\OneDrive\\Desktop\\Data Science\\BrainAndChestPedictor\\best_xray_model.pth'
xray_classes_path = r'C:\\Users\\sm803\\OneDrive\\Desktop\\Data Science\\BrainAndChestPedictor\\xray_class_names.json'
    """)

if __name__ == "__main__":
    main()