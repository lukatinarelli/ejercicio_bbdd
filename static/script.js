function showSection(sectionId) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.form-section');
    sections.forEach(section => section.style.display = 'none');

    // Mostrar solo la sección seleccionada
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}
