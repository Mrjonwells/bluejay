document.getElementById('submitBtn').addEventListener('click', async () => {
  const userInput = document.getElementById('userInput').value.trim();
  const responseDiv = document.getElementById('response');

  if (!userInput) {
    responseDiv.textContent = "Please enter a question.";
    return;
  }

  responseDiv.textContent = "PBJ is thinking...";

  try {
    const res = await fetch("https://pbj-server1.onrender.com/pbj", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await res.json();
    responseDiv.textContent = data.response || "No response received.";
  } catch (error) {
    responseDiv.textContent = "Error: " + error.message;
  }
});
