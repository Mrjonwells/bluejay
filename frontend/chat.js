document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

window.onload = () => {
  appendMessage("bot", "Welcome to BlueJay, what’s your name?");
};

function sendMessage() {
  const inputField = document.getElementById("user-input");
  const message = inputField.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputField.value = "";
  showTyping(true);

  fetch("https://bluejay-api.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  })
    .then((res) => res.json())
    .then((data) => {
      showTyping(false);
      appendMessage("bot", data.reply || "Something went wrong.");
      if (data.reply && data.reply.includes("calendly.com")) {
        openCalendly();
      }
    })
    .catch(() => {
      showTyping(false);
      appendMessage("bot", "Something went wrong.");
    });
}

function appendMessage(sender, message) {
  const chatlog = document.getElementById("chatlog");
  const msg = document.createElement("div");
  msg.className = sender === "user" ? "user-msg" : "bot-msg";
  msg.textContent = message;
  chatlog.appendChild(msg);
  chatlog.scrollTop = chatlog.scrollHeight;
}

function showTyping(show) {
  document.getElementById("typing-indicator").classList.toggle("hidden", !show);
}

document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger");
  const dropdown = document.getElementById("dropdown");
  hamburger.addEventListener("click", () => {
    dropdown.classList.toggle("hidden");
  });

  window.addEventListener("click", (e) => {
    if (!e.target.matches("#hamburger")) dropdown.classList.add("hidden");
  });
});

function openCalendly() {
  document.getElementById("dim-overlay").style.display = "block";
  document.getElementById("calendly-frame").style.display = "block";
  document.getElementById("calendly-iframe").src =
    "https://calendly.com/askbluejay/30min?embed_domain=AskBlueJay.ai&embed_type=Inline";
}

function closeCalendly() {
  document.getElementById("dim-overlay").style.display = "none";
  document.getElementById("calendly-frame").style.display = "none";
}
