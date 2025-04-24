const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const thinkingIcon = document.getElementById("thinking-icon");

const userIdKey = "bluejay_user_id";

if (!localStorage.getItem(userIdKey)) {
  localStorage.setItem(userIdKey, crypto.randomUUID());
}

const userId = localStorage.getItem(userIdKey);

const addMessage = (text, sender) => {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userInput = input.value.trim();
  if (!userInput) return;

  addMessage(userInput, "user");
  input.value = "";
  thinkingIcon.style.display = "inline-block";

  try {
    const res = await fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput, user_id: userId })
    });

    const data = await res.json();
    thinkingIcon.style.display = "none";

    if (data.reply) {
      addMessage(data.reply, "bot");
    } else {
      addMessage("Something went wrong. Please try again.", "bot");
    }
  } catch (err) {
    thinkingIcon.style.display = "none";
    addMessage("Network error. Try again later.", "bot");
  }
});