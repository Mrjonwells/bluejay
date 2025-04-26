const backendUrl = "https://bluejay-1.onrender.com";

// Generate or retrieve persistent user_id
let user_id = localStorage.getItem('user_id');
if (!user_id) {
  user_id = self.crypto.randomUUID();
  localStorage.setItem('user_id', user_id);
}

const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userInput = chatInput.value.trim();
  if (userInput === "") return;

  // Show user message immediately
  const userMessage = document.createElement("div");
  userMessage.textContent = userInput;
  userMessage.className = "fade-in";
  chatMessages.appendChild(userMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  chatInput.value = "";

  try {
    const response = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": user_id
      },
      body: JSON.stringify({ user_input: userInput })
    });

    const data = await response.json();
    if (data.assistant) {
      const assistantMessage = document.createElement("div");
      assistantMessage.textContent = data.assistant;
      assistantMessage.className = "fade-in";
      chatMessages.appendChild(assistantMessage);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    } else {
      const errorMessage = document.createElement("div");
      errorMessage.textContent = "Error: No response from server.";
      errorMessage.className = "fade-in";
      chatMessages.appendChild(errorMessage);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  } catch (error) {
    const errorMessage = document.createElement("div");
    errorMessage.textContent = "Error connecting to server.";
    errorMessage.className = "fade-in";
    chatMessages.appendChild(errorMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});