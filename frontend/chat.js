const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Add message to UI
function addMessage(role, text) {
  const message = document.createElement("div");
  message.classList.add("message", role);
  message.innerText = text;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Send user message to Flask
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage("user", message);
  userInput.value = "";
  sendBtn.disabled = true;

  addMessage("assistant", "Thinking...");

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    const assistantMessages = document.querySelectorAll(".message.assistant");
    const lastAssistantMessage = assistantMessages[assistantMessages.length - 1];

    lastAssistantMessage.innerText = data.reply || "Sorry, no response.";
  } catch (err) {
    console.error("Chat error:", err);
    addMessage("assistant", "Oops! Something went wrong.");
  }

  sendBtn.disabled = false;
}

// Send on button click or Enter key
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});