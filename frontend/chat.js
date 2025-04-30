body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, sans-serif;
  background: linear-gradient(to bottom right, #d8eefe, #bcd8f7);
  color: #003b6f;
  text-align: center;
  overflow-x: hidden;
}

.chat-wrapper {
  max-width: 420px;
  margin: 0 auto;
  background: url('chat_card.png') no-repeat center top;
  background-size: cover;
  height: 100vh;
  position: relative;
}

.chat-box {
  position: absolute;
  top: 190px;
  left: 0;
  right: 0;
  width: 90%;
  height: 280px;
  margin: 0 auto;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  border-radius: 14px;
  padding: 12px;
}

.input-container {
  position: absolute;
  top: 480px; /* Directly below .chat-box (190 + 280 + 10 padding buffer) */
  left: 0;
  right: 0;
  width: 90%;
  margin: 0 auto;
  display: flex;
  gap: 10px;
  align-items: center;
}

#user-input {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

#send-button {
  padding: 10px 16px;
  border: none;
  background-color: #0077cc;
  color: white;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}

#send-button:hover {
  background-color: #005fa3;
}

.message {
  background-color: rgba(255, 255, 255, 0.85);
  padding: 10px 14px;
  border-radius: 12px;
  margin: 6px 12px;
  max-width: 80%;
  line-height: 1.4;
  text-align: left;
  word-wrap: break-word;
}

.message.user {
  background-color: rgba(210, 235, 255, 0.85);
  align-self: flex-end;
  text-align: right;
}

.message.bot {
  background-color: rgba(210, 255, 230, 0.85);
  align-self: flex-start;
}

#thinking-icon {
  font-size: 18px;
}
