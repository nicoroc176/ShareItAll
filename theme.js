document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Par défaut, on utilise le thème dark
    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    // Appliquer le thème
    document.body.classList.toggle('light-theme', currentTheme === 'light');
    
    // Mettre à jour l'icône
    updateThemeIcon(currentTheme);
    
    // Gérer le basculement du thème
    themeToggle.addEventListener('click', function() {
        const newTheme = document.body.classList.contains('light-theme') ? 'dark' : 'light';
        document.body.classList.toggle('light-theme');
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    // Surveiller les changements de préférence système
    prefersDarkScheme.addListener(e => {
        const newTheme = e.matches ? 'dark' : 'light';
        document.body.classList.toggle('light-theme', !e.matches);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
});

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.textContent = theme === 'dark' ? '🌞' : '🌙';
}