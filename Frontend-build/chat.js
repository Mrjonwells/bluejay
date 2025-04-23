const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(sender, message) {
  const bubble = document.createElement("div");
  bubble.classList.add(sender === "user" ? "user-bubble" : "bot-bubble");
  bubble.innerText = message;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener("click", async () => {
  const message = userInput.value.trim();
  if (message === "") return;

  appendMessage("user", message);
  userInput.value = "";

  if (message.toLowerCase().includes("submit my info")) {
    await handleHubSpotSubmission();
    return;
  }

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    appendMessage("bot", data.reply || "There was an error processing your message.");
  } catch (err) {
    appendMessage("bot", "Error processing your message.");
  }
});

userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendBtn.click();
});

async function handleHubSpotSubmission() {
  try {
    const fullName = prompt("Please enter your full name:");
    if (!fullName) return appendMessage("bot", "Submission cancelled.");

    const phone = prompt("Please enter your phone number:");
    if (!phone) return appendMessage("bot", "Submission cancelled.");

    const email = prompt("Please enter your email address:");
    if (!email) return appendMessage("bot", "Submission cancelled.");

    const company = prompt("Please enter your business name:");
    if (!company) return appendMessage("bot", "Submission cancelled.");

    appendMessage("bot", `Confirming name: ${fullName}`);
    appendMessage("bot", `Confirming phone: ${phone}`);
    appendMessage("bot", `Confirming email: ${email}`);
    appendMessage("bot", `Confirming business: ${company}`);

    const response = await fetch("/submit-to-hubspot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fullName, phone, email, company }),
    });

    const result = await response.json();
    if (result.status === "success") {
      appendMessage("bot", "Thanks! Your info has been submitted.");
    } else {
      appendMessage("bot", "There was an error sending your info.");
    }
  } catch (err) {
    appendMessage("bot", "There was an error during submission.");
  }
}