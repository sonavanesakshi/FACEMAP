const authForm = document.getElementById("authForm");
const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const switchText = document.getElementById("switchText");
const switchLink = document.getElementById("switchToSignup");
const errorMsg = document.getElementById("errorMsg");

const confirmPasswordField = document.getElementById("confirmPassword");

const formContainer = document.querySelector(".form-container");

let isLogin = true;
let isAnimating = false;

function updateFormContent() {
    if (isLogin) {
        formTitle.innerText = "Login";
        submitBtn.innerText = "Login";
        switchText.innerText = "Don't have an account?";
        switchLink.innerText = "Sign up here";
        confirmPasswordField.style.display = "none";
        confirmPasswordField.removeAttribute("required");
    } else {
        formTitle.innerText = "Sign Up";
        submitBtn.innerText = "Sign Up";
        switchText.innerText = "Already have an account?";
        switchLink.innerText = "Login here";
        confirmPasswordField.style.display = "block";
        confirmPasswordField.setAttribute("required", "true");
    }
}

switchLink.addEventListener("click", (e) => {
    e.preventDefault();
    if (isAnimating) return; // Prevent multiple clicks during animation
    isAnimating = true;

    // Apply correct animation
    formContainer.classList.add(isLogin ? "slide-left" : "slide-right");

    // Wait for animation to complete
    setTimeout(() => {
        isLogin = !isLogin;
        updateFormContent();

        // Force reflow to reset animations
        formContainer.style.display = "none";
        formContainer.offsetHeight;
        formContainer.style.display = "block";

        // Remove slide-out class and add slide-in
        requestAnimationFrame(() => {
            formContainer.classList.remove("slide-left", "slide-right");
            formContainer.classList.add("slide-in");

            // Reset animation after slide-in
            setTimeout(() => {
                formContainer.classList.remove("slide-in");
                isAnimating = false; // Enable next click
            }, 300);
        });
    }, 300);
});

authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Hello")
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = confirmPasswordField.value;

    if (!isLogin && password !== confirmPassword) {
        errorMsg.innerText = "Passwords do not match!";
        return;
    }

    const url = isLogin ? "/login" : "/signup";
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    const result = await response.json();
    if (result.success) {
        if (!isLogin) alert("User successfully created!");
        if (isLogin) localStorage.setItem("username", username)
        window.location.href = isLogin ? "/home" : "/";
    } else {
        errorMsg.innerText = result.message;
    }
});

updateFormContent()