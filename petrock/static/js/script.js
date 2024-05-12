const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById("snap");
const captionText = document.getElementById("caption");

navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("[ERROR] Cannot access webcam:", err);
    });

snap.addEventListener("click", () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, 640, 480);
    const imageData = canvas.toDataURL('image/png');
    
    fetch('/capture', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        captionText.textContent = `Caption: ${data.caption}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
