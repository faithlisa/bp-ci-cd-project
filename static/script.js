function showSection(section) {
    document.getElementById("entry").style.display = "none";
    document.getElementById("graph").style.display = "none";
    document.getElementById(section).style.display = "block";
}

function submitReading() {
    const systolic = document.getElementById("systolic").value;
    const diastolic = document.getElementById("diastolic").value;

    fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({systolic: systolic, diastolic: diastolic})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("message").innerText = data.message;
    });
}

let chart;

function loadGraph() {
    const range = document.getElementById("range").value;

    fetch(`/readings?range=${range}`)
        .then(res => res.json())
        .then(data => {
            const labels = data.map(r => r.date);
            const systolic = data.map(r => r.systolic);
            const diastolic = data.map(r => r.diastolic);

            const ctx = document.getElementById("bpChart").getContext("2d");

            if (chart) chart.destroy();

            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Systolic',
                            data: systolic,
                            borderColor: 'red',
                            fill: false
                        },
                        {
                            label: 'Diastolic',
                            data: diastolic,
                            borderColor: 'blue',
                            fill: false
                        }
                    ]
                }
            });
        });
}
