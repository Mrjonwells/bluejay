body {
  margin: 0;
  padding: 0;
  background: url("chat_card.png") no-repeat center center fixed;
  background-size: contain;
  font-family: sans-serif;
  height: 100vh;
  overflow: hidden;
}

.chat-container {
  position: absolute;
  top: calc(50% - 60px); /* original BlueJay 8.0 GM position */
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 600px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

#chatlog {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.user-msg, .bot-msg {
  margin: 10px 0;
  padding: 10px;
  border-radius: 8px;
  line-height: 1.4em;
}

.user-msg {
  background-color: #007bff;
  color: white;
  text-align: right;
}

.bot-msg {
  background-color: #e0e0e0;
  color: black;
  text-align: left;
}

.input-container {
  display: flex;
  gap: 10px;
}

#user-input {
  flex: 1;
  padding: 10px;
  font-size: 1em;
  border-radius: 5px;
  border: 1px solid #ccc;
}

#send-btn {
  padding: 10px 20px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.legal-footer {
  position: absolute;
  bottom: 10px;
  width: 100%;
  text-align: center;
  font-size: 12px;
  color: white;
}