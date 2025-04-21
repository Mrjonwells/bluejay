let clientId = localStorage.getItem("bluejay_client_id");
if (!clientId) {
  clientId = crypto.randomUUID();
  localStorage.setItem("bluejay_client_id", clientId);
}

document.getElementById("submitBtn").addEventListener("click", submitQuestion);
document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    submitQuestion();
  }
});

async function submitQuestion() {
  const userInput = document.getElementById("userInput").value.trim();
  const responseDiv = document.getElementById("response");

  if (!userInput) {
    responseDiv.textContent = "Please enter a question.";
    return;
  }

  responseDiv.textContent = "BlueJay is thinking...";

  try {
    const res = await fetch("https://pbj-server1.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userInput,
        client_id: clientId
      }),
    });

    const data = await res.json();
    responseDiv.textContent = data.response || "No response received.";
    document.getElementById("userInput").value = "";
  } catch (error) {
    responseDiv.textContent = "Error: " + error.message;
  }
}
