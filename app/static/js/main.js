// main.js
console.log("main.js loaded and executed successfully!");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed.");
    // Additional debug message
    console.log("All DOM content is ready.");
});

// Handle any potential errors
try {
    // Insert specific JS code or functionality here
    console.log("Executing custom JavaScript functionality...");
    // Example functionality (this can be replaced with any code you need)
    // document.querySelector("body").style.backgroundColor = "#f0f0f0";
} catch (error) {
    console.error("Error in main.js:", error);
}
