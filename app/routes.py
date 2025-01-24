from flask import Blueprint, request, jsonify
from . import supabase_client
from .model import ModelSingleton
from .utils import process_yolo_results
from PIL import Image
import io
import base64

main = Blueprint('main', __name__)

@main.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        image_id = data.get('image_id')
        
        response = supabase_client.table('images').select('data').eq('id', image_id).execute()
        
        hex_string = response.data[0]['data']
        
         # Convert hex string to bytes
        hex_string = hex_string.replace('\\x', '').replace(' ', '')
        image_bytes = bytes.fromhex(hex_string)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Run inference with the YOLO11n model on the 'bus.jpg' image
        model = ModelSingleton.get_instance().get_model()
        results = model(image)
        
         # Plot the results on the image
        plotted_image = results[0].plot()  # Returns a numpy array
        
        # Convert numpy array to bytes
        plotted_image_bytes = io.BytesIO()
        Image.fromarray(plotted_image).save(plotted_image_bytes, format='JPEG')
        plotted_image_bytes = plotted_image_bytes.getvalue()
            
        return jsonify({
            'status': 'success',
            'message': 'Image processed successfully',
            'results': process_yolo_results(results),
            'plotted_image': base64.b64encode(plotted_image_bytes).decode('utf-8')  # Convert to base64 string

        })
        
    except Exception as e:
        print(f"Error in detect route: {e}")
        return jsonify({'error': str(e)}), 500