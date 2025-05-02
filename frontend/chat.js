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

async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  chatInput.value = "";

  const botBubble = document.createElement("div");
  botBubble.className = "bot-bubble";
  botBubble.textContent = "…";
  chatLog.appendChild(botBubble);
  chatLog.scrollTop = chatLog.scrollHeight;

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id: userId })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let result = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    try {
      const lines = chunk.trim().split("\n");
      for (const line of lines) {
        const data = JSON.parse(line);
        if (data.partial) {
          result += data.partial;
          botBubble.textContent = result;
        } else if (data.error) {
          botBubble.textContent = "Something went wrong.";
        }
      }
    } catch (err) {
      console.error("Parse error:", err);
      break;
    }
  }
}
sendButton.addEventListener("click", sendMessage);
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
