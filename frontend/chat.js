const chatLog = document.getElementById("chat-log");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");

let userId = localStorage.getItem("user_id");
if (!userId) {
  userId = crypto.randomUUID();
  localStorage.setItem("user_id", userId);
}

function appendMessage(sender, text) {
  const bubble = document.createElement("div");
  bubble.className = sender === "user" ? "user-bubble" : "bot-bubble";
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  chatInput.value = "";

  const botBubble = document.createElement("div");
  botBubble.className = "bot-bubble";
  botBubble.textContent = "…";
  chatLog.appendChild(botBubble);
  chatLog.scrollTop = chatLog.scrollHeight;

  const eventSource = new EventSourcePolyfill("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    payload: JSON.stringify({ message, user_id: userId })
  });

  let responseText = "";

  eventSource.onmessage = function (event) {
    try {
      const data = JSON.parse(event.data);
      if (data.partial) {
        responseText += data.partial;
        botBubble.textContent = responseText;
      } else if (data.error) {
        botBubble.textContent = "Something went wrong.";
        eventSource.close();
      }
    } catch {
      eventSource.close();
    }
  };

  eventSource.onerror = function () {
    eventSource.close();
  };
}

sendButton.addEventListener("click", sendMessage);
chatInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter") sendMessage();
});
