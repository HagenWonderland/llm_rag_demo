window.onload = function() {
    const chatbox = document.getElementById("chatbox");
    const questionInput = document.getElementById("question");
    const sendBtn = document.getElementById("send-btn");
    let isComposing = false;

    // 加入中文輸入狀態監聽
    questionInput.addEventListener('compositionstart', () => {
        isComposing = true;
    });

    questionInput.addEventListener('compositionend', () => {
        isComposing = false;
    });

    // 按 Enter 送出，避免輸入法干擾
    questionInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !isComposing) {
            e.preventDefault(); // 避免跳行或預設提交
            sendBtn.click();    // 模擬點擊送出按鈕
        }
    });

    function addMessage(role, text) {
        const msgContainer = document.createElement("div");
        msgContainer.classList.add("message-container");

        const msgBubble = document.createElement("div");
        msgBubble.classList.add("message");
        msgBubble.textContent = text;

        if (role === "user") {
            msgBubble.classList.add("user-message");
            msgContainer.classList.add("user-container");
        } else {
            msgBubble.classList.add("ai-message");
            msgContainer.classList.add("ai-container");
        }

        msgContainer.appendChild(msgBubble);
        chatbox.appendChild(msgContainer);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    sendBtn.onclick = function() {
        const question = questionInput.value.trim();
        if (!question) return;

        addMessage("user", question);
        questionInput.value = "";

        fetch("/api/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        })
        .then(r => r.json())
        .then(data => {
            addMessage("ai", data.answer);
        })
        .catch(() => {
            addMessage("ai", "伺服器錯誤，請稍後再試。");
        });
    };
};
