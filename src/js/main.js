document.addEventListener('DOMContentLoaded', () => {
    console.log('Aeronautics Intro App Loaded');

    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Chatbot Placeholder Logic
    const chatbotFab = document.querySelector('.fab');
    if (chatbotFab) {
        chatbotFab.addEventListener('click', () => {
            alert('AI Chatbot coming soon!');
        });
    }
});
