from ultralytics import YOLO
import cv2
import json
import time
from datetime import datetime
import numpy as np
from pathlib import Path
import requests
from typing import Dict, List, Optional

class ObjectDetector:
    def __init__(self, 
                 model_path: str = "yolov8n.pt",
                 confidence_threshold: float = 0.5,
                 target_class: str = "chair"):
        
        # Initialize YOLO model
        self.model = YOLO(model_path)
        self.conf_threshold = confidence_threshold
        self.target_class = target_class
        
        # Initialize video capture (0 is usually the default camera)
        self.cap = cv2.VideoCapture(0)
        
        # Ensure camera is set to a reasonable resolution for RPi
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def generate_military_packet(self, 
                               detections: List[Dict], 
                               frame_shape: tuple) -> dict:
        """Generate military packet from detections"""
        
        # Calculate center of the detected object
        if detections:
            # Use the first detected chair for this example
            detection = detections[0]
            x_center = (detection['x1'] + detection['x2']) / 2
            y_center = (detection['y1'] + detection['y2']) / 2
            
            # Normalize coordinates to 0-1 range
            x_norm = x_center / frame_shape[1]
            y_norm = y_center / frame_shape[0]
            
            return {
                "action": f"DETECT_{self.target_class.upper()}",
                "target_units": ["SecurityCamera_1"],
                "coordinates": {
                    "x": float(x_norm),
                    "y": float(y_norm)
                },
                "timeframe": datetime.utcnow().strftime("%H%MZ"),
                "priority": "LOW"
            }
        return None

    def process_frame(self, frame: np.ndarray) -> List[Dict]:
        """Process a single frame and return detections"""
        results = self.model(frame)[0]
        detections = []
        
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            if score > self.conf_threshold and \
               results.names[int(class_id)].lower() == self.target_class.lower():
                detections.append({
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'score': score,
                    'class_id': class_id
                })
        return detections

    def run(self, api_endpoint: Optional[str] = None):
        """Main detection loop"""
        print("Starting detection... Press 'q' to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Process frame
            detections = self.process_frame(frame)
            
            # Generate and send packet if chair is detected
            if detections:
                packet = self.generate_military_packet(detections, frame.shape)
                print(f"Detection: {json.dumps(packet, indent=2)}")
                
                # Send to API if endpoint is provided
                if api_endpoint:
                    try:
                        requests.post(api_endpoint, json=packet)
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to send packet: {e}")

            # Draw detection boxes
            for det in detections:
                cv2.rectangle(frame, 
                            (int(det['x1']), int(det['y1'])), 
                            (int(det['x2']), int(det['y2'])), 
                            (0, 255, 0), 2)
                
            # Display frame
            cv2.imshow('Object Detection', frame)
            
            # Break loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create detector instance
    detector = ObjectDetector(
        model_path="yolov8n.pt",  # Using the smallest YOLOv8 model
        confidence_threshold=0.5,
        target_class="chair"
    )
    
    # Run detection (optionally specify API endpoint)
    detector.run(api_endpoint=None)