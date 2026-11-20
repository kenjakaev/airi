const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("send-button");
const statusElement = document.getElementById("status");

const userId = localStorage.getItem("user_id") || crypto.randomUUID();
localStorage.setItem("user_id", userId);

const conversationId =
    localStorage.getItem("conversation_id") || crypto.randomUUID();

localStorage.setItem("conversation_id", conversationId);


function addMessage(content, role) {
    const message = document.createElement("div");

    message.classList.add("message", role);
    message.textContent = content;

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}


form.addEventListener("submit", async (event) => { 
    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    input.value = "";
    sendButton.disabled = true;
    statusElement.textContent = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: userId,
                conversation_id: conversationId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        addMessage(data.response, "assistant");

    } catch (error) {
        console.error(error);
        statusElement.textContent = "Failed to send message. Check the server.";
    } finally {
        sendButton.disabled = false;
        input.focus();
    }
});