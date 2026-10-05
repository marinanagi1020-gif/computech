from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import os
import json

app = Flask(__name__)

# Image folder on Desktop or local directory
IMAGE_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop", "images")
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Data storage file (JSON)
DATA_FILE = "computech_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "reviews": [],
            "maintenance_requests": [],
            "cart": []
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Main Customer View Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compu Tech - Center & Maintenance</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; margin: 0; padding: 0; }
        header { background-color: #1f1f1f; padding: 20px; text-align: center; border-bottom: 2px solid #00adb5; }
        h1 { margin: 0; color: #00adb5; }
        nav { display: flex; justify-content: center; background-color: #222831; padding: 10px; gap: 15px; flex-wrap: wrap; }
        nav button { background-color: #393e46; color: #eeeeee; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        nav button:hover { background-color: #00adb5; }
        .container { padding: 20px; max-width: 1200px; margin: auto; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
        .card { background-color: #1e1e1e; border: 1px solid #333; border-radius: 8px; padding: 15px; text-align: center; }
        .price { color: #00adb5; font-size: 18px; font-weight: bold; margin: 10px 0; }
        .btn { background-color: #00adb5; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; }
        .btn:hover { background-color: #008c9e; }
        .section { display: none; }
        .active { display: block; }
        footer { text-align: center; padding: 15px; background-color: #1f1f1f; margin-top: 30px; color: #888; }
    </style>
</head>
<body>

<header>
    <h1>Compu Tech Center</h1>
    <p>Laptops | Accessories | Security Systems | Hardware Repair</p>
</header>

<nav>
    <button onclick="showSection('laptops')">💻 Laptops & Repair</button>
    <button onclick="showSection('accessories')">🎧 Mobile & PC Tech</button>
    <button onclick="showSection('security')">📹 Security Systems</button>
    <button onclick="showSection('reviews')">⭐ Reviews</button>
    <a href="/admin" style="text-decoration:none;"><button style="background-color:#d9534f;">🔒 Admin Panel</button></a>
</nav>

<div class="container">
    <!-- Laptops Section -->
    <div id="laptops" class="section active">
        <h2>Laptops & Maintenance Services</h2>
        <div class="grid">
            <div class="card">
                <h3>Dell Latitude Workstation</h3>
                <p>Core i7 - 16GB RAM - 512GB SSD</p>
                <div class="price">$550</div>
                <button class="btn">Add to Cart</button>
            </div>
            <div class="card">
                <h3>HP ProBook Series</h3>
                <p>Core i5 - 8GB RAM - 256GB SSD</p>
                <div class="price">$420</div>
                <button class="btn">Add to Cart</button>
            </div>
        </div>

        <h3 style="margin-top: 40px;">Book Maintenance Service</h3>
        <form action="/request_maintenance" method="POST" style="background:#1e1e1e; padding:15px; border-radius:8px; max-width:500px;">
            <input type="text" name="client_name" placeholder="Client Name" required style="width:96%; padding:8px; margin-bottom:10px;"><br>
            <input type="text" name="device_model" placeholder="Device Model" required style="width:96%; padding:8px; margin-bottom:10px;"><br>
            <textarea name="issue" placeholder="Describe hardware or software issue..." required style="width:96%; padding:8px; height:80px; margin-bottom:10px;"></textarea><br>
            <button type="submit" class="btn">Submit Maintenance Request</button>
        </form>
    </div>

    <!-- Accessories Section -->
    <div id="accessories" class="section">
        <h2>Mobile & Computer Accessories</h2>
        <p>High quality cables, chargers, power banks, mice, keyboards & storage drives.</p>
        <div class="grid">
            <div class="card">
                <h3>Gaming Mechanical Keyboard</h3>
                <p>RGB Backlit - Blue Switches</p>
                <div class="price">$35</div>
                <button class="btn">Add to Cart</button>
            </div>
            <div class="card">
                <h3>Fast Charger Power Bank 20000mAh</h3>
                <p>PD 22.5W Fast Charging</p>
                <div class="price">$28</div>
                <button class="btn">Add to Cart</button>
            </div>
        </div>
    </div>

    <!-- Security Systems Section -->
    <div id="security" class="section">
        <h2>Security Cameras & Surveillance</h2>
        <div class="grid">
            <div class="card">
                <h3>Outdoor IP Camera 4K</h3>
                <p>Night Vision - Motion Detection</p>
                <div class="price">$65</div>
                <button class="btn">Add to Cart</button>
            </div>
        </div>
    </div>

    <!-- Reviews Section -->
    <div id="reviews" class="section">
        <h2>Customer Reviews</h2>
        <form action="/add_review" method="POST" style="background:#1e1e1e; padding:15px; border-radius:8px; max-width:500px; margin-bottom:20px;">
            <input type="text" name="user_name" placeholder="Your Name" required style="width:96%; padding:8px; margin-bottom:10px;"><br>
            <textarea name="review_text" placeholder="Write your review..." required style="width:96%; padding:8px; height:60px; margin-bottom:10px;"></textarea><br>
            <button type="submit" class="btn">Submit Review (Pending Admin Approval)</button>
        </form>

        <h3>Approved Reviews:</h3>
        {% for review in reviews %}
            {% if review.approved %}
                <div style="background:#222; padding:10px; border-radius:5px; margin-bottom:10px;">
                    <strong>{{ review.user_name }}:</strong> {{ review.review_text }}
                </div>
            {% endif %}
        {% endfor %}
    </div>
</div>

<footer>
    &copy; 2026 Compu Tech Center - Managed by Eng. Rami & Ricardo
</footer>

<script>
    function showSection(id) {
        document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
        document.getElementById(id).classList.add('active');
    }
</script>
</body>
</html>
"""

# Admin Panel Template (Eng. Rami & Ricardo)
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Compu Tech - Admin Panel</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; padding: 20px; }
        .box { background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .btn-approve { background: #4CAF50; color: white; border: none; padding: 6px 12px; cursor: pointer; border-radius: 4px; }
        .btn-delete { background: #f44336; color: white; border: none; padding: 6px 12px; cursor: pointer; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🔒 Compu Tech Admin Dashboard</h1>
    <p>Manager Access: Eng. Rami & Ricardo</p>
    <a href="/" style="color:#00adb5; font-weight:bold;">← Return to Main Store View</a>
    
    <h2>Pending Reviews for Approval</h2>
    <div class="box">
        {% for idx, review in enumerate(data.reviews) %}
            {% if not review.approved %}
                <p><strong>{{ review.user_name }}:</strong> {{ review.review_text }}</p>
                <a href="/approve_review/{{ idx }}"><button class="btn-approve">Approve</button></a>
                <a href="/delete_review/{{ idx }}"><button class="btn-delete">Delete</button></a>
                <hr style="border-color:#333;">
            {% endif %}
        {% endfor %}
    </div>

    <h2>Active Maintenance Requests</h2>
    <div class="box">
        {% for req in data.maintenance_requests %}
            <p><strong>Client:</strong> {{ req.client_name }} | <strong>Device Model:</strong> {{ req.device_model }}</p>
            <p><strong>Issue Description:</strong> {{ req.issue }}</p>
            <hr style="border-color:#333;">
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    data = load_data()
    return render_template_string(HTML_TEMPLATE, reviews=data["reviews"])

@app.route('/admin')
def admin():
    data = load_data()
    return render_template_string(ADMIN_TEMPLATE, data=data, enumerate=enumerate)

@app.route('/add_review', methods=['POST'])
def add_review():
    data = load_data()
    user_name = request.form.get('user_name')
    review_text = request.form.get('review_text')
    data["reviews"].append({"user_name": user_name, "review_text": review_text, "approved": False})
    save_data(data)
    return redirect(url_for('home'))

@app.route('/approve_review/<int:idx>')
def approve_review(idx):
    data = load_data()
    if 0 <= idx < len(data["reviews"]):
        data["reviews"][idx]["approved"] = True
        save_data(data)
    return redirect(url_for('admin'))

@app.route('/delete_review/<int:idx>')
def delete_review(idx):
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
