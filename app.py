from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

ADMIN_PASSWORD = "Rocacher176"

# Créer les dossiers et fichiers nécessaires
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
for json_file in ['reminders.json', 'links.json']:
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            json.dump([], f)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    try:
        # Charger les rappels
        with open('reminders.json', 'r', encoding='utf-8') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        reminders = []
    
    try:
        # Charger les liens
        with open('links.json', 'r', encoding='utf-8') as f:
            links = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        links = []
    
    # Lister les fichiers uploadés
    files = []
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(path):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(path)
                })
    except OSError:
        files = []
    
    return render_template('index.html', reminders=reminders, links=links, files=files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Mot de passe incorrect', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('Aucun fichier sélectionné', 'error')
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Fichier uploadé avec succès', 'success')
    
    return redirect(url_for('index'))

@app.route('/delete_file/<filename>')
@login_required
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Fichier supprimé avec succès', 'success')
    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/add_reminder', methods=['POST'])
@login_required
def add_reminder():
    title = request.form.get('title', '').strip()
    date = request.form.get('date', '')
    time = request.form.get('time', '')
    alert_before = request.form.get('alert_before', '')
    alert_unit = request.form.get('alert_unit', 'hours')
    
    # Validation des données
    if not all([title, date, time, alert_before]):
        flash('Tous les champs sont requis', 'error')
        return redirect(url_for('index'))
    
    try:
        # Validation de la date et heure
        reminder_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        
        # Validation de l'alerte
        if not alert_before.isdigit() or int(alert_before) <= 0:
            flash('La valeur d\'alerte doit être un nombre positif', 'error')
            return redirect(url_for('index'))
        
        # Calculer le moment de l'alerte
        alert_before_int = int(alert_before)
        if alert_unit == 'minutes':
            alert_time = reminder_datetime - timedelta(minutes=alert_before_int)
        elif alert_unit == 'hours':
            alert_time = reminder_datetime - timedelta(hours=alert_before_int)
        else:  # days
            alert_time = reminder_datetime - timedelta(days=alert_before_int)
        
        new_reminder = {
            'id': datetime.now().strftime("%Y%m%d%H%M%S"),
            'title': title,
            'datetime': reminder_datetime.strftime("%Y-%m-%d %H:%M"),
            'alert_time': alert_time.strftime("%Y-%m-%d %H:%M"),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        try:
            with open('reminders.json', 'r', encoding='utf-8') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reminders = []
        
        reminders.append(new_reminder)
        
        with open('reminders.json', 'w', encoding='utf-8') as f:
            json.dump(reminders, f, indent=4, ensure_ascii=False)
        
        flash('Rappel ajouté avec succès', 'success')
    except ValueError as e:
        flash('Format de date/heure invalide', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_reminder/<reminder_id>')
@login_required
def delete_reminder(reminder_id):
    try:
        with open('reminders.json', 'r', encoding='utf-8') as f:
            reminders = json.load(f)
        
        original_count = len(reminders)
        reminders = [r for r in reminders if r['id'] != reminder_id]
        
        if len(reminders) == original_count:
            flash('Rappel non trouvé', 'error')
        else:
            with open('reminders.json', 'w', encoding='utf-8') as f:
                json.dump(reminders, f, indent=4, ensure_ascii=False)
            flash('Rappel supprimé avec succès', 'success')
    except (FileNotFoundError, json.JSONDecodeError):
        flash('Erreur lors du chargement des rappels', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/add_link', methods=['POST'])
@login_required
def add_link():
    name = request.form.get('name', '').strip()
    url = request.form.get('url', '').strip()
    
    # Validation des données
    if not all([name, url]):
        flash('Nom et URL sont requis', 'error')
        return redirect(url_for('index'))
    
    # Ajouter le protocole si nécessaire
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    new_link = {
        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
        'name': name,
        'url': url
    }
    
    try:
        try:
            with open('links.json', 'r', encoding='utf-8') as f:
                links = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            links = []
        
        links.append(new_link)
        
        with open('links.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=4, ensure_ascii=False)
        
        flash('Lien ajouté avec succès', 'success')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_link/<link_id>')
@login_required
def delete_link(link_id):
    try:
        with open('links.json', 'r', encoding='utf-8') as f:
            links = json.load(f)
        
        original_count = len(links)
        links = [l for l in links if l['id'] != link_id]
        
        if len(links) == original_count:
            flash('Lien non trouvé', 'error')
        else:
            with open('links.json', 'w', encoding='utf-8') as f:
                json.dump(links, f, indent=4, ensure_ascii=False)
            flash('Lien supprimé avec succès', 'success')
    except (FileNotFoundError, json.JSONDecodeError):
        flash('Erreur lors du chargement des liens', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/check_reminders')
@login_required
def check_reminders():
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        try:
            with open('reminders.json', 'r', encoding='utf-8') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return jsonify({'alerts': []})
        
        alerts = []
        for reminder in reminders:
            try:
                if reminder['alert_time'] <= now <= reminder['datetime']:
                    alerts.append({
                        'title': reminder['title'],
                        'time': reminder['datetime']
                    })
            except KeyError:
                # Ignorer les rappels avec des champs manquants
                continue
        
        return jsonify({'alerts': alerts})
    except Exception as e:
        return jsonify({'alerts': [], 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)