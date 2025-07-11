document.addEventListener('DOMContentLoaded', function() {
    // Vérifier les rappels toutes les minutes
    setInterval(checkReminders, 60000);
    
    // Vérifier immédiatement au chargement
    checkReminders();
});

function checkReminders() {
    fetch('/check_reminders')
        .then(response => response.json())
        .then(data => {
            data.alerts.forEach(alert => {
                showNotification(`Rappel: ${alert.title} à ${alert.time}`, 'warning');
            });
        });
}

function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(notification);
    
    // Supprimer automatiquement après 5 secondes
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.5s ease-out';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

// Exposer la fonction globalement pour les boutons
window.showNotification = showNotification;