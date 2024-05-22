// script.js
function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return;

    const messageElement = document.createElement('div');
    messageElement.className = 'message user';
    messageElement.textContent = userInput;
    document.getElementById('messages').appendChild(messageElement);

    fetch('http://localhost:8080', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message bot';
        botMessageElement.textContent = data.response;
        document.getElementById('messages').appendChild(botMessageElement);
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
    });

    document.getElementById('userInput').value = '';
}
