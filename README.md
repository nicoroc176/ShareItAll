# Dashboard Personnel

Un dashboard personnel moderne avec gestion de fichiers, rappels et liens favoris.

## Fonctionnalités

- 📁 **Gestion des fichiers** : Upload, téléchargement et suppression de fichiers
- ⏰ **Rappels personnalisés** : Création de rappels avec alertes
- 🔗 **Liens favoris** : Stockage et accès rapide aux liens importants
- 🌙 **Thème sombre/clair** : Basculement automatique selon les préférences
- 🔐 **Authentification** : Protection par mot de passe

## Déploiement sur Render

### 1. Préparer le projet

1. Assurez-vous que tous les fichiers sont présents :
   - `index.html` (page principale)
   - `static/style.css` (styles)
   - `static/script.js` (logique JavaScript)
   - `static/theme.js` (gestion des thèmes)
   - `package.json` (configuration Node.js)

### 2. Déployer sur Render

1. Connectez-vous à votre compte Render
2. Cliquez sur "New +" puis "Web Service"
3. Connectez votre repository GitHub/GitLab
4. Configurez le service :
   - **Name** : `dashboard-personnel`
   - **Environment** : `Node`
   - **Build Command** : `npm install`
   - **Start Command** : `npm start`
   - **Plan** : Free

### 3. Variables d'environnement (optionnel)

Si vous souhaitez changer le mot de passe par défaut, vous pouvez ajouter une variable d'environnement dans Render :
- **Key** : `ADMIN_PASSWORD`
- **Value** : Votre nouveau mot de passe

Puis modifier la ligne dans `index.html` :
```javascript
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "Rocacher176";
```

## Utilisation

1. Accédez à votre application déployée
2. Entrez le mot de passe : `Rocacher176`
3. Utilisez les différentes sections pour gérer vos données

## Stockage des données

Toutes les données sont stockées localement dans le navigateur via localStorage :
- Rappels : `dashboard_reminders`
- Liens : `dashboard_links`
- Fichiers : `dashboard_files`
- État de connexion : `dashboard_logged_in`

## Structure du projet

```
├── index.html          # Page principale
├── package.json        # Configuration Node.js
├── README.md          # Documentation
└── static/
    ├── style.css      # Styles CSS
    ├── script.js      # Logique JavaScript
    └── theme.js       # Gestion des thèmes
```

## Technologies utilisées

- HTML5
- CSS3 (avec variables CSS pour les thèmes)
- JavaScript vanilla (ES6+)
- localStorage pour le stockage
- http-server pour le serveur de développement

## Développement local

Pour tester localement :

```bash
npm install
npm start
```

Puis ouvrez `http://localhost:8080` dans votre navigateur.

## Notes importantes

- Les fichiers uploadés sont simulés (pas de stockage réel sur le serveur)
- Les données sont persistantes dans le navigateur
- L'application fonctionne entièrement côté client
- Compatible avec tous les navigateurs modernes 