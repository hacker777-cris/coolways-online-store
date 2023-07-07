// script.js

// Sample JavaScript code for any interactive functionality on your website (if needed).
// Replace this with your actual JavaScript logic.

// Example of adding a click event listener to a button
document.addEventListener("DOMContentLoaded", function() {
    const addToCartButtons = document.querySelectorAll(".btn");
  
    addToCartButtons.forEach(button => {
      button.addEventListener("click", function(event) {
        event.preventDefault();
        alert("Added to cart!");
      });
    });
  });
  