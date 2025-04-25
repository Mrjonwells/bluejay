const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

const uuid = localStorage.getItem("user_id") || crypto.randomUUID();
localStorage.setItem("user_id", uuid);

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value;
  appendMessage("You", message);
  chatInput.value = "";

  appendMessage("BlueJay", "Thinking...");

  const res = await fetch("https://pbj-server1.onrender.com/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: message,
      user_id: uuid
    })
  });

  const data = await res.json();
  const thinking = document.querySelector(".message:last-child");
  if (thinking.textContent === "BlueJay: Thinking...") thinking.remove();

  appendMessage("BlueJay", data.reply);
});

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add("message");
  msg.innerText = `${sender}: ${text}`;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}