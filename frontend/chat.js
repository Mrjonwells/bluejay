const backendUrl = "https://bluejay-1.onrender.com/chat";

const chatContainer = document.getElementById("chat-container");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

// Scroll to bottom
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Create a chat bubble
function createMessageBubble(message, sender) {
  const bubble = document.createElement("div");
  bubble.classList.add("message-bubble", sender);
  bubble.innerText = message;
  chatContainer.appendChild(bubble);
  scrollToBottom();
}

// Send message to backend
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  createMessageBubble(message, "user");
  userInput.value = "";

  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Server error. Please try again later.");
    }

    const data = await response.json();
    const reply = data.reply || "Sorry, something went wrong.";
    createMessageBubble(reply, "assistant");
  } catch (error) {
    console.error(error);
    createMessageBubble("Error contacting server.", "assistant");
  }
}

// Enter key sends message
userInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// Button click sends message
sendButton.addEventListener("click", sendMessage);