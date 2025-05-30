document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const captureBtn = document.getElementById("capture");
    const capturedImg = document.getElementById("captured-image");
    const analyzeBtn = document.getElementById("analyze");
    const resultsDiv = document.getElementById("results");
    const suggestionsBtn = document.getElementById("suggestions");
    const downloadBtn = document.getElementById("download");
    const suggestionsContainer = document.getElementById("suggestions-container");

    let gender;
    let age;
    let acne_type;

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Error accessing webcam:", err);
        });

    let capturedImage;

    captureBtn.addEventListener("click", () => {
        const context = canvas.getContext("2d");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        capturedImage = canvas.toDataURL("image/jpeg");

        capturedImg.src = capturedImage;
        video.style.display = "none";
        capturedImg.style.display = "block";

        alert("Image Captured!");
    });

    analyzeBtn.addEventListener("click", () => {
        if (!capturedImage) {
            alert("Please capture an image first!");
            return;
        }

        fetch("/realtime/analyze", {
            method: "POST",
            body: JSON.stringify({ image: capturedImage }),
            headers: { "Content-Type": "application/json" }
        })
            .then(response => response.json())
            .then(data => {
                gender = data.gender;
                age = data.age;
                acne_type = data.acne_type;
                document.getElementById("gender").textContent = data.gender;
                document.getElementById("age").textContent = data.age;
                document.getElementById("acne").textContent = data.acne_type;
                resultsDiv.classList.remove("hidden");
            })
            .catch(err => console.error("Error analyzing image:", err));
    });

    suggestionsBtn.addEventListener("click", () => {
        fetch("/realtime/suggestions", {
            method: "POST",
            body: JSON.stringify({ gender, age, acne_type }),
            headers: { "Content-Type": "application/json" }
        })
            .then(response => response.json())
            .then(data => {
                const categories = Object.keys(data);
                let htmlContent = "";

                categories.forEach((category) => {
                    try {
                        const suggestionsArray = JSON.parse(data[category].replace(/'/g, '"'));
                        htmlContent += `<h3>${category}</h3><ul>`;
                        suggestionsArray.forEach((suggestion) => {
                            htmlContent += `<li>${suggestion}</li>`;
                        });

                        htmlContent += `</ul>`;
                    } catch (error) {
                        console.error(`Error parsing suggestions for ${category}:`, error);
                    }
                });

                suggestionsContainer.innerHTML = htmlContent;
                suggestionsContainer.classList.remove("hidden");
            });
    });

    downloadBtn.addEventListener("click", () => {
        fetch("/realtime/download", {
            method: "POST",
            body: JSON.stringify({ gender, age, acne_type }),
            headers: { "Content-Type": "application/json" }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to generate PDF");
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);

                const a = document.createElement("a");
                a.href = url;
                a.download = "Skin_Analysis_Report.pdf";
                document.body.appendChild(a);
                a.click();

                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            })
            .catch(error => {
                console.error("Error downloading the PDF:", error);
            });
    });
});
