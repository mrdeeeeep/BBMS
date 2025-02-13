from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models import User, BloodDonation, BloodRequest
from forms import RegistrationForm, LoginForm, DonationForm, RequestForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    # Calculate blood stock for each blood type
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_stock = {}
    
    for blood_type in blood_types:
        # Calculate total donations
        total_donations = db.session.query(db.func.sum(BloodDonation.quantity)).\
            filter(BloodDonation.blood_type == blood_type).scalar() or 0
        
        # Calculate approved requests
        total_requests = db.session.query(db.func.sum(BloodRequest.quantity)).\
            filter(BloodRequest.blood_type == blood_type).\
            filter(BloodRequest.status == 'approved').scalar() or 0
        
        # Calculate available stock
        available = total_donations - total_requests
        
        blood_stock[blood_type] = {
            'donations': total_donations,
            'requests': total_requests,
            'available': available
        }
    
    return render_template('home.html', blood_stock=blood_stock)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid email or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if current_user.user_type != 'donor':
        flash('Access denied. Donors only.', 'error')
        return redirect(url_for('home'))
    
    form = DonationForm()
    if form.validate_on_submit():
        donation = BloodDonation(
            donor_id=current_user.id,
            blood_type=form.blood_type.data,
            quantity=form.quantity.data
        )
        db.session.add(donation)
        db.session.commit()
        flash('Blood donation recorded successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('donate.html', form=form)

@app.route('/request', methods=['GET', 'POST'])
@login_required
def request_blood():
    if current_user.user_type != 'requester':
        flash('Access denied. Requesters only.', 'error')
        return redirect(url_for('home'))
    
    form = RequestForm()
    if form.validate_on_submit():
        blood_request = BloodRequest(
            requester_id=current_user.id,
            blood_type=form.blood_type.data,
            quantity=form.quantity.data,
            urgency=form.urgency.data
        )
        db.session.add(blood_request)
        db.session.commit()
        flash('Blood request submitted successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('request.html', form=form)

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.user_type != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('home'))
    
    # Get basic stats
    total_donors = User.query.filter_by(user_type='donor').count()
    total_requesters = User.query.filter_by(user_type='requester').count()
    pending_requests = BloodRequest.query.filter_by(status='pending').count()
    
    # Calculate blood stock for each blood type
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_stock = {}
    
    for blood_type in blood_types:
        # Calculate total donations
        total_donations = db.session.query(db.func.sum(BloodDonation.quantity)).\
            filter(BloodDonation.blood_type == blood_type).scalar() or 0
        
        # Calculate approved requests
        total_requests = db.session.query(db.func.sum(BloodRequest.quantity)).\
            filter(BloodRequest.blood_type == blood_type).\
            filter(BloodRequest.status == 'approved').scalar() or 0
        
        # Calculate available stock
        available = total_donations - total_requests
        
        blood_stock[blood_type] = {
            'donations': total_donations,
            'requests': total_requests,
            'available': available
        }
    
    # Get pending requests with related user info
    pending_request_list = BloodRequest.query.\
        filter_by(status='pending').\
        order_by(BloodRequest.urgency.desc(), BloodRequest.request_date.asc()).\
        all()
    
    # Get recent donations
    recent_donations = BloodDonation.query.\
        order_by(BloodDonation.donation_date.desc()).\
        limit(10).\
        all()
    
    return render_template('admin.html',
                         total_donors=total_donors,
                         total_requesters=total_requesters,
                         pending_requests=pending_requests,
                         blood_stock=blood_stock,
                         pending_request_list=pending_request_list,
                         recent_donations=recent_donations)

@app.route('/admin/approve_request/<int:request_id>')
@login_required
def approve_request(request_id):
    if current_user.user_type != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('home'))
    
    blood_request = BloodRequest.query.get_or_404(request_id)
    blood_request.status = 'approved'
    db.session.commit()
    flash('Blood request approved!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/team')
def team():
    team_members = [
        {
            'name': 'Aditya Raj',
            'roll_no': '21BCS9723'
        },
        {
            'name': 'Aditya Raj',
            'roll_no': '21BCS9723'
        },
        {
            'name': 'Aditya Raj',
            'roll_no': '21BCS9723'
        },
        # Add more team members as needed
    ]
    return render_template('team.html', team_members=team_members)

@app.route('/donor_dashboard')
@login_required
def donor_dashboard():
    if current_user.user_type != 'donor':
        flash('Access denied. Donors only.', 'error')
        return redirect(url_for('home'))
    
    # Get all donations by the current user
    donations = BloodDonation.query\
        .filter_by(donor_id=current_user.id)\
        .order_by(BloodDonation.donation_date.desc())\
        .all()
    
    return render_template('donor_dashboard.html', donations=donations)

@app.route('/requester_dashboard')
@login_required
def requester_dashboard():
    if current_user.user_type != 'requester':
        flash('Access denied. Requesters only.', 'error')
        return redirect(url_for('home'))
    
    # Get all requests by the current user
    requests = BloodRequest.query\
        .filter_by(requester_id=current_user.id)\
        .order_by(BloodRequest.request_date.desc())\
        .all()
    
    return render_template('requester_dashboard.html', requests=requests)

if __name__ == '__main__':
    app.run(debug=True) 