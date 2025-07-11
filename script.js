// Gestion simplifiée des données en localStorage
const STORAGE_KEYS = {
    FILES: 'userFiles',
    REMINDERS: 'reminders',
    LINKS: 'links'
};

// Simulation de l'upload
function handleUpload() {
    const files = document.getElementById('file-upload').files;
    // Stockage dans localStorage (solution simplifiée)
    const storedFiles = JSON.parse(localStorage.getItem(STORAGE_KEYS.FILES) || '[]');
    
    Array.from(files).forEach(file => {
        storedFiles.push({
            name: file.name,
            size: file.size,
            lastModified: file.lastModified
        });
    });

    localStorage.setItem(STORAGE_KEYS.FILES, JSON.stringify(storedFiles));
    updateFileList();
}

function updateFileList() {
    const files = JSON.parse(localStorage.getItem(STORAGE_KEYS.FILES) || '[]');
    const fileListHTML = files.map(file => `
        <div class="file-item">
            <span>${file.name} (${(file.size / 1024).toFixed(2)} KB)</span>
            <button onclick="downloadFile('${file.name}')">Télécharger</button>
            <button onclick="deleteFile('${file.name}')">Supprimer</button>
        </div>
    `).join('');

    document.getElementById('fileList').innerHTML = fileListHTML || '<p>Aucun fichier</p>';
}

// Fonctions similaires pour reminders et links...