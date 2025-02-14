function saveNote() {
  const note = document.getElementById("notes").value;
  // Save the note to local storage or send it to the server
  console.log("Note saved:", note);
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

function sendMessage() {
  const userInput = document.getElementById("user-input").value;
  if (userInput.trim() === "") return;

  const chatBox = document.getElementById("chat-box");
  const userMessage = document.createElement("div");
  userMessage.className = "message user";
  userMessage.textContent = userInput;
  chatBox.appendChild(userMessage);

  document.getElementById("user-input").value = "";

  const typingIndicator = document.getElementById("typing-indicator");
  typingIndicator.style.display = "block";

  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userInput }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      typingIndicator.style.display = "none";
      if (data.error) {
        throw new Error(data.error);
      }
      const aiMessage = document.createElement("div");
      aiMessage.className = "message ai";
      aiMessage.textContent = data.response; // Ensure this matches the key in the JSON response
      chatBox.appendChild(aiMessage);
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch((error) => {
      typingIndicator.style.display = "none";
      console.error("There was a problem with the fetch operation:", error);
      const errorMessage = document.createElement("div");
      errorMessage.className = "message ai";
      errorMessage.textContent =
        "There was an error processing your request. Please try again later.";
      chatBox.appendChild(errorMessage);
      chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function clearChat() {
  document.getElementById("chat-box").innerHTML = "";
}
