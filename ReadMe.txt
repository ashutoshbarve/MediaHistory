Test the Backend:
Option 1: Use Swagger UI
Open the Swagger documentation:
arduino
Copy code
http://127.0.0.1:8000/docs
Find the endpoints /analyze/image/ and /analyze/video/.
Click on an endpoint and select Try it out.
Upload an image or video file as appropriate and click Execute.
Review the response to ensure the backend processes the file correctly.

Option 2: Use curl
You can test your API using the command line with curl.

For an image:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/analyze/image/" \
     -H "accept: application/json" \
     -F "file=@path/to/your/image.jpg"
For a video:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/analyze/video/" \
     -H "accept: application/json" \
     -F "file=@path/to/your/video.mp4"
