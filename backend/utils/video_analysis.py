import cv2
import os

def analyze_video(file_path, anomaly_threshold=30):
    """Analyze a video for metadata and frame-level anomalies."""
    try:
        # Capture video
        video = cv2.VideoCapture(file_path)
        if not video.isOpened():
            return {"error": "Failed to open video file"}

        # Extract metadata
        metadata = {
            "frame_count": int(video.get(cv2.CAP_PROP_FRAME_COUNT)),
            "fps": video.get(cv2.CAP_PROP_FPS),
            "resolution": f"{int(video.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))}",
            "duration": int(video.get(cv2.CAP_PROP_FRAME_COUNT)) / video.get(cv2.CAP_PROP_FPS),
        }

        frame_index = 0
        anomalies = []
        prev_frame = None

        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Convert to grayscale for better anomaly detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_frame is not None:
                # Calculate the absolute difference between the current and previous frames
                frame_diff = cv2.absdiff(prev_frame, gray_frame)
                # Compute the sum of pixel differences to determine if the change is significant
                diff_sum = frame_diff.sum()

                # If the difference exceeds the threshold, consider it an anomaly
                if diff_sum > anomaly_threshold:
                    anomalies.append(f"Anomaly detected at frame {frame_index} (diff_sum: {diff_sum})")

            prev_frame = gray_frame
            frame_index += 1

        video.release()

        # Return the analysis result
        return {
            "metadata": metadata,
            "anomalies": anomalies,
            "message": "Video analysis completed successfully."
        }
    except Exception as e:
        return {"error": str(e)}

