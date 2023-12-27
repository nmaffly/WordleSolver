function moveNext(input, event) {
    // Move to the next box when a character is entered
    if (input.value.length === input.maxLength) {
        var next = input;
        while (next = next.nextElementSibling) {
            if (next.tagName === "INPUT") {
                next.focus();
                break;
            }
        }
    }

    // Move to the previous box when backspace is pressed in an empty box
    if (event.key === "Backspace") {
        if (input.value.length === 0) {
            var previous = input;
            while (previous = previous.previousElementSibling) {
                if (previous.tagName === "INPUT") {
                    previous.focus();
                    break;
                }
            }
        }
    }
}

document.getElementById('wordle-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way

    let currentWord = '';
    const activeRow = document.querySelector('.wordle-row.active');
    const inputs = activeRow.querySelectorAll('.wordle-box');

    inputs.forEach(input => {
        currentWord += input.value;
    });

    // Now you can send currentWord to your server via AJAX or similar method
    // After processing, if you need to move to the next row:
    moveToNextRow();
});

function moveToNextRow() {
    const currentActiveRow = document.querySelector('.wordle-row.active');
    if (currentActiveRow.nextElementSibling) {
        currentActiveRow.classList.remove('active');
        currentActiveRow.nextElementSibling.classList.add('active');
    }
}

function sendWord(word) {
    fetch('/check-word', {
        method: 'POST',
        body: JSON.stringify({ 'word': word }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Process the response data
        console.log(data);
    });
}
