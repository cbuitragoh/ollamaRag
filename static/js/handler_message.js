function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    var chatBox = document.getElementById("chat-box");
    
    // Append user message to chat box
    var userMessage = '<div class="message user-message"><p>' + userInput + '</p></div>';
    chatBox.innerHTML += userMessage;

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send user message to server
    fetch('/send-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        // Append bot's response to chat box
        var botMessage = '<div class="message bot-message"><p>' + data.message + '</p></div>';
        chatBox.innerHTML += botMessage;

        // Scroll to bottom of chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default form submission
        sendMessage();
    }
});
