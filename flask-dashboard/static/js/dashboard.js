let dataQueue1 = [];
let dataQueue2 = [];

let pollingRateMs = 3000;
let maxLength = 150;

const ctx = document.getElementById("liveChart").getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Values over time',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1,
        },
        {
            label: 'Second Dataset',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1,
        }
        ]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second'
                },
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                min: 0,
                max: 100,
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        }
    }
});

function startStream() {
    streamInterval = setInterval(getData, pollingRateMs);
}

function stopStream() {
    clearInterval(streamInterval);
}

function getData() {
    fetch("http://127.0.0.1:5000/api/data")
        .then((response) => response.json())
        .then((json) => {
            storeData(json, dataQueue1);
            updateChart(0, dataQueue1);
            updateCombinedTable(dataQueue1, dataQueue2); // Update combined table

        })
        .catch((error) => console.error("Error fetching data:", error));


    fetch("http://127.0.0.1:5000/api/data")
        .then((response) => response.json())
        .then((json) => {
            storeData(json, dataQueue2);
            updateChart(1, dataQueue2);
            updateCombinedTable(dataQueue1, dataQueue2); // Update combined table

        })
        .catch((error) => console.error("Error fetching data:", error));
}

function storeData(data, dataQueue) {
    dataQueue.push({
        time: new Date(data.time), // Convert to JavaScript Date object
        value: data.value
    });
    if (dataQueue.length > maxLength) {
        dataQueue.splice(0, 10);
    }
}

function updateChart(datasetIdx, dataQueue) {
    const timeStamps = dataQueue.map(item => item.time);
    const values = dataQueue.map(item => item.value);

    chart.data.labels = timeStamps;
    chart.data.datasets[datasetIdx].data = values;

    chart.update();
}

function logStoredData() {
    console.log(chart.data.labels);
    console.log(chart.data.datasets[0].data)
}


function updateCombinedTable(queue1, queue2) {
    const tableBody = document.getElementById('combinedDataTable').querySelector('tbody');
    tableBody.innerHTML = '';

    const combinedData = [
        ...queue1.map(item => ({ ...item, source: 'Queue 1' })),
        ...queue2.map(item => ({ ...item, source: 'Queue 2' }))
    ];

    combinedData.sort((a, b) => b.time - a.time);

    combinedData.forEach((item) => {
        const row = document.createElement('tr');

        const sourceCell = document.createElement('td');
        sourceCell.textContent = item.source;
        row.appendChild(sourceCell);

        const timeCell = document.createElement('td');
        timeCell.textContent = item.time.toLocaleString();
        row.appendChild(timeCell);

        const valueCell = document.createElement('td');
        valueCell.textContent = item.value;
        row.appendChild(valueCell);

        tableBody.appendChild(row);
    });
}
