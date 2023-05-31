const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
let isDrawing = false;

// Event listeners for drawing on the canvas
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseout", stopDrawing);

// Start drawing
function startDrawing(event) {
    isDrawing = true;
    draw(event);
}

// Draw on the canvas
function draw(event) {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    context.fillStyle = "#000";
    context.fillRect(x, y, 10, 10);
}

// Stop drawing
function stopDrawing() {
    isDrawing = false;
}

// Submit the drawing to the server for prediction
document.getElementById("submitBtn").addEventListener("click", () => {
    const image = canvas.toDataURL();
    axios.post("/predict", { image })
        .then(response => {
            const resultDiv = document.getElementById("result");
            resultDiv.innerText = response.data.message;
        })
        .catch(error => {
            console.error(error);
        });
});

// Clear the canvas
document.getElementById("clearBtn").addEventListener("click", () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById("result").innerText = "";
});
