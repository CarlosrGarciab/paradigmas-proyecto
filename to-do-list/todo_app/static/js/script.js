// ===== JAVASCRIPT SIMPLE PARA TODO APP =====

// Variables globales
let tasks = [];
let filteredTasks = [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    initializeFilters();
    loadStatistics();
});

// Filtrar tareas
function filterTasks() {
    const statusFilter = document.getElementById('filterStatus')?.value || 'all';
    const priorityFilter = document.getElementById('filterPriority')?.value || 'all';

    const taskItems = document.querySelectorAll('.task-item');
    
    taskItems.forEach(item => {
        const taskStatus = item.dataset.status;
        const taskPriority = item.dataset.priority;
        
        const statusMatch = statusFilter === 'all' || taskStatus === statusFilter;
        const priorityMatch = priorityFilter === 'all' || taskPriority === priorityFilter;
        
        if (statusMatch && priorityMatch) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
    
    updateFilteredStatistics();
}

// Alternar estado de tarea
function toggleTask(taskId, completed) {
    fetch(`/toggle/${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: completed })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar la interfaz
            const taskItem = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskItem) {
                taskItem.dataset.status = completed ? 'completed' : 'pending';
                if (completed) {
                    taskItem.classList.add('completed');
                } else {
                    taskItem.classList.remove('completed');
                }
            }
            
            showNotification(
                completed ? 'Tarea completada' : 'Tarea marcada como pendiente',
                'success'
            );
            
            // Actualizar estadísticas
            loadStatistics();
        } else {
            showNotification('Error al actualizar la tarea', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error de conexión', 'error');
    });
}

// Eliminar tarea
function deleteTask(taskId) {
    if (confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        fetch(`/delete/${taskId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remover elemento del DOM
                const taskItem = document.querySelector(`[data-task-id="${taskId}"]`);
                if (taskItem) {
                    taskItem.remove();
                    loadStatistics();
                }
                
                showNotification('Tarea eliminada correctamente', 'success');
            } else {
                showNotification('Error al eliminar la tarea', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error de conexión', 'error');
        });
    }
}

// Cargar estadísticas
function loadStatistics() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStatisticsDisplay(data);
        })
        .catch(error => {
            console.error('Error cargando estadísticas:', error);
        });
}

// Actualizar visualización de estadísticas
function updateStatisticsDisplay(stats) {
    const totalElement = document.getElementById('total-tasks');
    const pendingElement = document.getElementById('pending-tasks');
    const completedElement = document.getElementById('completed-tasks');
    
    if (totalElement) totalElement.textContent = stats.total;
    if (pendingElement) pendingElement.textContent = stats.pending;
    if (completedElement) completedElement.textContent = stats.completed;
    
    // Actualizar barra de progreso
    const progressBar = document.querySelector('.custom-progress-bar');
    const progressText = document.querySelector('.text-center.d-block.mt-2');
    
    if (progressBar) {
        progressBar.style.width = `${stats.completion_rate}%`;
    }
    
    if (progressText) {
        progressText.textContent = `${stats.completion_rate}% Completado`;
    }
}

// Actualizar estadísticas filtradas
function updateFilteredStatistics() {
    const visibleTasks = document.querySelectorAll('.task-item:not([style*="none"])');
    const completedTasks = document.querySelectorAll('.task-item[data-status="completed"]:not([style*="none"])');
    
    const total = visibleTasks.length;
    const completed = completedTasks.length;
    const pending = total - completed;
    const percentage = total > 0 ? (completed / total) * 100 : 0;
    
    // Actualizar contadores
    const totalElement = document.getElementById('total-tasks');
    const pendingElement = document.getElementById('pending-tasks');
    const completedElement = document.getElementById('completed-tasks');
    
    if (totalElement) totalElement.textContent = total;
    if (pendingElement) pendingElement.textContent = pending;
    if (completedElement) completedElement.textContent = completed;
    
    // Actualizar barra de progreso
    const progressBar = document.querySelector('.custom-progress-bar');
    if (progressBar) {
        progressBar.style.width = `${percentage}%`;
    }
}

// Mostrar notificación simple
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Estilos para posicionar la notificación
    notification.style.position = 'fixed';
    notification.style.top = '80px';
    notification.style.right = '20px';
    notification.style.zIndex = '1050';
    notification.style.minWidth = '300px';
    notification.style.padding = '12px 16px';
    notification.style.borderRadius = '8px';
    notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    
    // Colores según tipo
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#d4edda';
            notification.style.color = '#155724';
            notification.style.border = '1px solid #c3e6cb';
            break;
        case 'error':
            notification.style.backgroundColor = '#f8d7da';
            notification.style.color = '#721c24';
            notification.style.border = '1px solid #f5c6cb';
            break;
        case 'warning':
            notification.style.backgroundColor = '#fff3cd';
            notification.style.color = '#856404';
            notification.style.border = '1px solid #ffeaa7';
            break;
        default:
            notification.style.backgroundColor = '#d1ecf1';
            notification.style.color = '#0c5460';
            notification.style.border = '1px solid #bee5eb';
    }
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 3 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Inicializar filtros
function initializeFilters() {
    const statusFilter = document.getElementById('filterStatus');
    const priorityFilter = document.getElementById('filterPriority');
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTasks);
    }
    
    if (priorityFilter) {
        priorityFilter.addEventListener('change', filterTasks);
    }
}

// Validación simple de formularios
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        // Limpiar errores previos
        field.classList.remove('error');
        const errorElement = field.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
        
        if (!field.value.trim()) {
            field.classList.add('error');
            showFieldError(field, 'Este campo es obligatorio');
            isValid = false;
        }
    });
    
    return isValid;
}

// Mostrar error en campo
function showFieldError(field, message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    field.parentNode.appendChild(errorElement);
}

// Menú móvil simple
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('active');
    }
}

// Validación en tiempo real para formularios
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                showNotification('Por favor, completa todos los campos requeridos', 'warning');
            }
        });
        
        // Limpiar errores cuando el usuario empieza a escribir
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                this.classList.remove('error');
                const errorElement = this.parentNode.querySelector('.field-error');
                if (errorElement) {
                    errorElement.remove();
                }
            });
        });
    });
});

// Cerrar menú móvil al hacer clic fuera
document.addEventListener('click', function(e) {
    const mobileMenu = document.getElementById('mobileMenu');
    const toggle = document.querySelector('.mobile-menu-toggle');
    
    if (mobileMenu && toggle && 
        !mobileMenu.contains(e.target) && 
        !toggle.contains(e.target)) {
        mobileMenu.classList.remove('active');
    }
});

// Atajos de teclado simples
document.addEventListener('keydown', function(e) {
    // Ctrl + N para nueva tarea
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/add_task';
    }
    
    // ESC para cerrar menú móvil
    if (e.key === 'Escape') {
        const mobileMenu = document.getElementById('mobileMenu');
        if (mobileMenu) {
            mobileMenu.classList.remove('active');
        }
    }
});