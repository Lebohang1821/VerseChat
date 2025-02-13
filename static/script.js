function saveNote() {
    const note = document.getElementById('notes').value;
    // Save the note to local storage or send it to the server
    console.log('Note saved:', note);
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    const inputField = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const typingIndicator = document.getElementById("typing-indicator");
    const userMessage = inputField.value.trim();
    if (userMessage === "") return;
    
    const userMsgElement = document.createElement("div");
    userMsgElement.classList.add("message", "user");
    userMsgElement.textContent = userMessage;
    chatBox.appendChild(userMsgElement);
    inputField.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
    
    typingIndicator.style.display = "block";
    
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        typingIndicator.style.display = "none";
        if (data.error) {
            console.error(data.error);
            return;
        }
        const aiMessage = document.createElement("div");
        aiMessage.classList.add("message", "ai");
        aiMessage.textContent = data.response;
        chatBox.appendChild(aiMessage);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        typingIndicator.style.display = "none";
        console.error('Error:', error);
    });
}

function clearChat() {
    document.getElementById("chat-box").innerHTML = "";
}
