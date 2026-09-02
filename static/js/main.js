document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    
    const resultContainer = document.getElementById('result-container');
    const predictedScoreEl = document.getElementById('predicted-score');
    const scoreMessageEl = document.getElementById('score-message');
    
    const placeholderContainer = document.getElementById('placeholder-container');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI State: Loading
        submitBtn.textContent = 'Generating...';
        submitBtn.disabled = true;
        resultContainer.classList.add('hidden');
        if (placeholderContainer) {
            placeholderContainer.classList.remove('hidden');
        }
        
        // Gather data
        const formData = new FormData(form);
        const data = {
            Study_Hours: parseFloat(formData.get('Study_Hours')),
            Attendance: parseFloat(formData.get('Attendance')),
            Previous_Score: parseFloat(formData.get('Previous_Score')),
            Parental_Education: formData.get('Parental_Education'),
            Test_Preparation: formData.get('Test_Preparation')
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // UI State: Success
                if (placeholderContainer) placeholderContainer.classList.add('hidden');
                displayResult(result.prediction);
            } else {
                // UI State: Error
                resetPlaceholder();
                alert(result.error || 'Something went wrong during prediction.');
            }
        } catch (error) {
            console.error('Error:', error);
            resetPlaceholder();
            alert('Failed to connect to the prediction server.');
        } finally {
            // Reset button state
            submitBtn.textContent = 'Generate prediction';
            submitBtn.disabled = false;
        }
    });

    function resetPlaceholder() {
        if (placeholderContainer) {
            placeholderContainer.classList.remove('hidden');
        }
    }

    function displayResult(score) {
        // Animate counting up to the score
        resultContainer.classList.remove('hidden');
        
        let startTimestamp = null;
        const duration = 1000; // 1 second animation
        
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            // Ease out quad
            const easeProgress = progress * (2 - progress);
            
            const currentScore = (easeProgress * score).toFixed(1);
            predictedScoreEl.textContent = currentScore;
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                predictedScoreEl.textContent = score.toFixed(1);
                setScoreMessage(score);
            }
        };
        
        window.requestAnimationFrame(step);
    }
    
    function setScoreMessage(score) {
        let message = '';
        
        if (score >= 85) {
            message = 'Based on the information provided, the model estimates a strong academic outcome.';
        } else if (score >= 70) {
            message = 'Based on the information provided, the model estimates an average academic outcome.';
        } else {
            message = 'Based on the information provided, the model estimates an at-risk academic outcome. Additional support is recommended.';
        }
        
        scoreMessageEl.textContent = message;
        // Removed dynamic color changes to match the more realistic product UI
        scoreMessageEl.style.color = 'var(--text-main)';
    }
});
