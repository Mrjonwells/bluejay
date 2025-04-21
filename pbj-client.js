document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("userInput");
  const responseDiv = document.getElementById("response");
  const sendBtn = document.getElementById("submitBtn");
  const clientId = localStorage.getItem("client_id") || crypto.randomUUID();
  localStorage.setItem("client_id", clientId);

  // Function to send the user's question
  async function sendQuestion() {
    const userText = input.value.trim();
    if (!userText) return;

    // Show user input in the chat
    appendMessage("You", userText);
    responseDiv.scrollTop = responseDiv.scrollHeight;
    input.value = "";

    appendMessage("BlueJay", "Thinking...");

    try {
      const res = await fetch("https://pbj-server1.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: userText,
          client_id: clientId
        })
      });

      const data = await res.json();
      const messages = responseDiv.querySelectorAll(".message");
      if (messages[messages.length - 1].textContent === "BlueJay: Thinking...") {
        messages[messages.length - 1].remove();
      }
      appendMessage("BlueJay", data.response || "No response received.");
    } catch (error) {
      appendMessage("BlueJay", "Error: " + error.message);
    }

    responseDiv.scrollTop = responseDiv.scrollHeight;
  }

  // Function to display messages
  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message");
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    responseDiv.appendChild(msg);
  }

  // Send on click
  sendBtn.addEventListener("click", sendQuestion);

  // Send on Enter
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendQuestion();
    }
  });
});
