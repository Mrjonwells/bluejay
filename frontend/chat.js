const backendUrl = "https://pbj-server1.onrender.com"; // Your Render backend URL

const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

// Function to generate or get UUID
function getOrCreateUUID() {
  let userId = localStorage.getItem("user_id");
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("user_id", userId);
  }
  return userId;
}

// Handle form submit
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userInput = chatInput.value.trim();
  if (userInput === "") return;

  appendMessage("You", userInput);
  chatInput.value = "";

  const userId = getOrCreateUUID();

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId, // Send UUID header
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

// Append chat message to window
function appendMessage(sender, message) {
  const messageElement = document.createElement("div");
  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}