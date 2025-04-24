document.addEventListener("DOMContentLoaded", function () {
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const thinking = document.getElementById("thinking-indicator");

  // Generate or retrieve a persistent user ID
  let userId = localStorage.getItem("bluejay_user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("bluejay_user_id", userId);
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendMessage();
  });

  function appendMessage(role, text) {
    const msg = document.createElement("div");
    msg.className = `message ${role}`;
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function updateLastAssistantMessage(newText) {
    const messages = document.querySelectorAll(".message.assistant");
    const last = messages[messages.length - 1];
    if (last) last.textContent = newText;
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;
    thinking.style.display = "inline-block";

    appendMessage("assistant", "Thinking...");

    try {
      const res = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          message,
          user_id: userId
        })
      });

      const data = await res.json();
      updateLastAssistantMessage(data.reply || "No response received.");
    } catch (err) {
      console.error("Chat error:", err);
      updateLastAssistantMessage("Oops! Something went wrong.");
    } finally {
      thinking.style.display = "none";
      userInput.disabled = false;
      sendBtn.disabled = false;
      userInput.focus();
    }
  }
});