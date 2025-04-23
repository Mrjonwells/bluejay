document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const inputField = document.getElementById("user-input");
  const message = inputField.value.trim();
  if (!message) return;

  appendMessage("user", message);
  inputField.value = "";

  if (message.toLowerCase().includes("submit my info")) {
    await submitToHubSpot();
    return;
  }

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    appendMessage("assistant", data.reply || "No response.");
  } catch (error) {
    console.error("Chat error:", error);
    appendMessage("assistant", "There was an error processing your message.");
  }
}

function appendMessage(sender, text) {
  const chatBox = document.getElementById("chat-box");
  const msg = document.createElement("div");
  msg.className = sender === "user" ? "message user" : "message assistant";
  msg.textContent = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function submitToHubSpot() {
  const userData = {
    firstname: prompt("What's your first name?") || "N/A",
    lastname: prompt("What's your last name?") || "N/A",
    email: prompt("Your email?") || "test@example.com",
    phone: prompt("Phone number?") || "1234567890",
    company: prompt("Company name?") || "BlueJay Test",
    city: prompt("City?") || "San Diego",
    state: prompt("State?") || "CA",
    notes: prompt("Any notes or message?") || "Submitted from BlueJay chat"
  };

  try {
    const response = await fetch("/submit-to-hubspot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });

    const result = await response.json();
    if (result.status === "success") {
      appendMessage("assistant", "Thanks! Your info has been sent to our team.");
    } else {
      appendMessage("assistant", "Something went wrong submitting to HubSpot.");
    }
  } catch (error) {
    console.error("HubSpot error:", error);
    appendMessage("assistant", "There was an error sending your info.");
  }
}