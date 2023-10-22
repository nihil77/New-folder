// Your classification model path
const modelPath = 'C:/Users/john/OneDrive/Desktop/New folder/Model/notebook/rnn/keypoint_rnn_model.pth';

// Function to render keypoints on the canvas
function renderKeypoints(predictions, canvas) {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (const prediction of predictions) {
        const keypoints = prediction.keypoints;

        for (const keypoint of keypoints) {
            const x = keypoint.position.x;
            const y = keypoint.position.y;

            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'red';
            ctx.fill();
        }
    }
}

// Load the PoseNet model and classify keypoints
async function detectPose() {
    const videoElement = document.getElementById('webcam');
    const canvas = document.getElementById('outputCanvas');
    const ctx = canvas.getContext('2d');

    // Load the PoseNet model
    const net = await posenet.load();

    // Load your classification model
    const yourClassificationModel = await tf.loadLayersModel(modelPath);

    const videoConfig = {
        video: {
            width: 640,
            height: 480,
        },
    };

    const stream = await navigator.mediaDevices.getUserMedia(videoConfig);
    videoElement.srcObject = stream;

    async function poseDetectionFrame() {
        const pose = await net.estimateSinglePose(videoElement);
        renderKeypoints([pose], canvas);

        // Pass the keypoints to your classification model
        const keypoints = pose.keypoints;
        const input = keypoints.map((keypoint) => [keypoint.position.x, keypoint.position.y]);
        const result = yourClassificationModel.predict(tf.tensor(input));
        const prediction = result.argMax().dataSync()[0];

        // Update the classification result on the HTML element
        const classificationResult = document.getElementById('classificationResult');
        const resultValue = document.getElementById('resultValue');
        resultValue.textContent = prediction;

        requestAnimationFrame(poseDetectionFrame);
    }

    poseDetectionFrame();
}

detectPose();
