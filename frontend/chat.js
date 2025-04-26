const backendUrl = "https://pbj-server1.onrender.com";

const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userInput = chatInput.value.trim();
  if (userInput === "") return;

  appendMessage("You", userInput);
  chatInput.value = "";

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_input: userInput }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    appendMessage("BlueJay", data.assistant);
  } catch (error) {
    console.error("Error:", error);
    appendMessage("BlueJay", "Sorry, something went wrong. Please try again later.");
  }
});

function appendMessage(sender, message) {
  const messageElement = document.createElement("div");
  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}