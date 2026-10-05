import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'computech_secret_key'

DATA_FILE = 'computech_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "services": [
                {"title": "Laptop & PC Maintenance", "description": "Screen, keyboard, and hardware repairs."},
                {"title": "Software & Updates", "description": "Original Windows, drivers, and setup."}
            ],
            "offers": [
                {"title": "20% Discount", "description": "Free internal cleaning with hardware maintenance."}
            ],
            "reviews": [],
            "maintenance_requests": []
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    data = load_data()
    approved_reviews = [r for r in data.get("reviews", []) if r.get("approved")]
    return render_template('index.html', services=data.get("services", []), offers=data.get("offers", []), reviews=approved_reviews)

@app.route('/add_review', methods=['POST'])
def add_review():
    data = load_data()
    name = request.form.get('name')
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    if name and comment:
        data["reviews"].append({
            "name": name,
            "comment": comment,
            "rating": rating,
            "approved": False
        })
        save_data(data)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '1234':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    return render_template('admin.html', data=data)

@app.route('/add_service', methods=['POST'])
def add_service():
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    title = request.form.get('title')
    description = request.form.get('description')
    if title and description:
        data["services"].append({"title": title, "description": description})
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/delete_service/<int:idx>')
def delete_service(idx):
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    if 0 <= idx < len(data["services"]):
        data["services"].pop(idx)
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/add_offer', methods=['POST'])
def add_offer():
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    title = request.form.get('title')
    description = request.form.get('description')
    if title and description:
        data["offers"].append({"title": title, "description": description})
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/delete_offer/<int:idx>')
def delete_offer(idx):
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    if 0 <= idx < len(data["offers"]):
        data["offers"].pop(idx)
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/approve_review/<int:idx>')
def approve_review(idx):
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    if 0 <= idx < len(data["reviews"]):
        data["reviews"][idx]["approved"] = True
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/delete_review/<int:idx>')
def delete_review(idx):
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    if 0 <= idx < len(data["reviews"]):
        data["reviews"].pop(idx)
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/request_maintenance', methods=['POST'])
def request_maintenance():
    data = load_data()
    client_name = request.form.get('client_name')
    device_model = request.form.get('device_model')
    issue = request.form.get('issue')
    data["maintenance_requests"].append({"client_name": client_name, "device_model": device_model, "issue": issue})
    save_data(data)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 
