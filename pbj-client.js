document.getElementById('submitBtn').addEventListener('click', submitQuestion);
document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        submitQuestion();
    }
});

async function submitQuestion() {
    const userInput = document.getElementById('userInput').value.trim();
    const responseDiv = document.getElementById('response');
    const savingsDiv = document.getElementById('savings');
    if (!userInput) return;

    responseDiv.innerHTML += `<div class='user-msg'><strong>You:</strong> ${userInput}</div>`;
    document.getElementById('userInput').value = '';
    responseDiv.innerHTML += `<div class='bot-msg'><em>BlueJay is thinking...</em></div>`;

    const clientId = localStorage.getItem('client_id') || crypto.randomUUID();
    localStorage.setItem('client_id', clientId);

    try {
        const res = await fetch("https://pbj-server1.onrender.com/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput, client_id: clientId })
        });

        const data = await res.json();
        document.querySelector(".bot-msg").remove();
        responseDiv.innerHTML += `<div class='bot-msg'><strong>BlueJay:</strong> ${data.response}</div>`;

        // Display estimated savings if returned
        if (data.savings) {
            savingsDiv.innerHTML = `
                <div class="savings-card">
                    <h3>Estimated Savings</h3>
                    <p><strong>Monthly:</strong> $${data.savings.monthly_savings}</p>
                    <p><strong>Yearly:</strong> $${data.savings.yearly_savings}</p>
                </div>
            `;
        }
        responseDiv.scrollTop = responseDiv.scrollHeight;
    } catch (error) {
        responseDiv.innerHTML += `<div class='bot-msg error'>Error: ${error.message}</div>`;
    }
}
