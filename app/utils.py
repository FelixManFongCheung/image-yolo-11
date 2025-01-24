def process_yolo_results(results):
    """
    Process YOLO results to get normalized coordinates, distances, and detection info
    
    Args:
        results: YOLO results object
    
    Returns:
        dict: Processed detection information including:
            - normalized coordinates (0-1 scale)
            - relative distances between detections
            - confidence scores
            - labels
            - image dimensions
    """
    processed_results = []
    
    for result in results:
        # Get image dimensions
        img_height, img_width = result.orig_shape
        boxes = result.boxes
        
        # Process each detection
        detections = []
        for box in boxes:
            # Get box coordinates and convert to list
            xyxy = box.xyxy.tolist()[0]
            
            # Normalize coordinates to 0-1 scale
            normalized_coords = {
                'x1': xyxy[0] / img_width,
                'y1': xyxy[1] / img_height,
                'x2': xyxy[2] / img_width,
                'y2': xyxy[3] / img_height
            }
            
            # Calculate center point
            center_x = (normalized_coords['x1'] + normalized_coords['x2']) / 2
            center_y = (normalized_coords['y1'] + normalized_coords['y2']) / 2
            
            # Calculate box dimensions
            width = normalized_coords['x2'] - normalized_coords['x1']
            height = normalized_coords['y2'] - normalized_coords['y1']
            
            detection = {
                'coordinates': {
                    'normalized': normalized_coords,
                    'original': {
                        'x1': int(xyxy[0]),
                        'y1': int(xyxy[1]),
                        'x2': int(xyxy[2]),
                        'y2': int(xyxy[3])
                    }
                },
                'center': {
                    'x': center_x,
                    'y': center_y
                },
                'dimensions': {
                    'width': width,
                    'height': height
                },
                'confidence': float(box.conf),
                'class_id': int(box.cls),
                'label': result.names[int(box.cls)]
            }
            detections.append(detection)
        
        # Calculate relative distances between all detections
        distances = []
        for i, det1 in enumerate(detections):
            for j, det2 in enumerate(detections):
                if i < j:  # avoid duplicate distances
                    distance = {
                        'between': [det1['label'], det2['label']],
                        'distance': {
                            'x': abs(det1['center']['x'] - det2['center']['x']),
                            'y': abs(det1['center']['y'] - det2['center']['y']),
                            'euclidean': ((det1['center']['x'] - det2['center']['x'])**2 + 
                                        (det1['center']['y'] - det2['center']['y'])**2)**0.5
                        }
                    }
                    distances.append(distance)
        
        processed_results.append({
            'image_dimensions': {
                'width': img_width,
                'height': img_height
            },
            'detections': detections,
            'relative_distances': distances
        })
    
    return processed_results