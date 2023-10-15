document.addEventListener("DOMContentLoaded", function () {
    const webcam = document.getElementById("webcam");
    const startButton = document.getElementById("startWebcamButton");
    const stopButton = document.getElementById("stopWebcamButton");

    let isWebcamRunning = false;
    let videoStream;

    // Function to start the webcam feed
    function startWebcam() {
        if (!isWebcamRunning) {
            // Create an EventSource to listen to the video feed
            videoStream = new EventSource("/video_feed");

            // Add an event listener for messages from the server
            videoStream.onmessage = function (event) {
                webcam.src = "data:image/jpeg;base64," + event.data;
            };

            isWebcamRunning = true;
        }
    }

    // Function to stop the webcam feed
    function stopWebcam() {
        if (isWebcamRunning) {
            // Close the video stream and clear the image source
            videoStream.close();
            webcam.src = "";
            isWebcamRunning = false;
        }
    }

    // Attach click event handlers to the buttons
    startButton.addEventListener("click", startWebcam);
    stopButton.addEventListener("click", stopWebcam);
});
