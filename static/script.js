document.addEventListener('DOMContentLoaded', function() {
    // Vérifier les rappels toutes les minutes
    setInterval(checkReminders, 60000);
    
    // Vérifier immédiatement au chargement
    checkReminders();
});

function checkReminders() {
    // Récupérer les rappels depuis localStorage
    const reminders = JSON.parse(localStorage.getItem('dashboard_reminders') || '[]');
    const now = new Date();
    
    const alerts = reminders.filter(reminder => {
        const alertTime = new Date(reminder.alert_time);
        const reminderTime = new Date(reminder.datetime);
        return alertTime <= now && now <= reminderTime;
    });

    alerts.forEach(alert => {
        const reminderTime = new Date(alert.datetime);
        showNotification(`Rappel: ${alert.title} à ${reminderTime.toLocaleString('fr-FR')}`, 'warning');
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