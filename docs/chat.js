
document.addEventListener("DOMContentLoaded", function () {
  const chatlog = document.getElementById("chatlog");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  function appendBubble(text, className) {
    const bubble = document.createElement("div");
    bubble.className = className;
    bubble.textContent = text;
    chatlog.appendChild(bubble);
    chatlog.scrollTop = chatlog.scrollHeight;
  }

  // Initial welcome message
  appendBubble("Hi! I’m BlueJay. I can help you cut merchant fees, compare processors, or scale smarter. Ask me anything!", "assistant-bubble");

  sendBtn.addEventListener("click", () => {
    const message = userInput.value.trim();
    if (!message) return;

    appendBubble(message, "user-bubble");
    userInput.value = "";

    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    })
      .then((res) => res.json())
      .then((data) => {
        appendBubble(data.reply, "assistant-bubble");
      })
      .catch(() => {
        appendBubble("Sorry, something went wrong. Please try again.", "assistant-bubble");
      });
  });

  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") sendBtn.click();
  });
});
