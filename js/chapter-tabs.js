// Este JavaScript puede agregarse a tu archivo script.js existente

document.addEventListener('DOMContentLoaded', function() {
    // Sistema de pestañas para el blog
    const tabSystem = document.getElementById('chapter-tabs');
    
    if (tabSystem) {
        const tabs = tabSystem.querySelectorAll('.tab');
        const tabContents = document.querySelectorAll('.tab-content');
        
        // Función para mostrar una pestaña y ocultar las demás
        function showTab(tabId) {
            // Ocultar todos los contenidos de pestañas
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            
            // Quitar la clase activa de todas las pestañas
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Mostrar el contenido de la pestaña seleccionada
            const selectedContent = document.getElementById(tabId);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }
            
            // Activar la pestaña seleccionada
            const selectedTab = document.querySelector(`[data-tab="${tabId}"]`);
            if (selectedTab) {
                selectedTab.classList.add('active');
            }
            
            // Guardar la pestaña activa en localStorage
            localStorage.setItem('activeTab', tabId);
        }
        
        // Agregar eventos de clic a las pestañas
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');
                showTab(tabId);
            });
        });
        
        // Verificar si hay una pestaña activa guardada
        const activeTab = localStorage.getItem('activeTab');
        if (activeTab) {
            showTab(activeTab);
        } else {
            // Mostrar la primera pestaña por defecto
            const firstTab = tabs[0];
            if (firstTab) {
                const firstTabId = firstTab.getAttribute('data-tab');
                showTab(firstTabId);
            }
        }
    }
    
    // Efecto de carga para contenido de capítulo
    const bookContent = document.querySelector('.book-content');
    if (bookContent) {
        const originalContent = bookContent.innerHTML;
        bookContent.innerHTML = '<p class="loading-text">Cargando capítulo... <span class="loading-percentage">0%</span></p>';
        
        let loadingPercentage = 0;
        const loadingInterval = setInterval(() => {
            loadingPercentage += 5;
            const loadingElement = document.querySelector('.loading-percentage');
            if (loadingElement) {
                loadingElement.textContent = loadingPercentage + '%';
            }
            
            if (loadingPercentage >= 100) {
                clearInterval(loadingInterval);
                setTimeout(() => {
                    bookContent.innerHTML = originalContent;
                }, 500);
            }
        }, 50);
    }
    
    // Efecto de cursor pulsante en texto de SofIA
    const sofiaMessages = document.querySelectorAll('.sofia-message');
    sofiaMessages.forEach(message => {
        const text = message.textContent;
        message.innerHTML = text + '<span class="cursor"></span>';
    });
});
