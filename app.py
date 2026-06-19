import os
import sqlite3
import json
from datetime import datetime
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

app = Flask(
    __name__,
    static_folder='assets',      # Use the existing assets directory for static files
    static_url_path='/assets'    # Serve static files at /assets/...
)
app.secret_key = 'loadalytic_kragbridge_key_2026'

DATABASE = 'kragbridge.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Create database and seed if it doesn't exist
    db_exists = os.path.exists(DATABASE)
    conn = get_db()
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            plan TEXT NOT NULL,
            limit_kwh REAL NOT NULL,
            usage_kwh REAL DEFAULT 0,
            status TEXT DEFAULT 'Active',
            email TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT NOT NULL,
            date TEXT NOT NULL,
            severity TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            audience TEXT NOT NULL,
            body TEXT NOT NULL,
            status TEXT NOT NULL,
            sent_at TEXT NOT NULL,
            count INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            kwh REAL NOT NULL
        )
    ''')
    
    if not db_exists or len(cursor.execute("SELECT * FROM users").fetchall()) == 0:
        # Seed Users
        users_data = [
            ("Apex Industrial", "Enterprise", 1000.0, 300.0, "Active", "admin@apex.com"),
            ("Lumina Corp", "Premium", 5000.0, 2200.0, "Active", "info@lumina.co"),
            ("Vortex Data", "Basic", 250.0, 99.0, "Active", "billing@vortex.net"),
            ("Nova Energy", "Premium", 1200.0, 450.0, "Active", "contact@nova.io"),
            ("Solar Plexus", "Basic", 100.0, 15.0, "Suspended", "user@solarplexus.com"),
        ]
        cursor.executemany(
            "INSERT INTO users (name, plan, limit_kwh, usage_kwh, status, email) VALUES (?, ?, ?, ?, ?, ?)",
            users_data
        )
        
        # Seed News
        news_data = [
            ("Grid Maintenance scheduled for Sector 4", "02.07.2023", "Active"),
            ("High demand alert: load reduction active", "06.07.2023", "Active"),
            ("Solar power buyback rates increased by 5%", "18.06.2026", "Active")
        ]
        cursor.executemany(
            "INSERT INTO news (headline, date, severity) VALUES (?, ?, ?)",
            news_data
        )
        
        # Seed Energy Readings (Last 7 Days)
        energy_data = [
            ("Mon", 1500.0),
            ("Tue", 1800.0),
            ("Wed", 1400.0),
            ("Thu", 2200.0),
            ("Fri", 1900.0),
            ("Sat", 2500.0),
            ("Sun", 1800.0),
        ]
        cursor.executemany(
            "INSERT INTO energy_log (timestamp, kwh) VALUES (?, ?)",
            energy_data
        )
        
        # Seed Emails (Initial History)
        emails_data = [
            ("Monthly Tariff Updates", "All Clients", "Dear Clients, please note that the winter tariffs will take effect starting next month.", "Sent", "2026-06-01 10:00:00", 5),
            ("Premium Rewards Program", "Premium", "Exclusive offers and discounts for our premium energy tier users.", "Sent", "2026-06-10 14:30:00", 2)
        ]
        cursor.executemany(
            "INSERT INTO emails (subject, audience, body, status, sent_at, count) VALUES (?, ?, ?, ?, ?, ?)",
            emails_data
        )
        
    conn.commit()
    conn.close()

# Initialize Database
init_db()

# --- Customer Facing Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    success = False
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        print(f"Contact form submitted by: {name} <{email}>, Phone: {phone}, Message: {message}")
        success = True
    return render_template('contact.html', success=success)

# --- Admin Section Helper ---
def is_logged_in():
    return session.get('admin_logged_in', False)

# --- Admin Routes ---
@app.route('/admin')
@app.route('/admin/')
@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # Retrieve active grid status
    grid_status = session.get('grid_status', 'Active')
    
    # Fetch lists
    users = cursor.execute("SELECT * FROM users").fetchall()
    news = cursor.execute("SELECT * FROM news ORDER BY id DESC LIMIT 5").fetchall()
    energy_logs = cursor.execute("SELECT * FROM energy_log ORDER BY id DESC LIMIT 7").fetchall()
    # Reverse to show chronological order
    energy_logs = list(reversed(energy_logs))
    
    # Calculate stats
    total_usage = sum([u['usage_kwh'] for u in users])
    total_limit = sum([u['limit_kwh'] for u in users])
    active_clients = len([u for u in users if u['status'] == 'Active'])
    
    # Formatting analytics to match user layout (e.g. MWh, Active count, Revenue)
    total_mwh = round(total_usage / 1000.0, 2)
    # Revenue: say R2.50 per kWh, scale to match mockup 4.5M if we want, or make it dynamic
    revenue_calc = round((total_usage * 1.48) / 1000.0, 2) # in Millions or Thousands depending on scale, let's match the 4.5M aesthetic or show R x.xx M
    
    # Prepare charts data
    chart_dates = [log['timestamp'] for log in energy_logs]
    chart_values = [log['kwh'] for log in energy_logs]
    
    client_names = [u['name'] for u in users if u['status'] == 'Active']
    client_values = [u['usage_kwh'] for u in users if u['status'] == 'Active']
    
    # Fetch news severity mapping count
    active_news_count = len(news)
    
    # Fetch dispatch email counts
    email_count = len(cursor.execute("SELECT * FROM emails").fetchall())
    
    conn.close()
    
    return render_template(
        'admin/dashboard.html',
        users=users,
        news=news,
        grid_status=grid_status,
        total_mwh=total_mwh,
        active_clients=active_clients,
        revenue=revenue_calc,
        chart_dates=json.dumps(chart_dates),
        chart_values=json.dumps(chart_values),
        client_names=json.dumps(client_names),
        client_values=json.dumps(client_values),
        logged_in=is_logged_in()
    )

@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    
    # Mock authentication checks
    if username == 'admin' and password == 'admin123':
        session['admin_logged_in'] = True
        session['admin_role'] = role or 'Admin'
        session['grid_status'] = 'Active'
        flash('Successfully authenticated.', 'success')
    else:
        flash('Invalid username or password.', 'error')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_role', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users')
def admin_users_page():
    if not is_logged_in():
        flash('Please login to access this section.', 'warning')
        return redirect(url_for('admin_dashboard'))
        
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template('admin/users.html', users=users, logged_in=is_logged_in())

@app.route('/admin/users/add', methods=['POST'])
def admin_add_user():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    name = request.form.get('name')
    email = request.form.get('email')
    plan = request.form.get('plan')
    limit_kwh = request.form.get('limit_kwh', type=float)
    usage_kwh = request.form.get('usage_kwh', default=0.0, type=float)
    status = request.form.get('status', default='Active')
    
    if not name or not email or not plan or limit_kwh is None:
        flash('All fields are required.', 'error')
        return redirect(url_for('admin_users_page'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, plan, limit_kwh, usage_kwh, status, email) VALUES (?, ?, ?, ?, ?, ?)",
        (name, plan, limit_kwh, usage_kwh, status, email)
    )
    conn.commit()
    conn.close()
    
    flash(f'Client {name} successfully added.', 'success')
    return redirect(url_for('admin_users_page'))

@app.route('/admin/users/edit/<int:user_id>', methods=['POST'])
def admin_edit_user(user_id):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    name = request.form.get('name')
    email = request.form.get('email')
    plan = request.form.get('plan')
    limit_kwh = request.form.get('limit_kwh', type=float)
    usage_kwh = request.form.get('usage_kwh', type=float)
    status = request.form.get('status')
    
    if not name or not email or not plan or limit_kwh is None or usage_kwh is None or not status:
        flash('All fields are required.', 'error')
        return redirect(url_for('admin_users_page'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name=?, plan=?, limit_kwh=?, usage_kwh=?, status=?, email=? WHERE id=?",
        (name, plan, limit_kwh, usage_kwh, status, email, user_id)
    )
    conn.commit()
    conn.close()
    
    flash(f'Client {name} details updated.', 'success')
    return redirect(url_for('admin_users_page'))

@app.route('/admin/users/toggle/<int:user_id>', methods=['POST'])
def admin_toggle_user(user_id):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if user:
        new_status = 'Suspended' if user['status'] == 'Active' else 'Active'
        cursor.execute("UPDATE users SET status=? WHERE id=?", (new_status, user_id))
        conn.commit()
        flash(f"Client {user['name']} status set to {new_status}.", 'info')
    conn.close()
    return redirect(url_for('admin_users_page'))

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if user:
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        flash(f"Client {user['name']} removed from the grid.", 'warning')
    conn.close()
    return redirect(url_for('admin_users_page'))

@app.route('/admin/news')
def admin_news_page():
    if not is_logged_in():
        flash('Please login to access this section.', 'warning')
        return redirect(url_for('admin_dashboard'))
        
    conn = get_db()
    news = conn.execute("SELECT * FROM news ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('admin/news.html', news=news, logged_in=is_logged_in())

@app.route('/admin/news/add', methods=['POST'])
def admin_add_news():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    headline = request.form.get('headline')
    severity = request.form.get('severity', default='Active')
    
    if not headline:
        flash('Headline content cannot be empty.', 'error')
        return redirect(url_for('admin_news_page'))
        
    date_str = datetime.now().strftime("%d.%m.%Y")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO news (headline, date, severity) VALUES (?, ?, ?)", (headline, date_str, severity))
    conn.commit()
    conn.close()
    
    flash('Headline published to system bulletins.', 'success')
    return redirect(url_for('admin_news_page'))

@app.route('/admin/news/delete/<int:news_id>', methods=['POST'])
def admin_delete_news(news_id):
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE id=?", (news_id,))
    conn.commit()
    conn.close()
    
    flash('Bulletin article removed.', 'info')
    return redirect(url_for('admin_news_page'))

@app.route('/admin/marketing')
def admin_marketing_page():
    if not is_logged_in():
        flash('Please login to access this section.', 'warning')
        return redirect(url_for('admin_dashboard'))
        
    conn = get_db()
    emails = conn.execute("SELECT * FROM emails ORDER BY id DESC").fetchall()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    
    # Calculate recipient segments counts
    counts = {
        'All Clients': len(users),
        'Premium': len([u for u in users if u['plan'] == 'Premium']),
        'Enterprise': len([u for u in users if u['plan'] == 'Enterprise']),
        'Basic': len([u for u in users if u['plan'] == 'Basic']),
        'Suspended': len([u for u in users if u['status'] == 'Suspended'])
    }
    
    return render_template('admin/marketing.html', emails=emails, counts=counts, logged_in=is_logged_in())

@app.route('/admin/marketing/send', methods=['POST'])
def admin_send_marketing():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    subject = request.form.get('subject')
    audience = request.form.get('audience')
    body = request.form.get('body')
    
    if not subject or not audience or not body:
        flash('Subject, audience, and email body are required.', 'error')
        return redirect(url_for('admin_marketing_page'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    # Calculate target audience count
    users = cursor.execute("SELECT * FROM users").fetchall()
    if audience == 'All Clients':
        target_users = users
    elif audience in ['Basic', 'Premium', 'Enterprise']:
        target_users = [u for u in users if u['plan'] == audience]
    elif audience == 'Suspended':
        target_users = [u for u in users if u['status'] == 'Suspended']
    else:
        target_users = users
        
    recipient_count = len(target_users)
    
    # Log email dispatch to db
    sent_at_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO emails (subject, audience, body, status, sent_at, count) VALUES (?, ?, ?, ?, ?, ?)",
        (subject, audience, body, 'Sent', sent_at_str, recipient_count)
    )
    conn.commit()
    conn.close()
    
    flash(f"Campaign dispatched successfully! {recipient_count} emails queued.", 'success')
    return redirect(url_for('admin_marketing_page'))

# --- Simulation Endpoints ---
@app.route('/admin/simulate-usage', methods=['POST'])
def admin_simulate_usage():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = get_db()
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM users").fetchall()
    
    # Fluctuate usage randomly (between -15% and +30% for realistic load change)
    for u in users:
        if u['status'] == 'Active':
            factor = random.uniform(0.85, 1.35)
            new_usage = round(u['usage_kwh'] * factor, 2)
            # Cap at 115% of daily limit
            limit = u['limit_kwh']
            if new_usage > limit * 1.15:
                new_usage = round(limit * 1.12, 2)
            cursor.execute("UPDATE users SET usage_kwh=? WHERE id=?", (new_usage, u['id']))
            
    # Add new entry to the energy log
    users_updated = cursor.execute("SELECT * FROM users WHERE status='Active'").fetchall()
    total_active_usage = sum([u['usage_kwh'] for u in users_updated])
    
    # Insert new hourly/daily reading
    # Remove oldest reading to maintain 7 days window (Mon-Sun)
    oldest = cursor.execute("SELECT id FROM energy_log ORDER BY id ASC LIMIT 1").fetchone()
    if oldest:
        # Just update usage for the current timestamp/last entry or append
        # Let's update the last entry to keep it at 7 entries, or insert a new one and delete the first
        cursor.execute("DELETE FROM energy_log WHERE id=?", (oldest['id'],))
        
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # Get last reading timestamp and pick the next day
    latest = cursor.execute("SELECT timestamp FROM energy_log ORDER BY id DESC LIMIT 1").fetchone()
    next_day = "Mon"
    if latest:
        try:
            curr_idx = days.index(latest['timestamp'])
            next_day = days[(curr_idx + 1) % len(days)]
        except ValueError:
            next_day = "Mon"
            
    cursor.execute("INSERT INTO energy_log (timestamp, kwh) VALUES (?, ?)", (next_day, round(total_active_usage, 2)))
    
    conn.commit()
    conn.close()
    
    flash("Simulation executed: client usage loads updated.", 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/set-grid-status', methods=['POST'])
def admin_set_grid_status():
    if not is_logged_in():
        return jsonify({'error': 'Unauthorized'}), 401
        
    status = request.form.get('grid_status')
    if status in ['Active', 'Warning', 'Loadshedding', 'Critical']:
        session['grid_status'] = status
        flash(f"Grid state successfully updated to: {status}", 'info')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

