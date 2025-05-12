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

  fetch("https://bluejay-mjpg.onrender.com/chat", {
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
  const typingIndicator = document.getElementById("typing-indicator");
  if (show) {
    typingIndicator.classList.add("active");
  } else {
    typingIndicator.classList.remove("active");
  }
}

// Dropdown Menu Logic
const menuBtn = document.getElementById("hamburger");
const dropdown = document.getElementById("dropdown");
menuBtn.addEventListener("click", () => {
  dropdown.classList.toggle("hidden");
});

// Calendly popup logic
function openCalendly() {
  document.getElementById("dim-overlay").style.display = "block";
  const frame = document.getElementById("calendly-frame");
  frame.style.display = "block";
  document.getElementById("calendly-iframe").src =
    "https://calendly.com/askbluejay/30min?embed_domain=AskBlueJay.ai&embed_type=Inline";

  window.addEventListener("message", function (e) {
    if (e.origin.includes("calendly.com") && e.data.event === "calendly.event_scheduled") {
      closeCalendly();
    }
  });
}

function closeCalendly() {
  document.getElementById("dim-overlay").style.display = "none";
  const frame = document.getElementById("calendly-frame");
  frame.style.display = "none";
  document.getElementById("calendly-iframe").src = "";
}
