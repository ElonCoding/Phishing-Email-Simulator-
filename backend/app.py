from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import json
import random
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your-secret-key-here-change-in-production'

# Database initialization
def init_db():
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT,
            role TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Phishing campaigns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            email_template TEXT NOT NULL,
            subject_line TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            sender_email TEXT NOT NULL,
            difficulty_level TEXT CHECK(difficulty_level IN ('easy', 'medium', 'hard')),
            attack_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    # Campaign recipients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            user_id INTEGER,
            email_sent BOOLEAN DEFAULT FALSE,
            email_opened BOOLEAN DEFAULT FALSE,
            link_clicked BOOLEAN DEFAULT FALSE,
            credentials_submitted BOOLEAN DEFAULT FALSE,
            response_time INTEGER,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Phishing email templates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            subject TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            sender_email TEXT NOT NULL,
            email_content TEXT NOT NULL,
            landing_page_template TEXT,
            difficulty_level TEXT CHECK(difficulty_level IN ('easy', 'medium', 'hard')),
            attack_vector TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            total_recipients INTEGER DEFAULT 0,
            emails_sent INTEGER DEFAULT 0,
            emails_opened INTEGER DEFAULT 0,
            links_clicked INTEGER DEFAULT 0,
            credentials_submitted INTEGER DEFAULT 0,
            open_rate REAL DEFAULT 0,
            click_rate REAL DEFAULT 0,
            conversion_rate REAL DEFAULT 0,
            avg_response_time INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Phishing email templates
PHISHING_TEMPLATES = [
    {
        'name': 'Urgent Password Reset',
        'category': 'credential_harvesting',
        'subject': '⚠️ Urgent: Your account will be locked in 24 hours',
        'sender_name': 'IT Security Team',
        'sender_email': 'security@company.com',
        'difficulty': 'easy',
        'attack_vector': 'fear_urgency',
        'content': '''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #d32f2f;">🚨 URGENT: Account Security Alert</h2>
            <p>Dear {name},</p>
            <p>Our security system has detected <strong>suspicious activity</strong> on your account. To prevent unauthorized access, you must verify your identity immediately.</p>
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; margin: 20px 0; border-radius: 5px;">
                <p><strong>Action Required:</strong> Click the link below to verify your account within the next 24 hours.</p>
            </div>
            <p style="text-align: center;">
                <a href="{phishing_link}" style="background-color: #d32f2f; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">VERIFY ACCOUNT NOW</a>
            </p>
            <p><em>Failure to verify your account will result in immediate suspension.</em></p>
            <p>Best regards,<br>IT Security Team</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 12px; color: #666;">This is an automated security notification. Please do not reply to this email.</p>
        </div>
        ''',
        'landing_page': '''
        <div style="font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #d32f2f; text-align: center;">Account Verification</h2>
            <p style="text-align: center;">Enter your credentials to verify your identity:</p>
            <form method="POST" action="/submit-credentials">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px;">Username:</label>
                    <input type="text" name="username" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px;">Password:</label>
                    <input type="password" name="password" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                <button type="submit" style="width: 100%; background-color: #d32f2f; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer;">VERIFY ACCOUNT</button>
            </form>
        </div>
        '''
    },
    {
        'name': 'CEO Request',
        'category': 'business_email_compromise',
        'subject': 'Urgent request from {ceo_name}',
        'sender_name': '{ceo_name}',
        'sender_email': '{ceo_email}',
        'difficulty': 'medium',
        'attack_vector': 'authority_impersonation',
        'content': '''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <p>{name},</p>
            <p>I need you to handle a confidential matter for me today. I'm currently in meetings and cannot take calls.</p>
            <p>I need you to purchase 10 gift cards ($100 each) for client gifts. Purchase them from any store and send me the codes immediately.</p>
            <p>I will reimburse you as soon as I'm back in the office.</p>
            <p>Please confirm receipt and let me know when this is completed.</p>
            <p>Best,<br>{ceo_name}</p>
            <p style="font-size: 12px; color: #666;">Sent from my mobile device</p>
        </div>
        ''',
        'landing_page': '''
        <div style="font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="text-align: center;">Gift Card Submission</h2>
            <p>Please enter the gift card codes below:</p>
            <form method="POST" action="/submit-giftcards">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px;">Gift Card Codes (one per line):</label>
                    <textarea name="giftcard_codes" rows="5" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;"></textarea>
                </div>
                <button type="submit" style="width: 100%; background-color: #007bff; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer;">SUBMIT CODES</button>
            </form>
        </div>
        '''
    },
    {
        'name': 'Package Delivery',
        'category': 'shipping_notification',
        'subject': 'Package delivery failed - Action required',
        'sender_name': 'FedEx Delivery',
        'sender_email': 'notifications@fedex.com',
        'difficulty': 'easy',
        'attack_vector': 'curiosity_urgency',
        'content': '''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <img src="https://via.placeholder.com/150x50/4F7AC4/FFFFFF?text=FedEx" alt="FedEx Logo" style="display: block; margin: 0 auto 20px;">
            <h2 style="color: #4F7AC4;">Delivery Notification</h2>
            <p>Dear {name},</p>
            <p>We attempted to deliver your package but no one was available to receive it.</p>
            <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; margin: 20px 0; border-radius: 5px;">
                <p><strong>Tracking Number:</strong> {tracking_number}</p>
                <p><strong>Delivery Address:</strong> {address}</p>
                <p><strong>Delivery Date:</strong> {delivery_date}</p>
            </div>
            <p>To reschedule your delivery, please click the link below:</p>
            <p style="text-align: center;">
                <a href="{phishing_link}" style="background-color: #4F7AC4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">RESCHEDULE DELIVERY</a>
            </p>
            <p>Please note: Packages not rescheduled within 48 hours will be returned to sender.</p>
            <p>Thank you for choosing FedEx.</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="font-size: 12px; color: #666;">This is an automated delivery notification from FedEx Corporation.</p>
        </div>
        ''',
        'landing_page': '''
        <div style="font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 30px; border: 1px solid #ddd; border-radius: 8px;">
            <h2 style="color: #4F7AC4; text-align: center;">Reschedule Delivery</h2>
            <p>Please confirm your delivery details:</p>
            <form method="POST" action="/submit-delivery">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px;">Full Name:</label>
                    <input type="text" name="full_name" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px;">Phone Number:</label>
                    <input type="text" name="phone" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px;">Preferred Delivery Date:</label>
                    <input type="date" name="delivery_date" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
                </div>
                <button type="submit" style="width: 100%; background-color: #4F7AC4; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer;">CONFIRM DELIVERY</button>
            </form>
        </div>
        '''
    }
]

# Routes
@app.route('/')
def index():
    return render_template('simulator/index.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator/simulator.html')

@app.route('/admin')
def admin():
    return render_template('simulator/admin.html')

@app.route('/analytics')
def analytics():
    return render_template('simulator/analytics.html')

@app.route('/about')
def about_page():
    return render_template('simulator/about.html')

@app.route('/projects')
def projects_page():
    return render_template('simulator/projects.html')

# API Routes
@app.route('/api/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        conn = sqlite3.connect('phishing_simulation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        conn.close()
        
        user_list = []
        for user in users:
            user_list.append({
                'id': user[0],
                'email': user[1],
                'name': user[2],
                'department': user[3],
                'role': user[4],
                'created_at': user[5]
            })
        
        return jsonify(user_list)
    
    elif request.method == 'POST':
        data = request.json
        conn = sqlite3.connect('phishing_simulation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (email, name, department, role)
            VALUES (?, ?, ?, ?)
        ''', (data['email'], data['name'], data['department'], data['role']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'User added successfully'}), 201

@app.route('/api/templates', methods=['GET'])
def get_templates():
    return jsonify(PHISHING_TEMPLATES)

@app.route('/api/campaigns', methods=['GET', 'POST'])
def manage_campaigns():
    if request.method == 'GET':
        conn = sqlite3.connect('phishing_simulation.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, COUNT(cr.id) as recipient_count
            FROM campaigns c
            LEFT JOIN campaign_recipients cr ON c.id = cr.campaign_id
            GROUP BY c.id
            ORDER BY c.created_at DESC
        ''')
        campaigns = cursor.fetchall()
        conn.close()
        
        campaign_list = []
        for campaign in campaigns:
            campaign_list.append({
                'id': campaign[0],
                'name': campaign[1],
                'description': campaign[2],
                'email_template': campaign[3],
                'subject_line': campaign[4],
                'sender_name': campaign[5],
                'sender_email': campaign[6],
                'difficulty_level': campaign[7],
                'attack_type': campaign[8],
                'status': campaign[10],
                'recipient_count': campaign[11]
            })
        
        return jsonify(campaign_list)
    
    elif request.method == 'POST':
        data = request.json
        conn = sqlite3.connect('phishing_simulation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO campaigns (name, description, email_template, subject_line, sender_name, sender_email, difficulty_level, attack_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['description'], data['email_template'], data['subject_line'], 
              data['sender_name'], data['sender_email'], data['difficulty_level'], data['attack_type']))
        
        campaign_id = cursor.lastrowid
        
        # Add recipients
        for user_id in data['recipients']:
            cursor.execute('''
                INSERT INTO campaign_recipients (campaign_id, user_id)
                VALUES (?, ?)
            ''', (campaign_id, user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Campaign created successfully', 'id': campaign_id}), 201

@app.route('/api/seed-users', methods=['POST'])
def seed_users():
    sample = [
        ('alice@example.com','Alice Johnson','Finance','Analyst'),
        ('bob@example.com','Bob Smith','Engineering','Developer'),
        ('carol@example.com','Carol Lee','HR','Coordinator'),
        ('dan@example.com','Dan Brown','Sales','Associate')
    ]
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    for email,name,dept,role in sample:
        try:
            cursor.execute('INSERT INTO users (email, name, department, role) VALUES (?,?,?,?)', (email,name,dept,role))
        except Exception:
            pass
    conn.commit()
    conn.close()
    return jsonify({'message':'Seeded users'}), 201

@app.route('/api/send-campaign/<int:campaign_id>', methods=['POST'])
def send_campaign(campaign_id):
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    
    # Update campaign status
    cursor.execute('UPDATE campaigns SET status = ? WHERE id = ?', ('sent', campaign_id))
    
    # Get campaign details
    cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
    campaign = cursor.fetchone()
    
    # Get recipients
    cursor.execute('''
        SELECT u.* FROM users u
        JOIN campaign_recipients cr ON u.id = cr.user_id
        WHERE cr.campaign_id = ?
    ''', (campaign_id,))
    recipients = cursor.fetchall()
    
    # Simulate sending emails (in real implementation, this would send actual emails)
    for recipient in recipients:
        cursor.execute('''
            UPDATE campaign_recipients 
            SET email_sent = TRUE 
            WHERE campaign_id = ? AND user_id = ?
        ''', (campaign_id, recipient[0]))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Campaign sent successfully'})

@app.route('/api/analytics/<int:campaign_id>')
def get_campaign_analytics(campaign_id):
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    
    # Get campaign statistics
    cursor.execute('''
        SELECT 
            COUNT(*) as total_recipients,
            SUM(CASE WHEN email_sent = TRUE THEN 1 ELSE 0 END) as emails_sent,
            SUM(CASE WHEN email_opened = TRUE THEN 1 ELSE 0 END) as emails_opened,
            SUM(CASE WHEN link_clicked = TRUE THEN 1 ELSE 0 END) as links_clicked,
            SUM(CASE WHEN credentials_submitted = TRUE THEN 1 ELSE 0 END) as credentials_submitted,
            AVG(response_time) as avg_response_time
        FROM campaign_recipients
        WHERE campaign_id = ?
    ''', (campaign_id,))
    
    stats = cursor.fetchone()
    
    # Calculate rates
    total = stats[0] if stats[0] > 0 else 1
    open_rate = (stats[2] / total) * 100 if total > 0 else 0
    click_rate = (stats[3] / total) * 100 if total > 0 else 0
    conversion_rate = (stats[4] / total) * 100 if total > 0 else 0
    
    analytics_data = {
        'total_recipients': stats[0],
        'emails_sent': stats[1],
        'emails_opened': stats[2],
        'links_clicked': stats[3],
        'credentials_submitted': stats[4],
        'open_rate': round(open_rate, 2),
        'click_rate': round(click_rate, 2),
        'conversion_rate': round(conversion_rate, 2),
        'avg_response_time': round(stats[5], 2) if stats[5] else 0
    }
    
    conn.close()
    
    return jsonify(analytics_data)

@app.route('/api/campaign-recipients/<int:campaign_id>')
def list_campaign_recipients(campaign_id):
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.id, u.name, u.email, cr.email_sent, cr.email_opened, cr.link_clicked, cr.credentials_submitted
        FROM users u
        JOIN campaign_recipients cr ON u.id = cr.user_id
        WHERE cr.campaign_id = ?
        ORDER BY cr.created_at ASC
    ''', (campaign_id,))
    rows = cursor.fetchall()
    conn.close()
    recipients = []
    for r in rows:
        recipients.append({
            'id': r[0],
            'name': r[1],
            'email': r[2],
            'email_sent': bool(r[3]),
            'email_opened': bool(r[4]),
            'link_clicked': bool(r[5]),
            'credentials_submitted': bool(r[6]),
        })
    return jsonify(recipients)

# Phishing simulation endpoints
@app.route('/track/open/<int:campaign_id>/<int:user_id>')
def track_email_open(campaign_id, user_id):
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE campaign_recipients 
        SET email_opened = TRUE, ip_address = ?, user_agent = ?
        WHERE campaign_id = ? AND user_id = ?
    ''', (request.remote_addr, request.headers.get('User-Agent'), campaign_id, user_id))
    
    conn.commit()
    conn.close()
    
    # Return a 1x1 transparent pixel
    return '', 204

@app.route('/phishing/<int:campaign_id>/<int:user_id>')
def phishing_landing_page(campaign_id, user_id):
    conn = sqlite3.connect('phishing_simulation.db')
    cursor = conn.cursor()
    
    # Track link click
    cursor.execute('''
        UPDATE campaign_recipients 
        SET link_clicked = TRUE, response_time = ?
        WHERE campaign_id = ? AND user_id = ?
    ''', (int(datetime.datetime.now().timestamp()), campaign_id, user_id))
    
    # Get campaign details
    cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
    campaign = cursor.fetchone()
    
    conn.commit()
    conn.close()
    
    # Render appropriate landing page based on campaign type
    return render_template('simulator/phishing_page.html', campaign=campaign, user_id=user_id)

@app.route('/submit-credentials', methods=['POST'])
def submit_credentials():
    # This would normally track credential submission
    # For demo purposes, we'll just show an educational message
    return render_template('simulator/educational_message.html', 
                         message='You have successfully identified this as a phishing attempt! Remember to always verify the sender and never enter credentials on suspicious websites.')

if __name__ == '__main__':
    app.run(debug=True, port=5000)