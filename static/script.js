document.addEventListener('DOMContentLoaded', function() {
    const btnElList = document.querySelectorAll('.button');
    const clearBtn = document.getElementById('clear-btn');
    const inputText = document.getElementById('input-text');
    const submitBtn = document.getElementById('submit-btn');

    btnElList.forEach(btnEl => {
        btnEl.addEventListener('click', () => {
            document.querySelector('.special')?.classList.remove('special');
            btnEl.classList.add('special');
        });
    });

    clearBtn.addEventListener('click', () => {
        inputText.value = '';
        submitBtn.disabled = true;
    });

    inputText.addEventListener('input', () => {
        submitBtn.disabled = !inputText.value.trim();
    });

    submitBtn.disabled = !inputText.value.trim();
});

