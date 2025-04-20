document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  const button = document.getElementById("send-btn");
  const chatBox = document.getElementById("chat-box");

  function appendToChat(role, text) {
    const msg = document.createElement("div");
    msg.textContent = `${role === "user" ? "You" : "BlueJay"}: ${text}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const userMessage = input.value.trim();
    if (!userMessage) return;

    appendToChat("user", userMessage);
    input.value = "";

    try {
      const response = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      appendToChat("assistant", data.response || "No response from assistant.");
    } catch (err) {
      appendToChat("assistant", "There was an error reaching the server.");
      console.error(err);
    }
  }

  button.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });
});
