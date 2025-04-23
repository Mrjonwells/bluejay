document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  function appendMessage(role, content) {
    const msg = document.createElement("div");
    msg.classList.add("message", role);
    msg.textContent = content;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    userInput.value = "";

    try {
      const response = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      appendMessage("assistant", data.reply || "No response received.");
    } catch (err) {
      console.error("Error:", err);
      appendMessage("assistant", "Error processing your message.");
    }
  }

  // Event listener for the button click
  sendBtn.addEventListener("click", () => {
    console.log("Send button clicked");
    sendMessage();
  });

  // Event listener for the Enter key
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      console.log("Enter key pressed");
      sendMessage();
    }
  });
});
