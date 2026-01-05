// --- CONFIGURATION ---
const drawDate = new Date("Jan 6, 2026 12:00:00").getTime();
const apiEndpoint = "https://6poe7qf2a2.execute-api.eu-west-1.amazonaws.com/check"; 

// --- COUNTDOWN TIMER ---
const timerElement = document.getElementById("timer");

const countdown = setInterval(function() {
    const now = new Date().getTime();
    const distance = drawDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    timerElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

    if (distance < 0) {
        clearInterval(countdown);
        timerElement.innerHTML = "¡El Sorteo ha comenzado!";
        timerElement.style.color = "#FFD700";
    }
}, 1000);

// --- CHECK RESULT LOGIC ---
async function checkResult() {
    // 1. Get Input Elements
    const ticketInput = document.getElementById("ticket-number");
    const resultContainer = document.getElementById("result-container");
    const resultTitle = document.getElementById("result-title");
    const prizeAmount = document.getElementById("prize-amount");
    const resultMessage = document.getElementById("result-message");
    const btn = document.getElementById("check-btn");

    const ticketValue = ticketInput.value.trim();

    // 2. Input Validation
    if (ticketValue.length !== 5 || isNaN(ticketValue)) {
        alert("Por favor, introduce un número válido de 5 cifras.");
        return;
    }

    // 3. API Request
    const originalText = btn.innerText;
    btn.innerText = "Consultando a los Reyes...";
    btn.disabled = true;

    try {
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket: ticketValue })
        });

        if (!response.ok) throw new Error("Connection Failed");

        const data = await response.json();
        
        // 4. Update UI Based on Result
        resultContainer.classList.remove("hidden");

        if (data.result === "WIN") {
            // WINNER UI
            resultTitle.innerText = "¡GLORIA!";
            resultTitle.style.color = "#FFD700"; // Gold
            prizeAmount.innerText = data.prize; 
            resultMessage.innerText = `${data.category} - Ticket #${ticketValue}`;
            
            triggerConfetti(); 
        } else {
            // NON-WINNER UI
            resultTitle.innerText = "El Destino ha hablado";
            resultTitle.style.color = "#ff6b6b"; // Red
            prizeAmount.innerText = "€0";
            resultMessage.innerText = `El número ${ticketValue} no ha sido premiado esta vez.`;
        }

    } catch (error) {
        console.error(error);
        alert("Error de conexión con el servidor.");
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

function resetSearch() {
    document.getElementById("result-container").classList.add("hidden");
    const input = document.getElementById("ticket-number");
    input.value = "";
    input.focus();
}

// --- INPUT RESTRICTIONS & ENTER KEY HANDLER ---
const ticketInput = document.getElementById('ticket-number');

ticketInput.addEventListener('input', function (e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

ticketInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        checkResult();
    }
});

// --- CONFETTI EFFECT ---
function triggerConfetti() {
    const colors = ['#FFD700', '#C0C0C0', '#ffffff']; // Gold, Silver, White
    const container = document.body;

    for(let i=0; i<60; i++) {
        const spark = document.createElement('div');
        spark.style.position = 'fixed';
        spark.style.left = Math.random() * 100 + 'vw';
        spark.style.top = '-10px';
        spark.style.width = Math.random() * 8 + 5 + 'px'; 
        spark.style.height = spark.style.width;
        spark.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        spark.style.borderRadius = '50%';
        spark.style.zIndex = '9999';
        
        const duration = Math.random() * 2 + 1.5; 
        spark.style.transition = `top ${duration}s ease-in, opacity ${duration}s`;
        
        container.appendChild(spark);
        
        setTimeout(() => {
            spark.style.top = '110vh';
            spark.style.opacity = '0';
        }, 50);
        
        setTimeout(() => spark.remove(), duration * 1000);
    }
}