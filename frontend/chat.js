const backendUrl = "https://your-new-backend-url.onrender.com"; // Replace this with your new Render backend URL

document.getElementById("user-input")
  .addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      sendMessage();
    }
});

async function sendMessage() {
  const inputField = document.getElementById("user-input");
  const userInput = inputField.value.trim();
  if (userInput === "") return;

  showThinkingIcon(true);

  appendMessage(userInput, "user");
  inputField.value = "";

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    appendMessage(data.response, "bot");
  } catch (error) {
    appendMessage("Error: There was a problem connecting to BlueJay.", "bot");
  } finally {
    showThinkingIcon(false);
  }
}

function appendMessage(message, sender) {
  const chatbox = document.getElementById("chatbox");
  const messageElement = document.createElement("div");
  messageElement.className = sender;
  messageElement.innerText = message;
  chatbox.appendChild(messageElement);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function showThinkingIcon(show) {
  const icon = document.getElementById("thinking-icon");
  icon.style.display = show ? "inline-block" : "none";
}