let redditQueue = [];
let twitterQueue = [];

let pollingRateMs = 200;
let maxLength = 500;

const ctx = document.getElementById("liveChart").getContext('2d');
const histogramCtxReddit = document.getElementById("redditHistogram").getContext('2d');
const histogramCtxTwitter = document.getElementById("twitterHistogram").getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Reddit Mean',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)', // Red
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.4,
        },
        {
            label: 'Twitter Mean',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)', // Blue
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.4,
        }]
    },
    options: {
        responsive: true,
        animation: {
            duration: 500, // Smooth transition
            easing: 'easeInOutQuad'
        },
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
                min: -1.0, // Updated for TextBlob range
                max: 1.0,  // Updated for TextBlob range
                title: {
                    display: true,
                    text: 'Sentiment Polarity'
                }
            }
        }
    }
});


const redditHistogram = new Chart(histogramCtxReddit, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Reddit Value Distribution',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.7)'
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Value Range'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Frequency'
                }
            }
        }
    }
});

const twitterHistogram = new Chart(histogramCtxTwitter, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Twitter Value Distribution',
            data: [],
            backgroundColor: 'rgba(75, 192, 192, 0.7)'
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Value Range'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Frequency'
                }
            }
        }
    }
});

function startStream() {
    getHistoricalData();
    streamInterval = setInterval(getLatestData, pollingRateMs);
}

function stopStream() {
    clearInterval(streamInterval);
}

function getHistoricalData() {
    fetch("http://127.0.0.1:5000/api/historical?prefix=mean_store")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(json => {
            console.log("Historical Data:", json);

            if (json.reddit_mean) {
                storeData(json.reddit_mean, redditQueue);
                updateChart(0, redditQueue);
                updateHistogram(redditQueue, redditHistogram);
            } else {
                console.error("Missing reddit_mean in response:", json);
            }

            if (json.twitter_mean) {
                storeData(json.twitter_mean, twitterQueue);
                updateChart(1, twitterQueue);
                updateHistogram(twitterQueue, twitterHistogram);
            } else {
                console.error("Missing twitter_mean in response:", json);
            }

            updateCombinedTable(redditQueue, twitterQueue);
        })
        .catch(error => console.error("Error fetching historical data:", error));
}

function getLatestData() {
    fetch("http://127.0.0.1:5000/api/latest?prefix=mean_store")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(json => {
            if (json.reddit_mean) {
                storeData(json.reddit_mean, redditQueue);
                updateChart(0, redditQueue);
                updateHistogram(redditQueue, redditHistogram);
            } else {
                console.error("Missing reddit_mean in response:", json);
            }

            if (json.twitter_mean) {
                storeData(json.twitter_mean, twitterQueue);
                updateChart(1, twitterQueue);
                updateHistogram(twitterQueue, twitterHistogram);
            } else {
                console.error("Missing twitter_mean in response:", json);
            }

            updateCombinedTable(redditQueue, twitterQueue);
        })
        .catch(error => console.error("Error fetching latest data:", error));
}

function storeData(data, dataQueue) {
    if (!data || !Array.isArray(data)) {
        console.error("Data is not valid or not an array:", data);
        return;
    }

    data.forEach(item => {
        if (item.timestamp && item.value !== undefined) {
            dataQueue.push({
                time: new Date(item.timestamp),
                value: parseFloat(item.value)
            });
        } else {
            console.error("Invalid data point:", item);
        }
    });

    if (dataQueue.length > maxLength) {
        dataQueue.splice(0, dataQueue.length - maxLength);
    }
}

function updateChart(datasetIdx, dataQueue) {
    const datasetData = dataQueue.map(item => ({
        x: item.time,
        y: item.value
    }));

    if (chart.data.datasets[datasetIdx].data.length > 0) {
        chart.data.datasets[datasetIdx].data.push(datasetData[datasetData.length - 1]);
        chart.data.labels.push(datasetData[datasetData.length - 1].x);
    } else {
        chart.data.datasets[datasetIdx].data = datasetData;
        chart.data.labels = dataQueue.map(item => item.time);
    }

    if (chart.data.labels.length > maxLength) {
        chart.data.labels.shift();
        chart.data.datasets[datasetIdx].data.shift();
    }

    chart.update('none'); // Smooth updates
}

function updateHistogram(dataQueue, histogram) {
    const values = dataQueue.map(item => item.value);

    // Create bins between -1 and 1
    const binCount = 10; // Number of bins
    const binSize = 2 / binCount; // Range (-1 to 1) divided into equal parts
    const bins = Array.from({ length: binCount }, (_, i) => -1 + i * binSize);

    // Calculate frequencies
    const frequencies = bins.map((_, i) =>
        values.filter(value =>
            value >= bins[i] && value < (bins[i + 1] || Infinity)
        ).length
    );

    // Update histogram labels and data
    histogram.data.labels = bins.map((bin, i) =>
        `${bin.toFixed(2)} - ${((bins[i + 1] || 1)).toFixed(2)}`
    );
    histogram.data.datasets[0].data = frequencies;

    histogram.update();
}


function updateCombinedTable(queue1, queue2) {
    const tableBody = document.getElementById('combinedDataTable').querySelector('tbody');
    tableBody.innerHTML = '';

    const combinedData = [
        ...queue1.map(item => ({ ...item, source: 'Reddit' })),
        ...queue2.map(item => ({ ...item, source: 'Twitter' }))
    ];

    combinedData.sort((a, b) => b.time - a.time);

    combinedData.forEach(item => {
        const row = document.createElement('tr');

        const sourceCell = document.createElement('td');
        sourceCell.textContent = item.source;
        row.appendChild(sourceCell);

        const timeCell = document.createElement('td');
        timeCell.textContent = item.time.toLocaleTimeString([], {
            hour: '2-digit',
            minute
        });
        row.appendChild(timeCell);

        const valueCell = document.createElement('td');
        valueCell.textContent = item.value.toFixed(2);
        row.appendChild(valueCell);

        tableBody.appendChild(row);
    });
}
