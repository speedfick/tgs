document.addEventListener('DOMContentLoaded', function () {
    let patientData = window.patientData; // Dados passados do template Flask
    console.log(patientData);
    patientData = patientData.readings;
    const limit = 100;
    const limitedPatientData = patientData.slice(-limit);

    const oxygenData = limitedPatientData.map(p => p.oxigenio);
    const heartRateData = limitedPatientData.map(p => p.batimento_cardiaco);
    const pressureData = limitedPatientData.map(p => p.pulsacao);
    const temperatureData = limitedPatientData.map(p => p.temperatura);

    const timeLabels = limitedPatientData.map(p => p.timestamp);

    const chartOptions = {
        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 16
                    },
                    color: '#e0e0e0'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    font: {
                        size: 16
                    },
                    color: '#e0e0e0'
                }
            },
            y: {
                ticks: {
                    font: {
                        size: 16
                    },
                    color: '#e0e0e0'
                }
            }
        }
    };

    // Exibir a data atual no formato "DD/MM/YYYY"
    const currentDate = new Date();
    const formattedDate = currentDate.toLocaleDateString('pt-BR'); // Exemplo: "13/12/2024"
    document.getElementById('DateDisplay').textContent = formattedDate;

    // Gráfico de SpO2
    new Chart(document.getElementById('oxygenChart'), {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'Saturação de Oxigênio (%)',
                data: oxygenData,
                borderColor: 'rgba(0, 123, 255, 1)',
                fill: false
            }]
        },
        options: chartOptions
    });

    // Gráfico de Batimento Cardíaco
    new Chart(document.getElementById('heartRateChart'), {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'Batimento Cardíaco (bpm)',
                data: heartRateData,
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            }]
        },
        options: chartOptions
    });

    // Gráfico de Pressão Arterial
    new Chart(document.getElementById('pressureChart'), {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'Pressão Arterial (mmHg)',
                data: pressureData,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        },
        options: chartOptions
    });

    // Gráfico de Temperatura
    new Chart(document.getElementById('temperatureChart'), {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: temperatureData,
                borderColor: 'rgba(153, 102, 255, 1)',
                fill: false
            }]
        },
        options: chartOptions
    });
});
