body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: "Segoe UI", sans-serif;
  overflow: hidden;
}

.background {
  background-image: url("chat_card.png");
  background-size: cover;
  background-position: center;
  height: 94vh;
  width: 100vw;
  position: absolute;
  z-index: -1;
}

.overlay {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
  padding-top: 3vh;
  padding-bottom: 6vh;
  position: relative;
}

.motto {
  font-size: 18px;
  color: white;
  margin-bottom: 20px;
  text-align: center;
  max-width: 90%;
}

#chat-box {
  width: 90%;
  max-width: 400px;
  height: 58vh;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 15px;
  padding: 12px;
  margin-bottom: 12px;
}

.bubble {
  padding: 10px 14px;
  margin: 6px 0;
  border-radius: 16px;
  max-width: 85%;
  word-wrap: break-word;
}

.user {
  background: #007AFF;
  color: white;
  align-self: flex-end;
  text-align: right;
}

.assistant {
  background: #f1f0f0;
  color: black;
  align-self: flex-start;
  text-align: left;
}

#chat-form {
  width: 90%;
  max-width: 400px;
  display: flex;
  justify-content: center;
}

#chat-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 20px;
  border: none;
  font-size: 16px;
}

#typing-indicator {
  font-size: 14px;
  color: #555;
  margin-top: 8px;
  font-style: italic;
}

.dots::after {
  content: "";
  display: inline-block;
  animation: dots 1.2s steps(4, end) infinite;
}

@keyframes dots {
  0% { content: ""; }
  25% { content: "."; }
  50% { content: ".."; }
  75% { content: "..."; }
  100% { content: ""; }
}

.footer {
  position: absolute;
  bottom: 8px;
  font-size: 12px;
  color: white;
  text-align: center;
  width: 100%;
}

.hidden {
  display: none;
}