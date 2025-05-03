document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const messages = document.getElementById("chat-messages");

  function appendMessage(content, sender) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender);
    msg.innerHTML = content;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  function showTyping() {
    const typing = document.createElement("div");
    typing.classList.add("message", "bluejay", "typing");
    typing.innerHTML = `<span class="dot"></span><span class="dot"></span><span class="dot"></span>`;
    typing.id = "typing-indicator";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;
  }

  function removeTyping() {
    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const userInput = input.value.trim();
    if (!userInput) return;

    appendMessage(userInput, "user");
    input.value = "";
    showTyping();

    try {
      const response = await fetch("https://bluejay.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
      });
      const data = await response.json();
      removeTyping();
      appendMessage(data.reply, "bluejay");
    } catch (error) {
      removeTyping();
      appendMessage("Something went wrong. Please try again.", "bluejay");
    }
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }
  });
});