<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#dcebdc">
    <title>AERIA AI</title>

    <style>
        :root {
            --matcha: #6f9277;
            --dark: #47664f;
            --cream: #fbfaf3;
            --pink: #f5dce0;
            --pink-dark: #b96e7d;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: var(--cream);
            color: #304538;
            font-family: Arial, sans-serif;
        }

        .topbar {
            background: #dcebdc;
            padding: 22px;
            text-align: center;
        }

        .brand {
            color: var(--dark);
            font-size: 36px;
            letter-spacing: 4px;
            margin: 0;
        }

        .shell {
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 24px;
            border-radius: 20px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px #00000010;
        }

        .btn {
            background: var(--matcha);
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 12px;
            cursor: pointer;
            margin-top: 12px;
        }

        .btn-soft {
            background: var(--pink);
            color: #754b54;
        }

        .field-label {
            display: block;
            margin: 14px 0 6px;
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 13px;
            border: 1px solid #d4dfd1;
            border-radius: 10px;
        }

        .message {
            color: var(--pink-dark);
            font-size: 13px;
        }

        .link-btn {
            display: block;
            border: none;
            background: none;
            color: var(--dark);
            text-decoration: underline;
            margin-top: 12px;
            cursor: pointer;
        }

        .hidden {
            display: none !important;
        }
    </style>
</head>

<body>

<header class="topbar">
    <h1 class="brand">AERIA AI</h1>
    <p>Breathe Better. Live Better. 🌿</p>
</header>

<main class="shell">
<!-- LOGIN PAGE -->
<section id="loginPage" class="card">
    <h2>Welcome back 🌷</h2>
    <p>Log in to your AERIA AI account.</p>

    <label class="field-label">Username</label>
    <input id="loginUsername" type="text"
           placeholder="Enter username">

    <label class="field-label">Password</label>
    <input id="loginPassword" type="password"
           placeholder="Enter password">

    <button id="loginButton" class="btn">
        Log in
    </button>

    <p id="loginMessage" class="message"></p>

    <button id="goRegister" class="link-btn">
        Create a new account
    </button>
</section>
<!-- REGISTER PAGE -->
<section id="registerPage" class="card hidden">
    <h2>Create your account 🍓</h2>
    <p>Join AERIA AI.</p>

    <label class="field-label">Username</label>
    <input id="registerUsername" type="text"
           placeholder="Create username">

    <label class="field-label">Password</label>
    <input id="registerPassword" type="password"
           placeholder="Create password">

    <button id="registerButton" class="btn">
        Register
    </button>

    <p id="registerMessage" class="message"></p>

    <button id="goLogin" class="link-btn">
        Already have an account? Log in
    </button>
</section>
<!-- MAIN APP -->
<section id="appPage" class="hidden">

    <nav style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;">
        <button class="btn" data-view="homeView">Home</button>
        <button class="btn" data-view="breathingView">60 sec</button>
        <button class="btn" data-view="analysisView">AI Analysis</button>
        <button class="btn" data-view="dataView">My Data</button>
        <button id="logoutButton" class="btn btn-soft">Log out</button>
    </nav>

    <!-- HOME -->
    <section id="homeView" class="app-view">
        <div class="card">
            <h2 id="welcomeTitle">Welcome to AERIA AI 🌷</h2>
            <p>Your personal breathing and wellness support space.</p>

            <button class="btn" data-open-view="breathingView">
                Start Breathing
            </button>

            <button class="btn" data-open-view="analysisView">
                View AI Analysis
            </button>

            <button class="btn" data-open-view="dataView">
                My Data
            </button>
        </div>
    </section>
    <!-- BREATHING -->
    <section id="breathingView" class="app-view hidden">
        <div class="card" style="text-align:center;">
            <h2>60 Seconds Breathing 🌿</h2>

            <p id="breathText">Ready to begin?</p>

            <div id="breathCircle"
                 style="width:170px;height:170px;border-radius:50%;background:#e3eee0;display:flex;align-items:center;justify-content:center;margin:20px auto;font-size:22px;color:#47664f;">
                Ready
            </div>

            <h1 id="timer">60</h1>

            <button id="startBreathing" class="btn">
                Start
            </button>

            <button id="resetBreathing" class="btn btn-soft">
                Reset
            </button>
        </div>
    </section>
    <!-- AI ANALYSIS -->
    <section id="analysisView" class="app-view hidden">
        <div class="card">
            <h2>AI Analysis 🧠</h2>

            <p class="muted">
                View your latest AI analysis result.
            </p>

            <div class="result-box">
                <h3 id="analysisResult">Belum dianalisis</h3>

                <p id="confidence">Confidence: 0%</p>

                <p id="analysisMessage">
                    Press View Analysis to check your result.
                </p>
            </div>

            <button id="viewAnalysisButton" class="btn">
                View Analysis
            </button>

            <div class="disclaimer">
                <strong>Important notice:</strong>
                AI results are preliminary screening and precautionary
                indicators only. They are not a medical diagnosis.
                Please consult a doctor or qualified healthcare
                professional for further assessment.
            </div>
        </div>
    </section>
    <!-- MY DATA -->
    <section id="dataView" class="app-view hidden">
        <div class="card">
            <h2>My Data 📁</h2>

            <p class="muted">
                Your saved analysis records.
            </p>

            <div id="historyData">
                <p>No records loaded yet.</p>
            </div>

            <button id="refreshHistory" class="btn">
                Refresh Data
            </button>
        </div>
    </section>

</section>
</main>

<footer style="text-align:center;padding:20px;color:#6e7d72;font-size:12px;">
    AERIA AI · Breathe Better. Live Better. 🌿
</footer>
<script>
const $ = id => document.getElementById(id);

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        cache: "no-store",
        ...options
    });

    const data = await response.json().catch(() => ({}));
    return {response, data};
}

// PAGE CONTROL
function showLogin() {
    $("loginPage").classList.remove("hidden");
    $("registerPage").classList.add("hidden");
    $("appPage").classList.add("hidden");
}

function showRegister() {
    $("loginPage").classList.add("hidden");
    $("registerPage").classList.remove("hidden");
    $("appPage").classList.add("hidden");
}

function showHome(username) {
    $("loginPage").classList.add("hidden");
    $("registerPage").classList.add("hidden");
    $("appPage").classList.remove("hidden");

    $("welcomeTitle").textContent = "Welcome, " + username + "!";
    openView("homeView");
}

// REGISTER
async function register() {
    const username = $("registerUsername").value.trim();
    const password = $("registerPassword").value;

    $("registerMessage").textContent = "Creating account...";
    $("registerButton").disabled = true;

    try {
        const {response, data} = await apiRequest("/api/register", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        if (!response.ok) {
            $("registerMessage").textContent =
                data.error || "Registration failed.";
            return;
        }

        $("loginUsername").value = username;
        $("loginPassword").value = "";
        showLogin();
        $("loginMessage").textContent =
            "Account created! Please log in.";

    } catch (error) {
        $("registerMessage").textContent =
            "Connection error. Please try again.";
    } finally {
        $("registerButton").disabled = false;
    }
}

// LOGIN
async function login() {
    const username = $("loginUsername").value.trim();
    const password = $("loginPassword").value;

    $("loginMessage").textContent = "Logging in...";
    $("loginButton").disabled = true;

    try {
        const {response, data} = await apiRequest("/api/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });

        if (!response.ok) {
            $("loginMessage").textContent =
                data.error || "Login failed.";
            return;
        }

        $("loginMessage").textContent = "";
        showHome(data.username || username);

    } catch (error) {
        $("loginMessage").textContent =
            "Connection error. Please try again.";
    } finally {
        $("loginButton").disabled = false;
    }
}

// LOGOUT
async function logout() {
    try {
        await apiRequest("/api/logout", {method: "POST"});
    } catch (error) {
        console.error(error);
    }

    showLogin();
}

// CHECK LOGIN
async function checkLogin() {
    try {
        const {response, data} = await apiRequest("/api/me");

        if (response.ok && data.logged_in) {
            showHome(data.username || "User");
        } else {
            showLogin();
        }
    } catch (error) {
        showLogin();
    }
}
// NAVIGATION
function openView(viewId) {
    document.querySelectorAll(".app-view").forEach(view => {
        view.classList.toggle("hidden", view.id !== viewId);
    });

    if (viewId === "analysisView") {
        getAnalysis();
    }

    if (viewId === "dataView") {
        getHistory();
    }
}
// BREATHING TIMER
let timeLeft = 60;
let elapsedTime = 0;
let timerInterval = null;

function updateBreathing() {
    $("timer").textContent = timeLeft;

    if (elapsedTime % 8 < 4) {
        $("breathText").textContent = "Inhale gently";
        $("breathCircle").textContent = "Inhale";
        $("breathCircle").style.transform = "scale(1.12)";
    } else {
        $("breathText").textContent = "Exhale gently";
        $("breathCircle").textContent = "Exhale";
        $("breathCircle").style.transform = "scale(0.9)";
    }
}

function startBreathing() {
    if (timerInterval !== null) return;

    if (timeLeft <= 0) resetBreathing();

    updateBreathing();

    timerInterval = setInterval(() => {
        timeLeft--;
        elapsedTime++;

        if (timeLeft <= 0) {
            stopBreathing();
            $("timer").textContent = "0";
            $("breathText").textContent = "Session completed! 🌷";
            $("breathCircle").textContent = "Done";
            $("breathCircle").style.transform = "scale(1)";
            return;
        }

        updateBreathing();
    }, 1000);
}

function stopBreathing() {
    if (timerInterval !== null) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function resetBreathing() {
    stopBreathing();

    timeLeft = 60;
    elapsedTime = 0;

    $("timer").textContent = "60";
    $("breathText").textContent = "Ready to begin?";
    $("breathCircle").textContent = "Ready";
    $("breathCircle").style.transform = "scale(1)";
}
// GET AI ANALYSIS
async function getAnalysis() {
    const button = $("viewAnalysisButton");

    $("analysisResult").textContent = "Loading...";
    $("confidence").textContent = "";
    $("analysisMessage").textContent = "Connecting to AERIA AI...";

    button.disabled = true;

    try {
        const {response, data} = await apiRequest(
            "/api/analysis?time=" + Date.now()
        );

        if (!response.ok) {
            $("analysisResult").textContent =
                data.error || "Unable to load result.";
            $("analysisMessage").textContent =
                "Please check your login.";
            return;
        }

        $("analysisResult").textContent =
            data.class || "No result";

        $("confidence").textContent =
            "Confidence: " +
            Number(data.confidence || 0).toFixed(2) + "%";

        if (data.class === "Belum dianalisis") {
            $("analysisMessage").textContent =
                "No analysis has been saved yet.";
        } else {
            $("analysisMessage").textContent =
                "Latest saved AI result.";
        }

    } catch
    // GET SAVED HISTORY
async function getHistory() {
    const container = $("historyData");

    container.textContent = "Loading your data...";

    try {
        const {response, data} = await apiRequest(
            "/api/history?time=" + Date.now()
        );

        if (!response.ok) {
            container.textContent =
                data.error || "Unable to load history.";
            return;
        }

        container.replaceChildren();

        const records = data.history || [];

        if (records.length === 0) {
            container.textContent = "No analysis records yet.";
            return;
        }

        records.forEach(record => {
            const card = document.createElement("div");
            card.className = "history-card";

            const title = document.createElement("h3");
            title.textContent = record.result;

            const confidence = document.createElement("p");
            confidence.textContent =
                "Confidence: " +
                Number(record.confidence || 0).toFixed(2) + "%";

            const date = document.createElement("p");
            date.textContent = "Date: " + record.date;

            card.append(title, confidence, date);
            container.appendChild(card);
        });

    } catch (error) {
        container.textContent =
            "Connection error. Please try again.";
    }
}
// BUTTON EVENT LISTENERS

$("goRegister").addEventListener("click", showRegister);
$("goLogin").addEventListener("click", showLogin);

$("loginButton").addEventListener("click", login);
$("registerButton").addEventListener("click", register);

$("logoutButton").addEventListener("click", logout);

$("startBreathing").addEventListener("click", startBreathing);
$("resetBreathing").addEventListener("click", resetBreathing);

$("viewAnalysisButton").addEventListener("click", getAnalysis);
$("refreshHistory").addEventListener("click", getHistory);

// NAVIGATION BUTTONS
document.querySelectorAll("[data-view]").forEach(button => {
    button.addEventListener("click", () => {
        openView(button.dataset.view);
    });
});

document.querySelectorAll("[data-open-view]").forEach(button => {
    button.addEventListener("click", () => {
        openView(button.dataset.openView);
    });
});

// START APP
checkLogin();

</script>

</body>
</html>
