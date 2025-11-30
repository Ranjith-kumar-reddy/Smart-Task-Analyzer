let tasks = [];  //  before sending to backend

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("addTaskBtn").addEventListener("click", addTask);
    document.getElementById("analyzeBtn").addEventListener("click", analyzeTasks);
});

function addTask() {
    const titleEl = document.getElementById("title");
    const dueEl = document.getElementById("due_date");
    const importanceEl = document.getElementById("importance");
    const hoursEl = document.getElementById("estimated_hours");
    const depsEl = document.getElementById("dependencies");

    const title = titleEl.value.trim();
    const due_date = dueEl.value; // "YYYY-MM-DD"
    const importance = parseInt(importanceEl.value, 10);
    const estimated_hours = parseInt(hoursEl.value, 10);
    const depsRaw = depsEl.value.trim();

    if (!title || !due_date || isNaN(importance) || isNaN(estimated_hours)) {
        alert("Please fill all required fields (*) correctly.");
        return;
    }

    let dependencies = [];
    if (depsRaw) {
        dependencies = depsRaw.split(",").map((v) => v.trim()).filter(Boolean);
    }

    const task = {
        title,
        due_date,
        importance,
        estimated_hours,
        dependencies,
    };

    tasks.push(task);
    renderTaskList();

    // Optionally clear form (except importance default)
    titleEl.value = "";
    dueEl.value = "";
    importanceEl.value = 5;
    hoursEl.value = 1;
    depsEl.value = "";
}

function renderTaskList() {
    const ul = document.getElementById("taskList");
    ul.textContent = "";

    if (tasks.length === 0) {
        ul.textContent = "<li>No tasks added yet.</li>";
        return;
    }

    tasks.forEach((t, index) => {
        const li = document.createElement("li");
        li.textContent = `${index + 1}. ${t.title} (Due: ${t.due_date}, Importance: ${t.importance}, Hours: ${t.estimated_hours})`;
        ul.appendChild(li);
    });
}

async function analyzeTasks() {
    if (tasks.length === 0) {
        alert("Add at least one task before analyzing.");
        return;
    }

    const payload = { tasks };

    try {
        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            alert("Backend error while analyzing tasks.");
            return;
        }

        const data = await response.json();
        const scoredTasks = data.tasks || [];
        renderResults(scoredTasks);
    } catch (err) {
        console.error(err);
        alert("Could not reach backend. Make sure Django server is running.");
    }
}

function renderResults(tasksWithScores) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!tasksWithScores.length) {
        resultsDiv.innerHTML = "<p>No tasks returned.</p>";
        return;
    }

    tasksWithScores.forEach((task) => {
        const card = document.createElement("div");
        card.className = "task-card";
        card.innerHTML = `
            <strong>${task.title}</strong><br>
            Due: ${task.due_date}<br>
            Importance: ${task.importance}<br>
            Hours: ${task.estimated_hours}<br>
            Score: ${task.score}
        `;
        resultsDiv.appendChild(card);
    });
}
