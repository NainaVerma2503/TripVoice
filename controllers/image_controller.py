from flask import Blueprint, send_from_directory, jsonify
import os

image_bp = Blueprint('image', __name__)

@image_bp.route('/images/<category>/<filename>')
def serve_image(category, filename):
    """
    Serve images from the images directory
    """
    try:
        # Validate category to prevent directory traversal
        valid_categories = ['flights', 'hotels', 'airlines', 'amenities', 'packages']
        if category not in valid_categories:
            return jsonify({"error": "Invalid category"}), 400
        
        # Serve image from the appropriate directory
        image_path = os.path.join('images', category)
        return send_from_directory(image_path, filename)
        
    except Exception as e:
        return jsonify({"error": f"Image not found: {str(e)}"}), 404

@image_bp.route('/api/images/list')
def list_images():
    """
    List all available images
    """
    try:
        images = {}
        base_path = 'images'
        
        if not os.path.exists(base_path):
            return jsonify({"error": "Images directory not found"}), 404
        
        for category in os.listdir(base_path):
            category_path = os.path.join(base_path, category)
            if os.path.isdir(category_path):
                images[category] = []
                for filename in os.listdir(category_path):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        images[category].append(filename)
        
        return jsonify({
            "status": "success",
            "images": images
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
