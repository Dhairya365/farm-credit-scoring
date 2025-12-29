document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('credit-form');
    const resultSection = document.getElementById('result-section');
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    const cityInput = document.getElementById('city-input');
    const coordsInput = document.getElementById('coords-input');
    const resetBtn = document.getElementById('reset-btn');

    // Toggle Location Method
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            toggleBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            btn.classList.add('active');

            // Show/Hide inputs
            const target = btn.dataset.target;
            if (target === 'city-input') {
                cityInput.classList.remove('hidden');
                coordsInput.classList.add('hidden');
            } else {
                cityInput.classList.add('hidden');
                coordsInput.classList.remove('hidden');
            }
        });
    });

    // Handle Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Clean up data based on active tab
        const isCityActive = !cityInput.classList.contains('hidden');
        if (isCityActive) {
            delete data.latitude;
            delete data.longitude;
        } else {
            delete data.city;
        }

        // Show loading state
        const submitBtn = form.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Analyzing...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('api/calculate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Something went wrong');
            }

            displayResult(result);

        } catch (error) {
            alert(error.message);
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });

    function displayResult(data) {
        // Populate Result
        document.getElementById('score-value').textContent = data.final_score.toFixed(1);
        document.getElementById('weather-condition').textContent = data.weather_condition || 'N/A';
        document.getElementById('soil-rating').textContent = data.soil_rating.toFixed(2);
        document.getElementById('farm-score').textContent = data.farm_score.toFixed(2);

        // Animation logic could go here

        // Switch Views
        form.closest('.glass-card').classList.add('hidden');
        resultSection.classList.remove('hidden');
    }

    // Reset
    resetBtn.addEventListener('click', () => {
        form.reset();
        resultSection.classList.add('hidden');
        form.closest('.glass-card').classList.remove('hidden');
    });
});
