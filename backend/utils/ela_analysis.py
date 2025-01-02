import cv2
import os
import tempfile

def error_level_analysis(image_path, threshold=30, jpeg_quality=95):
    """Perform Error Level Analysis (ELA) on an image."""
    try:
        # Read the original image
        original = cv2.imread(image_path)
        if original is None:
            return {"error": "Invalid image file"}

        # Create a temporary file to save the recompressed image
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_path = temp_file.name
            cv2.imwrite(temp_path, original, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])

        # Reload the recompressed image
        recompressed = cv2.imread(temp_path)

        # Calculate the difference
        ela = cv2.absdiff(original, recompressed)

        # Convert the difference image to grayscale
        ela = cv2.cvtColor(ela, cv2.COLOR_BGR2GRAY)

        # Apply a threshold to highlight the differences
        _, ela = cv2.threshold(ela, threshold, 255, cv2.THRESH_BINARY)

        # Optionally: You could save the ELA result to a file or return some analysis metrics
        ela_result_path = "ela_result.jpg"
        cv2.imwrite(ela_result_path, ela)

        # Clean up the temporary file
        os.remove(temp_path)

        # Return more detailed information
        return {
            "ela_analysis": "ELA completed successfully.",
            "ela_result_path": ela_result_path,
            "difference_threshold": threshold,
            "jpeg_quality": jpeg_quality
        }

    except Exception as e:
        return {"error": str(e)}
