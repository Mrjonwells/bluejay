async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value;
  if (!message.trim()) return;

  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
  input.value = "";

  const response = await fetch("https://pbj-server1.onrender.com/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      user_id: localStorage.getItem("user_id") || "bluejay-stream"
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let output = "";

  chatBox.innerHTML += `<div id="bluejay-reply"><strong>BlueJay:</strong> <span></span></div>`;
  const replySpan = document.querySelector("#bluejay-reply span");

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    output += chunk;
    replySpan.textContent = output;
  }
}