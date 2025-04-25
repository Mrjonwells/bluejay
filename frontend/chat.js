const backendUrl = "https://pbj-server1.onrender.com";

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

  const response = await fetch(`${backendUrl}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userInput })
  });

  const data = await response.json();
  appendMessage(data.response, "bot");
  showThinkingIcon(false);
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