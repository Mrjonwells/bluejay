const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");
const typingIndicator = document.getElementById("typingIndicator");

function appendMessage(sender, message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;
  messageDiv.innerText = message;
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function showTyping(show) {
  typingIndicator.style.display = show ? "block" : "none";
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  userInput.value = "";
  showTyping(true);

  try {
    const response = await fetch("https://bluejay-api.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    appendMessage("bot", data.response);
  } catch (error) {
    appendMessage("bot", "Sorry, something went wrong.");
  } finally {
    showTyping(false);
  }
}

userInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") sendMessage();
});
