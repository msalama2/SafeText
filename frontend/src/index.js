// src/index.js

// Wait for the DOM to be fully loaded before executing the code
document.addEventListener('DOMContentLoaded', () => {
    // Select the 'root' div and set its inner HTML
    const rootElement = document.getElementById('root');
    rootElement.innerHTML = `<h1>Hello, Frontend!</h1>
                             <p>Welcome to my website. This is a simple frontend application.</p>`;
});
