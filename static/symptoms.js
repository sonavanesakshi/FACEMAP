// Show/hide tabs
function showTab(tabName) {
    document.getElementById("symptoms").style.display = tabName === "symptoms" ? "block" : "none";
    document.getElementById("upload").style.display = tabName === "upload" ? "block" : "none";

    // Remove 'active' class from all buttons
    document.getElementById("symptomsBtn").classList.remove("active");
    document.getElementById("uploadBtn").classList.remove("active");

    // Add 'active' class to the selected button
    if (tabName === "symptoms") {
        document.getElementById("symptomsBtn").classList.add("active");
    } else {
        document.getElementById("uploadBtn").classList.add("active");
    }
}

// Show image preview after uploading
function previewImage(event) {
    const file = event.target.files[0];

    if (!file) {
        document.getElementById("imageResult").innerHTML = `<div class="error">Please upload an image.</div>`;
        return;
    }

    // Check if the uploaded file is an image
    if (!file.type.startsWith("image/")) {
        document.getElementById("imageResult").innerHTML = `<div class="error">Only image files are allowed.</div>`;
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("imagePreview").innerHTML = `
            <h4>Uploaded Image</h4>
            <img id="uploadedImage" src="${e.target.result}" alt="Uploaded Image" />
        `;
    };
    reader.readAsDataURL(file);
}

// Predict acne type from symptoms
function predictSymptoms() {
    const symptoms = document.getElementById("symptomInput").value;
    fetch("/predict_symptoms", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ symptoms }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                document.getElementById("symptomResult").innerHTML = `<p style="color:red;">${data.error}</p>`;
            } else {
                document.getElementById("symptomList").style.display = "none";
                displayResults(data);
            }
        });
}

// Predict acne type from uploaded image
function predictImage() {
    const imageInput = document.getElementById("imageInput").files[0];
    if (!imageInput) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append("file", imageInput);

    fetch("/predict_image", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                document.getElementById("imageResult").innerHTML = `<p style="color:red;">${data.error || "Unable to predict acne type or no recommendations available."}</p>`;
            } else {
                const resultDiv = document.getElementById("imageResult");
                let resultHTML = `
                <div class="result">
                <h3>✅ Predicted Acne Type: <span>${data.acne_type}</span></h3>
                <h4>⚡ Symptoms:</h4>
                <ul>
                ${data.symptoms.map(symptom => `<li>${symptom}</li>`).join("")}
                </ul>
                
                <h4>🍴 Recommendations:</h4>
                <div class="recommendations">
                `;
                for (const [key, value] of Object.entries(data.recommendations)) {
                    if (typeof value === 'string') continue
                    resultHTML += `
                    <h5>${formatKey(key)}</h5>
                    <ul>
                    ${value.map(item => `<li>${item}</li>`).join("")}
                    </ul>
                    `;
                }

                resultHTML += `
                </div>
                </div>
                `;
                resultDiv.innerHTML = resultHTML;
            }
        });
}

// Render prediction results
function displayResults(data) {
    const resultDiv = document.getElementById("symptomResult");

    if (!data.acne_type || !data.recommendations) {
        resultDiv.innerHTML = "<div class='error'>❌ Unable to predict acne type.</div>";
        return;
    }

    // Start building HTML to display data
    let resultHTML = `
        <div class="result">
            <h3>✅ Predicted Acne Type: <span>${data.acne_type}</span></h3>
            <h4>⚡ Symptoms:</h4>
            <ul>
                ${data.symptoms.map(symptom => `<li>${symptom}</li>`).join("")}
            </ul>

            <h4>🍴 Recommendations:</h4>
            <div class="recommendations">
    `;

    // Loop through each recommendation type
    for (const [key, value] of Object.entries(data.recommendations)) {
        if (typeof value === 'string') continue
        resultHTML += `
            <h5>${formatKey(key)}</h5>
            <ul>
                ${value.map(item => `<li>${item}</li>`).join("")}
            </ul>
        `;
    }

    resultHTML += `
            </div>
        </div>
    `;

    // Insert the result HTML into the div
    resultDiv.innerHTML = resultHTML;
}

// Format keys to display with proper capitalization
function formatKey(key) {
    return key
        .replace(/_/g, " ")
        .replace(/\b\w/g, char => char.toUpperCase());
}

// Function to display symptoms list dynamically
function loadSymptomsList() {
    fetch("/symptoms/list", {
        method: "GET",
    })
        .then((response) => response.json())
        .then((data) => {
            const symptomListContainer = document.getElementById("symptomList");
            symptomListContainer.innerHTML = ""; // Clear previous list

            data.forEach((symptom) => {
                const symptomItem = document.createElement("div");
                symptomItem.className = "symptom-item";
                symptomItem.innerText = symptom;

                // Add symptom to textarea on click
                symptomItem.onclick = function () {
                    addSymptomToInput(symptom);
                };

                symptomListContainer.appendChild(symptomItem);
            });
        });
}

// Add symptom to textarea on click
function addSymptomToInput(symptom) {
    const input = document.getElementById("symptomInput");
    const currentValue = input.value.trim();

    if (currentValue) {
        // Check if symptom already exists in the textarea
        const symptomsList = currentValue.split(",").map(s => s.trim().toLowerCase());
        if (!symptomsList.includes(symptom.toLowerCase())) {
            input.value = `${currentValue}, ${symptom}`;
        }
    } else {
        input.value = symptom;
    }
}

// Show symptom list when user modifies symptoms
function showSymptomList() {
    const symptomListContainer = document.getElementById("symptomList");
    symptomListContainer.style.display = "block";
}

// Attach event listener to textarea to show the symptom list when modified
function attachTextareaListener() {
    const input = document.getElementById("symptomInput");
    input.addEventListener("input", () => {
        if (input.value.trim() !== "") {
            showSymptomList();
        }
    });
}

window.onload = function () {
    loadSymptomsList();
    attachTextareaListener();
};