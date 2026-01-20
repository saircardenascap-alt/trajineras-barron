// Cargar datos ecológicos desde el API
async function cargarDatosEcologicos() {
    try {
        const response = await fetch('/api/ecologico/datos');
        const datos = await response.json();
        
        // Llenar aliados ambientales
        cargarAliados(datos.compromiso.aliados);
        
        // Llenar certificaciones
        cargarCertificaciones(datos.compromiso.certificaciones);
        
        // Llenar especies
        cargarEspecies(datos.ecosistema.especies);
        
        // Llenar proyectos
        cargarProyectos(datos.proyectos);
        
        // Llenar experiencias
        cargarExperiencias(datos.experiencias);
        
        // Llenar reglas
        cargarReglas(datos.reglas);
        
        // Llenar impacto
        cargarImpacto(datos.impacto);
        
        // Llenar testimonios
        cargarTestimonios(datos.testimonios);
        
    } catch (error) {
        console.error('Error cargando datos ecológicos:', error);
    }
}

function cargarAliados(aliados) {
    const grid = document.getElementById('aliados-grid');
    grid.innerHTML = aliados.map(aliado => `
        <div class="aliado-card">
            <div class="aliado-logo">
                <i class="fas fa-leaf fa-3x"></i>
            </div>
            <h4>${aliado.nombre}</h4>
        </div>
    `).join('');
}
