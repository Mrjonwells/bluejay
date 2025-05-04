document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const chatBox = document.getElementById("chat-box");
  let userId = localStorage.getItem("bluejay_user_id");

  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("bluejay_user_id", userId);
  }

  function addMessage(role, text) {
    const msg = document.createElement("div");
    msg.className = role;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage("user", message);
    input.value = "";

    addMessage("bot", "...");
    const loading = chatBox.querySelector(".bot:last-child");

    try {
      const res = await fetch("https://bluejay-3999.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, user_id: userId }),
      });
      const data = await res.json();
      loading.remove();
      addMessage("bot", data.response);
    } catch (e) {
      loading.remove();
      addMessage("bot", "Something went wrong. Try again.");
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});