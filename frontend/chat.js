const backendUrl = "https://www.googleapis.com/books/v1/volumes?q=javascript";

document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

async function sendMessage() {
  const inputField = document.getElementById("user-input");
  const message = inputField.value.trim();
  if (!message) return;

  addMessage(message, "user");
  inputField.value = "";

  try {
    const response = await fetch(backendUrl, {
      method: "GET", // Changed to GET for public API test
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    addMessage("API Response: " + JSON.stringify(data.items[0].volumeInfo.title), "bot");
  } catch (error) {
    console.error("Error:", error);
    addMessage("Error contacting server.", "bot");
  }
}

function addMessage(text, sender) {
  const chatContainer = document.getElementById("chat-container");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.textContent = text;
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}