document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  function appendMessage(message, role) {
    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble", role);
    bubble.innerText = message;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    userInput.value = "";

    appendMessage("...", "assistant");

    try {
      const res = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await res.json();
      const bubbles = document.querySelectorAll(".chat-bubble.assistant");
      if (bubbles.length) {
        bubbles[bubbles.length - 1].innerText = data.response || "Sorry, I didn’t get that.";
      }
    } catch (err) {
      console.error("Error:", err);
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});