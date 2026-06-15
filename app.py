import os
from flask import Flask, render_template, request, abort

app = Flask(
    __name__,
    static_folder='assets',      # Use the existing assets directory for static files
    static_url_path='/assets'    # Serve static files at /assets/...
)

# Resellers Finder Database
RESELLERS = [
    {
        "id": 1,
        "name": "VoltStream Energy",
        "rating": 4.9,
        "reviews": 182,
        "rate": 0.105,
        "energy_type": "100% Renewable (Wind & Solar)",
        "plan_type": "Fixed Rate",
        "contract_term": "12 Months",
        "features": ["No Sign-up Fees", "Smart Thermostat Integration", "Weekly Usage Reports"],
        "logo_color": "#029041",
        "phone": "+1 (800) 555-0199",
        "website": "https://voltstream.example.com"
    },
    {
        "id": 2,
        "name": "EcoCurrent Power",
        "rating": 4.8,
        "reviews": 94,
        "rate": 0.112,
        "energy_type": "100% Solar Energy",
        "plan_type": "Fixed Rate",
        "contract_term": "24 Months",
        "features": ["Free Nest Thermostat", "$50 Bill Credit", "Zero Carbon Footprint"],
        "logo_color": "#00c853",
        "phone": "+1 (800) 555-0142",
        "website": "https://ecocurrent.example.com"
    },
    {
        "id": 3,
        "name": "GridFlow Solutions",
        "rating": 4.6,
        "reviews": 230,
        "rate": 0.098,
        "energy_type": "Mix (60% Renewable, 40% Natural Gas)",
        "plan_type": "Variable Rate",
        "contract_term": "Month-to-Month",
        "features": ["No Cancellation Fees", "Paperless Billing Discount", "Budget Billing Option"],
        "logo_color": "#1b5e20",
        "phone": "+1 (800) 555-0187",
        "website": "https://gridflow.example.com"
    },
    {
        "id": 4,
        "name": "Apex Power Corp",
        "rating": 4.7,
        "reviews": 115,
        "rate": 0.108,
        "energy_type": "Mix (80% Renewable, 20% Hydro)",
        "plan_type": "Fixed Rate",
        "contract_term": "18 Months",
        "features": ["Price Protection Guarantee", "Refer-a-Friend Bonus", "24/7 Live Support"],
        "logo_color": "#4caf50",
        "phone": "+1 (800) 555-0123",
        "website": "https://apexpower.example.com"
    },
    {
        "id": 5,
        "name": "KiloWatt Co.",
        "rating": 4.5,
        "reviews": 78,
        "rate": 0.095,
        "energy_type": "Standard Mix",
        "plan_type": "Fixed Rate",
        "contract_term": "6 Months",
        "features": ["Low Intro Rate", "Simple Billing", "Auto-pay Discounts"],
        "logo_color": "#2e7d32",
        "phone": "+1 (800) 555-0155",
        "website": "https://kilowatt.example.com"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resellers')
@app.route('/resellers.html')
def resellers():
    query = request.args.get('q', '').strip()
    plan_type = request.args.get('plan_type', 'All').strip()
    energy_type = request.args.get('energy_type', 'All').strip()

    filtered = RESELLERS
    if query:
        q_lower = query.lower()
        filtered = [
            r for r in filtered
            if q_lower in r['name'].lower() or any(q_lower in f.lower() for f in r['features'])
        ]
    if plan_type != 'All':
        filtered = [r for r in filtered if r['plan_type'] == plan_type]
    if energy_type != 'All':
        if energy_type == 'Renewable':
            filtered = [r for r in filtered if 'Renewable' in r['energy_type'] or 'Solar' in r['energy_type']]
        elif energy_type == 'Mix':
            filtered = [r for r in filtered if 'Mix' in r['energy_type'] or 'Standard' in r['energy_type']]

    return render_template(
        'resellers.html',
        resellers=filtered,
        search_query=query,
        plan_type=plan_type,
        energy_type=energy_type
    )

# 1. OPERATIONS DASHBOARD ROUTE
@app.route('/dashboard')
@app.route('/dashboard.html')
def dashboard():
    kpis = {
        "energy_sold": {
            "value": "1.24 GWh",
            "trend": "+18.4%",
            "sparkline": [30, 40, 35, 50, 49, 60, 70, 91, 125, 124]
        },
        "revenue": {
            "value": "R4.8M",
            "trend": "+12.2%",
            "sparkline": [20, 24, 22, 28, 30, 32, 38, 42, 45, 48]
        },
        "properties": {
            "value": "248",
            "trend": "+7.1%",
            "sparkline": [210, 215, 220, 222, 228, 230, 235, 238, 242, 248]
        },
        "customers": {
            "value": "12,450",
            "trend": "+15.8%",
            "sparkline": [10100, 10300, 10500, 10800, 11000, 11200, 11500, 11800, 12100, 12450]
        }
    }

    analytics_data = {
        "Today": {
            "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
            "consumption": [120, 110, 340, 520, 480, 220],
            "production": [0, 10, 280, 590, 410, 20],
            "revenue": [5, 4, 18, 26, 22, 10]
        },
        "Week": {
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "consumption": [2400, 2600, 2500, 2800, 3100, 1900, 1700],
            "production": [1800, 1950, 2100, 1700, 2200, 2450, 2600],
            "revenue": [120, 130, 125, 140, 155, 95, 85]
        },
        "Month": {
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "consumption": [12500, 13100, 12800, 14200],
            "production": [11800, 12500, 13200, 12900],
            "revenue": [625, 655, 640, 710]
        },
        "Quarter": {
            "labels": ["Jan", "Feb", "Mar"],
            "consumption": [52000, 49000, 55000],
            "production": [45000, 48000, 51000],
            "revenue": [2600, 2450, 2750]
        },
        "Year": {
            "labels": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "consumption": [180, 195, 210, 205, 220, 240, 230, 215, 225, 210, 195, 185],
            "production": [150, 165, 180, 195, 210, 190, 175, 190, 215, 220, 210, 195],
            "revenue": [9.0, 9.8, 10.5, 10.3, 11.0, 12.0, 11.5, 10.8, 11.3, 10.5, 9.8, 9.3]
        }
    }

    performance = [
        {"name": "Solar Production", "percentage": 92, "status": "Peak Efficiency"},
        {"name": "Battery Storage", "percentage": 78, "status": "Charging"},
        {"name": "Carbon Offset", "percentage": 85, "status": "Optimal"},
        {"name": "Grid Feed-In", "percentage": 64, "status": "Active Flow"}
    ]

    properties = [
        {"name": "Green Oaks Estate", "usage": 89, "revenue": "R124k", "status": "Active"},
        {"name": "Riverside Mall", "usage": 74, "revenue": "R98k", "status": "Active"},
        {"name": "Tech Park West", "usage": 91, "revenue": "R152k", "status": "Active"},
        {"name": "Ocean View Apartments", "usage": 68, "revenue": "R72k", "status": "Active"},
        {"name": "Industrial Hub South", "usage": 94, "revenue": "R240k", "status": "Active"},
        {"name": "Metro Gateway Plaza", "usage": 82, "revenue": "R185k", "status": "Maintenance"}
    ]

    technicians = [
        {"name": "Sipho Ndlovu", "skills": "Solar, Batteries", "rating": 4.9, "jobs": 124, "availability": "Immediate", "avatar": "S"},
        {"name": "Emma Botha", "skills": "Smart Meters, Grid", "rating": 4.8, "jobs": 98, "availability": "Today", "avatar": "E"},
        {"name": "David Naidoo", "skills": "Solar, Microgrids", "rating": 4.7, "jobs": 143, "availability": "Scheduled", "avatar": "D"},
        {"name": "Thabo Mokoena", "skills": "Battery Storage", "rating": 4.9, "jobs": 62, "availability": "Immediate", "avatar": "T"}
    ]

    billing = {
        "outstanding_invoices": 18,
        "outstanding_amount": "R245,600",
        "payment_methods": [
            {"name": "EFT / Bank Transfer", "value": 55, "color": "#029041"},
            {"name": "Credit Card", "value": 25, "color": "#111111"},
            {"name": "Instant EFT", "value": 20, "color": "#00c853"}
        ],
        "transactions": [
            {"id": "TXN-84920", "property": "Tech Park West", "amount": "R48,200", "date": "10 Jun 2026", "status": "Paid"},
            {"id": "TXN-84919", "property": "Green Oaks Estate", "amount": "R31,400", "date": "09 Jun 2026", "status": "Paid"},
            {"id": "TXN-84918", "property": "Riverside Mall", "amount": "R98,000", "date": "08 Jun 2026", "status": "Processing"},
            {"id": "TXN-84917", "property": "Industrial Hub South", "amount": "R64,000", "date": "07 Jun 2026", "status": "Paid"},
            {"id": "TXN-84916", "property": "Metro Gateway Plaza", "amount": "R12,500", "date": "06 Jun 2026", "status": "Overdue"}
        ]
    }

    ai_insights = [
        {
            "type": "prediction",
            "title": "Peak Load Demand Warning",
            "desc": "Expected 24% load surge at Tech Park West between 17:00-19:00 today. Recommend battery discharge routing.",
            "action": "Route Battery Power"
        },
        {
            "type": "forecast",
            "title": "Solar Performance Boost",
            "desc": "Favorable solar yields predicted for next week in Western Cape. Solar generation forecast is R48,000 above seasonal average.",
            "action": "View Solar Yields"
        },
        {
            "type": "recommendation",
            "title": "Grid Export Optimization",
            "desc": "Battery banks are at 92% capacity. Recommend exporting 15 kW to the grid during peak tariff rates at Riverside Mall.",
            "action": "Enable Grid Feed"
        }
    ]

    activity = [
        {"time": "10 min ago", "event": "New customer registered", "details": "Naledi Dlamini joined Riverside Mall solar community pool.", "type": "customer"},
        {"time": "45 min ago", "event": "Energy purchase successful", "details": "Tech Park West acquired 12.4 MWh via smart-trade interface.", "type": "purchase"},
        {"time": "2 hours ago", "event": "Technician assignment dispatch", "details": "Sipho Ndlovu assigned to Battery storage calibration at Green Oaks Estate.", "type": "tech"},
        {"time": "4 hours ago", "event": "Billing reconciliation complete", "details": "Month-end billing finalized for 248 properties; R4.8M invoiced.", "type": "billing"}
    ]

    return render_template(
        'dashboard.html',
        kpis=kpis,
        analytics_data=analytics_data,
        performance=performance,
        properties=properties,
        technicians=technicians,
        billing=billing,
        ai_insights=ai_insights,
        activity=activity
    )

# 2. CLIENT/CONSUMER DASHBOARD ROUTE
@app.route('/dashboard-client')
@app.route('/dashboard-client.html')
def dashboard_client():
    active_plan = {
        "reseller_name": "EcoCurrent Power",
        "rate": 0.112,
        "energy_type": "100% Solar Energy",
        "plan_type": "Fixed Rate",
        "contract_term": "24 Months",
        "start_date": "Jan 10, 2026",
        "end_date": "Jan 10, 2028",
        "phone": "+1 (800) 555-0142",
        "account_no": "KB-8947-2026"
    }
    
    usage_stats = {
        "current_month_kwh": 782,
        "current_month_bill": 87.58,
        "avg_daily_kwh": 26.1,
        "co2_saved_tons": 4.2,
        "trees_planted_equiv": 70
    }
    
    usage_history = [
        {"month": "Dec 2025", "kwh": 890, "bill": 99.68},
        {"month": "Jan 2026", "kwh": 845, "bill": 94.64},
        {"month": "Feb 2026", "kwh": 810, "bill": 90.72},
        {"month": "Mar 2026", "kwh": 750, "bill": 84.00},
        {"month": "Apr 2026", "kwh": 720, "bill": 80.64},
        {"month": "May 2026", "kwh": 782, "bill": 87.58}
    ]
    
    billing_history = [
        {"invoice_no": "INV-2026-005", "date": "Jun 01, 2026", "period": "May 01 - May 31", "kwh": 782, "amount": 87.58, "status": "Paid"},
        {"invoice_no": "INV-2026-004", "date": "May 01, 2026", "period": "Apr 01 - Apr 30", "kwh": 720, "amount": 80.64, "status": "Paid"},
        {"invoice_no": "INV-2026-003", "date": "Apr 01, 2026", "period": "Mar 01 - Mar 31", "kwh": 750, "amount": 84.00, "status": "Paid"},
        {"invoice_no": "INV-2026-002", "date": "Mar 01, 2026", "period": "Feb 01 - Feb 28", "kwh": 810, "amount": 90.72, "status": "Paid"},
        {"invoice_no": "INV-2026-001", "date": "Feb 01, 2026", "period": "Jan 10 - Jan 31", "kwh": 620, "amount": 69.44, "status": "Paid"}
    ]
    
    cheaper_reseller = {
        "name": "VoltStream Energy",
        "rate": 0.105,
        "energy_type": "100% Renewable (Wind & Solar)",
        "monthly_savings": 5.47,
        "phone": "+1 (800) 555-0199",
        "website": "https://voltstream.example.com"
    }

    return render_template(
        'dashboard-client.html',
        active_plan=active_plan,
        usage_stats=usage_stats,
        usage_history=usage_history,
        billing_history=billing_history,
        cheaper_reseller=cheaper_reseller
    )

@app.route('/<path:path>')
def serve_page(path):
    if not path.endswith('.html'):
        html_path = f"{path}.html"
    else:
        html_path = path

    template_exists = os.path.exists(os.path.join(app.template_folder, html_path))
    if template_exists:
        return render_template(html_path)
    
    error_template_exists = os.path.exists(os.path.join(app.template_folder, '404-error.html'))
    if error_template_exists:
        return render_template('404-error.html'), 404
    abort(404)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
