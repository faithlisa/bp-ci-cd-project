const API = "http://localhost:8000/readings";

async function loadReadings() {
    const res = await fetch(API);
    const data = await res.json();
    const list = document.getElementById("list");
    list.innerHTML = "";
    data.forEach(r => {
        const li = document.createElement("li");
        li.innerText = `Systolic: ${r.systolic}, Diastolic: ${r.diastolic}`;
        list.appendChild(li);
    });
}

async function addReading() {
    const s = document.getElementById("systolic").value;
    const d = document.getElementById("diastolic").value;

    await fetch(API, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({systolic: parseInt(s), diastolic: parseInt(d)})
    });

    loadReadings();
}

loadReadings();
