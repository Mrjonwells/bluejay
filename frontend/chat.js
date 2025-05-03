const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const typingIndicator = document.getElementById("typing-indicator");

// Show greeting
addMessage("Hi, I'm BlueJay, your business expert. What’s your name?", "assistant");

// Scroll to bottom
function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Add message to box
function addMessage(text, sender) {
  const bubble = document.createElement("div");
  bubble.classList.add("chat-bubble", sender);
  bubble.innerText = text;
  chatBox.appendChild(bubble);
  scrollToBottom();
}

// Show typing dots
function showTyping() {
  typingIndicator.style.display = "flex";
  scrollToBottom();
}

// Hide typing
function hideTyping() {
  typingIndicator.style.display = "none";
}

// Handle message send
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";
  showTyping();

  try {
    const response = await fetch("https://bluejay-api.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    hideTyping();
    addMessage(data.reply, "assistant");
  } catch (err) {
    hideTyping();
    addMessage("Sorry, there was an error.", "assistant");
  }
});