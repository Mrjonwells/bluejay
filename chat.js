document.addEventListener("DOMContentLoaded", function () {
  const sendBtn = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  let thinkingLogo;

  function appendMessage(sender, text) {
    const message = document.createElement("div");
    message.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function showThinkingAnimation() {
    thinkingLogo = document.createElement("img");
    thinkingLogo.src = "bluejay-logo.jpeg";
    thinkingLogo.alt = "BlueJay thinking...";
    thinkingLogo.style.width = "40px";
    thinkingLogo.style.marginTop = "10px";
    thinkingLogo.style.animation = "spin 1s linear infinite";
    thinkingLogo.id = "thinking-logo";
    chatBox.appendChild(thinkingLogo);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeThinkingAnimation() {
    const existing = document.getElementById("thinking-logo");
    if (existing) {
      chatBox.removeChild(existing);
    }
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage("You", message);
    userInput.value = "";
    userInput.disabled = true;
    sendBtn.disabled = true;

    showThinkingAnimation();

    try {
      const response = await fetch("https://pbj-server1.onrender.com/pbj", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      appendMessage("BlueJay", data.response || "There was an error. Please try again.");
    } catch (err) {
      appendMessage("BlueJay", "There was an error reaching the server. Please try again later.");
    } finally {
      removeThinkingAnimation();
      userInput.disabled = false;
      sendBtn.disabled = false;
      userInput.focus();
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});
