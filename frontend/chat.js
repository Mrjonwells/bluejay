document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatLog = document.getElementById("chatLog");

  const appendMessage = (sender, message) => {
    const bubble = document.createElement("div");
    bubble.className = sender === "user" ? "user-bubble" : "assistant-bubble";
    bubble.innerText = message;
    chatLog.appendChild(bubble);
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    chatInput.value = "";

    try {
      const response = await fetch("https://bluejay-api.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      if (data.response) {
        appendMessage("assistant", data.response);
      } else {
        appendMessage("assistant", "Sorry, I didn't get that.");
      }
    } catch (err) {
      appendMessage("assistant", "Error reaching BlueJay.");
    }
  });
});
