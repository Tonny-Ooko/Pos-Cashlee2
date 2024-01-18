document.addEventListener("DOMContentLoaded", function() {
    const successMessageDiv = document.getElementById("success-message");
    const messageBox = document.querySelector(".message");

    // Check if the message variable contains a success message
    if (messageBox.textContent.trim() === "Successfully registered the product!") {
        // Hide the original message box
        messageBox.style.display = "none";

        // Show the success message div
        successMessageDiv.style.display = "block";
    }

    // Add functionality for the register product button
    const registerButton = document.querySelector("button[type='submit']");
    registerButton.addEventListener("click", function(event) {
        // Add your custom logic here for registering the product
        console.log("Product registered!"); // Example message, replace with your logic
    });
});

