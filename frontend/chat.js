document.addEventListener("DOMContentLoaded", () => {
  const chatForm = document.getElementById("chatForm");
  const chatInput = document.getElementById("chatInput");
  const chatLog = document.getElementById("chatLog");

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    appendMessage("user", userMessage);
    chatInput.value = "";

    try {
      const response = await fetch("https://bluejay-api.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          user_id: getUserId(),
        }),
      });

      const data = await response.json();
      appendMessage("assistant", data.response);
    } catch (err) {
      appendMessage("assistant", "Something went wrong.");
    }
  });

  function appendMessage(role, message) {
    const div = document.createElement("div");
    div.textContent = message;
    div.className = role === "user" ? "userBubble" : "assistantBubble";
    chatLog.appendChild(div);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  function getUserId() {
    let id = localStorage.getItem("bluejay_user_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("bluejay_user_id", id);
    }
    return id;
  }
});
