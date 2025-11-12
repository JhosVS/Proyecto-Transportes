// ========== VARIABLES GLOBALES DE PANELES ==========
const overlay = document.getElementById('overlay');
const trackingPanel = document.getElementById('tracking-panel');
const rankingPanel = document.getElementById('ranking-panel');

let selectedTrip = {};
let selectedSeats = [];

// ========== LÓGICA DE MANEJO DE PANELES CORE ==========

function openPanel(panel) {
  if (overlay) overlay.classList.add('active');
  panel.classList.add('active');
}

function closePanel(panel) {
  panel.classList.remove('active');
}

function closeAllPanels() {
  closeTracking();
  closeRanking();
  if (overlay) overlay.classList.remove('active');
}

// ========== RASTREO (TRACKING) ==========

function openTracking() {
  closeAllPanels();
  openPanel(trackingPanel);
}

function closeTracking() {
  closePanel(trackingPanel);
}

async function searchPackage() {
    const serie = document.getElementById('tracking-serie').value;
    const correlativo = document.getElementById('tracking-correlativo').value;
    const clave_secreta = document.getElementById('tracking-clave').value;

    if (!serie || !correlativo || !clave_secreta) {
        alert('Ingrese la Serie, Correlativo y Clave Secreta para buscar.');
        return;
    }

    try {
        const response = await fetch('/api/rastrear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                serie: serie,
                correlativo: correlativo,
                clave_secreta: clave_secreta
            })
        });

        const data = await response.json();

        if (data.success) {
            const encomienda = data.encomienda;
            
            document.getElementById('package-id').textContent = `Paquete #${encomienda.serie}-${encomienda.correlativo}`;
            document.getElementById('package-route').textContent = `${encomienda.origen} → ${encomienda.destino}`;
            document.getElementById('current-status').textContent = encomienda.estado_actual;

            const timelineHtml = encomienda.timeline.map((item, index) => `
                <div class="timeline-item ${index === 0 ? 'active' : ''}">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <h5>${item.Estado}</h5>
                        <p>${item.Ubicacion || 'Sin ubicación'}</p>
                        <span class="time">${new Date(item.FechaHora).toLocaleString()}</span>
                    </div>
                </div>
            `).join('');

            document.getElementById('timeline').innerHTML = timelineHtml;
            document.getElementById('package-result').style.display = 'block';
        } else {
            alert('No se encontró la encomienda. Verifique los datos.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al buscar la encomienda.');
    }
}

// ========== RANKING ==========

function openRanking() {
  closeAllPanels();
  renderFeaturedCompanies();
  openPanel(rankingPanel);
}

function closeRanking() {
  closePanel(rankingPanel);
}

async function renderFeaturedCompanies() {
    try {
        const response = await fetch('/api/ranking');
        const data = await response.json();
        
        const grid = document.getElementById('featured-companies');
        
        if (data.agencias && data.agencias.length > 0) {
            grid.innerHTML = data.agencias.map(agencia => `
                <div class="company-card">
                    <div class="company-logo" style="background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold;">
                        ${agencia.Nombre ? agencia.Nombre.charAt(0) : 'A'}
                    </div>
                    <h3>${agencia.Nombre || 'Agencia'}</h3>
                    <div class="company-rating">
                        <span class="star">⭐</span>
                        <span class="score">${agencia.Rating ? agencia.Rating.toFixed(1) : '4.5'}</span>
                        <span class="trips">(${agencia.UsosSimulados || '100'} viajes)</span>
                    </div>
                    <div class="service-tags">
                        <span class="service-tag">Pasajes</span>
                        <span class="service-tag">Encomiendas</span>
                    </div>
                    <button class="btn primary" onclick="searchFromCompany('${agencia.Nombre || ''}')">Ver Servicios</button>
                </div>
            `).join('');
        } else {
            // Datos de ejemplo si no hay agencias en la BD
            grid.innerHTML = `
                <div class="company-card">
                    <div class="company-logo" style="background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold;">T</div>
                    <h3>Transportes El Rápido</h3>
                    <div class="company-rating">
                        <span class="star">⭐</span>
                        <span class="score">4.8</span>
                        <span class="trips">(1250 viajes)</span>
                    </div>
                    <div class="service-tags">
                        <span class="service-tag">Pasajes</span>
                        <span class="service-tag">Encomiendas</span>
                    </div>
                    <button class="btn primary" onclick="searchFromCompany('Transportes El Rápido')">Ver Servicios</button>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error cargando ranking:', error);
    }
}

function searchFromCompany(companyName) {
    document.getElementById('hero-origen').value = 'LIMA';
    document.getElementById('hero-destino').value = 'CERRO DE PASCO';
    closeAllPanels();
    document.getElementById('hero-section').scrollIntoView({ behavior: 'smooth' });
}

// ========== LÓGICA DE COMPRA DE PASAJES ==========
function scrollToHero() {
    document.getElementById('hero-section').scrollIntoView({ behavior: 'smooth' });
}

function setStep(step) {
  const steps = document.querySelectorAll('#progress-bar .step');
  steps.forEach(s => {
    const stepNum = parseInt(s.dataset.step);
    s.classList.remove('active', 'done');
    if (stepNum === step) {
      s.classList.add('active');
    } else if (stepNum < step) {
      s.classList.add('done');
    }
  });
}

function searchFromHero() {
  const origen = document.getElementById('hero-origen').value;
  const destino = document.getElementById('hero-destino').value;
  const fecha = document.getElementById('hero-fecha').value;

  if (!origen || !destino || !fecha) {
      alert('Por favor, complete Origen, Destino y Fecha.');
      return;
  }

  // Enviar formulario
  const form = document.createElement('form');
  form.method = 'POST';
  form.action = '/buscar-viajes';
  
  const inputOrigen = document.createElement('input');
  inputOrigen.name = 'ciudad_origen';
  inputOrigen.value = origen;
  form.appendChild(inputOrigen);
  
  const inputDestino = document.createElement('input');
  inputDestino.name = 'ciudad_destino';
  inputDestino.value = destino;
  form.appendChild(inputDestino);
  
  const inputFecha = document.createElement('input');
  inputFecha.name = 'fecha';
  inputFecha.value = fecha;
  form.appendChild(inputFecha);
  
  document.body.appendChild(form);
  form.submit();
}

function backToSearch() {
    window.location.href = '/';
}

function updatePriceFilter() {
    const value = document.getElementById('price-range').value;
    document.getElementById('price-label').textContent = `Máx: S/${value}`;
    filterResults();
}

function filterResults() {
    const priceFilter = parseFloat(document.getElementById('price-range').value);
    const sortBy = document.getElementById('sort-by').value;
    
    const results = document.querySelectorAll('.result-item');
    
    results.forEach(result => {
        const priceText = result.querySelector('.price').textContent;
        const price = parseFloat(priceText.replace('S/', ''));
        
        if (price <= priceFilter) {
            result.style.display = 'grid';
        } else {
            result.style.display = 'none';
        }
    });
    
    // Ordenar resultados (simplificado)
    const container = document.getElementById('results-list');
    const items = Array.from(results).filter(item => item.style.display !== 'none');
    
    if (sortBy === 'price') {
        items.sort((a, b) => {
            const priceA = parseFloat(a.querySelector('.price').textContent.replace('S/', ''));
            const priceB = parseFloat(b.querySelector('.price').textContent.replace('S/', ''));
            return priceA - priceB;
        });
    }
    
    // Re-insertar en orden
    items.forEach(item => container.appendChild(item));
}

function selectTrip(company, route, price, id) {
    selectedTrip = { company, route, price, id };
    selectedSeats = [];

    document.getElementById('results-section').style.display = 'none';
    document.getElementById('checkout-section').style.display = 'block';

    setStep(3);

    renderSeats(40);
    updateSummary();

    document.getElementById('checkout-section').scrollIntoView({ behavior: 'smooth' });
}

function renderSeats(totalSeats) {
    const layout = document.getElementById('seat-layout');
    let seatsHtml = '';

    for(let i = 1; i <= totalSeats; i++) {
        let status = 'available';
        if (i % 7 === 0 || i === 1) status = 'reserved';

        const isSelected = selectedSeats.includes(i);
        if (isSelected) status = 'selected';

        seatsHtml += `
            <div class="seat ${status}" data-seat="${i}" onclick="toggleSeat(${i}, '${status}')">${i}</div>
        `;
    }
    layout.innerHTML = seatsHtml;
}

function toggleSeat(seatNum, status) {
    if (status === 'reserved') return;

    const index = selectedSeats.indexOf(seatNum);
    if (index > -1) {
        selectedSeats.splice(index, 1);
    } else {
        selectedSeats.push(seatNum);
    }

    renderSeats(40);
    updateSummary();
}

function updateSummary() {
    const total = selectedSeats.length * (selectedTrip.price || 0);
    const passengerName = document.getElementById('p-nombres').value + ' ' + document.getElementById('p-apellidos').value;
    const passengerDni = document.getElementById('p-dni').value;

    document.getElementById('summary-route').textContent = selectedTrip.route || '-';
    document.getElementById('summary-company').textContent = selectedTrip.company || '-';
    document.getElementById('summary-passenger').textContent = passengerName.trim() || '-';
    document.getElementById('summary-dni').textContent = passengerDni || '-';
    document.getElementById('summary-seats').textContent = selectedSeats.sort((a,b) => a-b).join(', ') || 'Ninguno';
    document.getElementById('summary-total').textContent = `S/ ${total.toFixed(2)}`;
}

function nextStep(nextStepNum) {
    if (nextStepNum === 4) {
         if (selectedSeats.length === 0) {
             alert('Debe seleccionar al menos un asiento.');
             return;
         }
         if (!document.getElementById('p-nombres').value || !document.getElementById('p-dni').value) {
             alert('Por favor, complete los datos del pasajero (Nombres y DNI).');
             return;
         }

         document.getElementById('checkout-section').style.display = 'none';
         document.getElementById('confirmation-section').style.display = 'block';
         setStep(4);
         document.getElementById('confirmation-section').scrollIntoView({ behavior: 'smooth' });
    }
}

// ========== INICIALIZACIÓN Y EVENTOS ==========
document.addEventListener('DOMContentLoaded', () => {
  // 1. Configurar fecha de salida para mañana
  const today = new Date();
  today.setDate(today.getDate() + 1);
  const dateStr = today.toISOString().split('T')[0];
  if (document.getElementById('hero-fecha')) {
    document.getElementById('hero-fecha').value = dateStr;
  }

  // 2. Renderizar contenido dinámico inicial para Ranking
  if (document.getElementById('featured-companies')) renderFeaturedCompanies();

  // 3. Inicializar barra de progreso si existe
  if (document.getElementById('progress-bar')) {
    setStep(1); 
  }
});

// 4. Cerrar con ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeAllPanels();
});