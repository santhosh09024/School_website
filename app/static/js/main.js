/* ==========================================================================
   Apex School Website - Public JavaScript Interactions
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    console.log("Apex International Academy Website Loaded.");

    // Smooth Scrolling for inner links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if(targetId && targetId !== '#') {
                const targetElem = document.querySelector(targetId);
                if(targetElem) {
                    e.preventDefault();
                    targetElem.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // Dynamic Result Search via API fallback
    const resultForm = document.getElementById('public-result-form');
    if (resultForm) {
        resultForm.addEventListener('submit', function(e) {
            const inputVal = document.getElementById('identifier-input').value.trim();
            if (!inputVal) {
                alert('Please enter your Admission Number or Roll Number.');
                e.preventDefault();
            }
        });
    }
});
