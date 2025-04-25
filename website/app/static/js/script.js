let patientData = [];
let currentFilters = {
    unidade: '',
    setor: '',
    quarto: '',
    search: ''
};
let flag=0
function updateDateTime() {
    const now = new Date();
    const options = {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const formatted = now.toLocaleString('pt-PT', options);
    document.querySelector('.datetimeInfo').textContent = formatted;
}

function checkVitalSigns(patient) {
    const alerts = [];
    
    if (patient.pulsacao < 60 || patient.pulsacao > 100) {
        alerts.push('Batimentos cardíacos anormais');
    }
    
    if (patient.temperatura < 36.0 || patient.temperatura > 37.5) {
        alerts.push('Temperatura anormal');
    }
    
    if (patient.oxigenio < 95) {
        alerts.push('Saturação de oxigênio baixa');
    }
    
    return alerts;
}

function createPatientCard(patient) {
    // Criar o elemento div manualmente em vez de usar template
    const cardHtml = `
        <div class="col-2 patient-card"
             data-unidade="${patient.unidade}"
             data-setor="${patient.setor}"
             data-quarto="${patient.quarto}"
             data-nome="${patient.nome || ''}">
            <div class="card" onclick="viewPatientDetails('${patient.id}')">
                <div class="card-title">
                    <span class="bed-info">Cama ${patient.cama}</span> | 
                    <span class="patient-name">${patient.nome || 'Paciente'}</span>
                    <div class="unit-info">${patient.unidade} - Setor ${patient.setor}</div>
                </div>
                <div class="card-body">
                    <div class="alerts"></div>
                    <div class="card-text">
                        <div class="infopulsacao cardborder">
                            <div class="row">
                                <div class="col-6">
                                    <div class="mediumInfo">NIBP<div>mmHg</div></div>
                                </div>
                                <div class="col-6">
                                    <div class="bigInfo blood-pressure">${patient.pulsacao}</div>
                                </div>
                            </div>
                        </div>
                        <div class="infooxyg cardborder">
                            <div class="row">
                                <div class="col-6">
                                    <div class="mediumInfo">SpO2<div>%</div></div>
                                </div>
                                <div class="col-6">
                                    <div class="bigInfo oxygen">${patient.oxigenio}</div>
                                </div>
                            </div>
                        </div>
                        <div class="infobatimentocardiacao cardborder">
                            <div class="row">
                                <div class="col-6">
                                    <div class="mediumInfo">
                                        <svg width="16" height="16" fill="currentColor" class="bi bi-heart-pulse-fill" viewBox="0 0 16 16">
                                            <path d="M1.475 9C2.702 10.84 4.779 12.871 8 15c3.221-2.129 5.298-4.16 6.525-6H12a.5.5 0 0 1-.464-.314l-1.457-3.642-1.598 5.593a.5.5 0 0 1-.945.049L5.889 6.568l-1.473 2.21A.5.5 0 0 1 4 9z"/>
                                        </svg> PR<div>bpm</div>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="bigInfo heart-rate">${patient.batimento_cardiaco}</div>
                                </div>
                            </div>
                        </div>
                        <div class="infotemparuta cardborder">
                            <div class="row">
                                <div class="col-6">
                                    <div class="mediumInfo">
                                        <svg width="16" height="16" fill="currentColor" class="bi bi-thermometer-high" viewBox="0 0 16 16">
                                            <path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V2.5a.5.5 0 0 1 1 0v8.585a1.5 1.5 0 0 1 1 1.415"/>
                                        </svg>Temp<div>ºC</div>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="bigInfo temperature">${patient.temperatura}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    const template = document.createElement('template');
    template.innerHTML = cardHtml.trim();
    
    // Adicionar alertas se necessário
    const card = template.content.firstChild;
    const alerts = checkVitalSigns(patient);
    if (alerts.length > 0) {
        const alertsContainer = card.querySelector('.alerts');
        alerts.forEach(alert => {
            const alertElement = document.createElement('div');
            alertElement.className = 'alert';
            alertElement.textContent = alert;
            alertsContainer.appendChild(alertElement);
        });
        card.querySelector('.card').classList.add('critical');
    }
    
    return card;
}

function viewPatientDetails(patientId) {
    // Redirect to the patient details page
    window.location.href = `/patient/${patientId}/details`;
}

function updateFilters() {
    // Coletar todas as opções únicas dos dados
    const unidades = [...new Set(patientData.map(p => p.unidade))].sort();
    const setores = [...new Set(patientData.map(p => p.setor))].sort();
    const quartos = [...new Set(patientData.map(p => p.quarto))].sort();
    
    const unidadeSelect = document.getElementById('unidadeFilter');
    const setorSelect = document.getElementById('setorFilter');
    const quartoSelect = document.getElementById('quartoFilter');
    
    // Manter seleções atuais
    const selectedUnidade = unidadeSelect.value || currentFilters.unidade;
    const selectedSetor = setorSelect.value || currentFilters.setor;
    const selectedQuarto = quartoSelect.value || currentFilters.quarto;
    
    // Atualizar unidades
    unidadeSelect.innerHTML = '<option value="">Todas Unidades</option>' + 
        unidades.map(u => `<option value="${u}" ${u === selectedUnidade ? 'selected' : ''}>${u}</option>`).join('');
    
    // Atualizar setores
    setorSelect.innerHTML = '<option value="">Todos Setores</option>' + 
        setores.map(s => `<option value="${s}" ${s === selectedSetor ? 'selected' : ''}>Setor ${s}</option>`).join('');
    
    // Atualizar quartos
    quartoSelect.innerHTML = '<option value="">Todos Quartos</option>' + 
        quartos.map(q => `<option value="${q}" ${q === selectedQuarto ? 'selected' : ''}>Quarto ${q}</option>`).join('');
    
    // Restaurar valor da busca
    document.getElementById('searchPatient').value = currentFilters.search;
}

function applyFilters() {
    // Atualizar filtros atuais
    currentFilters = {
        unidade: document.getElementById('unidadeFilter').value,
        setor: document.getElementById('setorFilter').value,
        quarto: document.getElementById('quartoFilter').value,
        search: document.getElementById('searchPatient').value.toLowerCase()
    };
    
    const cards = document.querySelectorAll('.patient-card');
    
    cards.forEach(card => {
        const matchUnidade = !currentFilters.unidade || card.dataset.unidade === currentFilters.unidade;
        const matchSetor = !currentFilters.setor || card.dataset.setor === currentFilters.setor;
        const matchQuarto = !currentFilters.quarto || card.dataset.quarto === currentFilters.quarto;
        const matchSearch = !currentFilters.search || card.dataset.nome.toLowerCase().includes(currentFilters.search);
        
        card.style.display = (matchUnidade && matchSetor && matchQuarto && matchSearch) ? '' : 'none';
    });
}

function resetFilters() {
    // Limpar filtros atuais
    currentFilters = {
        unidade: '',
        setor: '',
        quarto: '',
        search: ''
    };
    
    // Resetar elementos do DOM
    document.getElementById('unidadeFilter').value = '';
    document.getElementById('setorFilter').value = '';
    document.getElementById('quartoFilter').value = '';
    document.getElementById('searchPatient').value = '';
    
    applyFilters();
}

async function fetchPatientData() {
    if (flag === 1) {
        console.log("Aguardando a execução anterior terminar...");
        return;
    }
    
    flag = 1;
    try {
        console.log("entreaqui");
        const response = await fetch('http://localhost:8000/leituras');
        console.log("passei aqui");
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const patientData = Array.isArray(data) ? data : [];
        const container = document.getElementById('patientCards');
        container.innerHTML = ''; // Clear existing cards

        if (patientData.length === 0) {
            container.innerHTML = '<div class="col-12 text-center text-white">Nenhum paciente encontrado</div>';
            flag = 0;
            return;
        }

        patientData.forEach(patient => {
            container.appendChild(createPatientCard(patient));
        });

        updateFilters(); // Isso agora manterá as seleções
        applyFilters(); // Reaplicar filtros aos novos cartões
    } catch (error) {
        console.error('Error fetching patient data:', error);
        const container = document.getElementById('patientCards');
        container.innerHTML = '<div class="col-12 text-center text-white">Erro ao carregar dados dos pacientes</div>';
    } finally {
        flag = 0;
    }
}

// Event listeners
document.getElementById('unidadeFilter').addEventListener('change', applyFilters);
document.getElementById('setorFilter').addEventListener('change', applyFilters);
document.getElementById('quartoFilter').addEventListener('change', applyFilters);
document.getElementById('searchPatient').addEventListener('input', applyFilters);

// Update data every 5 seconds
setInterval(fetchPatientData, 5000);
setInterval(updateDateTime, 1000);

// Initial load
updateDateTime();
fetchPatientData();
