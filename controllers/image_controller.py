from flask import Blueprint, send_from_directory, jsonify
import os

image_bp = Blueprint('image', __name__)

# Image directory path
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

@image_bp.route('/images/<category>/<filename>')
def serve_image(category, filename):
    """
    Serve images from the local images directory
    """
    try:
        image_path = os.path.join(IMAGES_DIR, category)
        return send_from_directory(image_path, filename)
    except Exception as e:
        return jsonify({'error': f'Image not found: {str(e)}'}), 404

@image_bp.route('/api/images/list')
def list_images():
    """
    List all available images in the project
    """
    try:
        images = {}
        for category in os.listdir(IMAGES_DIR):
            category_path = os.path.join(IMAGES_DIR, category)
            if os.path.isdir(category_path):
                images[category] = os.listdir(category_path)
        
        return jsonify({
            'status': 'success',
            'images': images,
            'base_url': '/images'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
