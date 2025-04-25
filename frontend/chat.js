async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value;
  if (!message.trim()) return;

  const chatBox = document.getElementById("chat-box");
  const thinking = document.getElementById("thinking");

  chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
  input.value = "";
  thinking.style.display = "inline-block";

  const response = await fetch("https://pbj-server1.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id: "bluejay-user" })
  });

  const data = await response.json();
  chatBox.innerHTML += `<div><strong>BlueJay:</strong> ${data.reply}</div>`;
  thinking.style.display = "none";
  chatBox.scrollTop = chatBox.scrollHeight;
}