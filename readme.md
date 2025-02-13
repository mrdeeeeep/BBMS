# Blood Bank Management System 🩸

A simple web application to manage blood donations and requests.

## Login Details 🔑

### Admin Login
- **Email:** admin@bloodbank.com
- **Password:** admin123
- **Login URL:** /admin/login

### Test User
- **Email:** test@example.com
- **Password:** test123

## Main Pages 📄

1. **Home Page** - `/`
2. **Login Page** - `/login`
3. **Register Page** - `/register`
4. **Dashboard** - `/dashboard`
5. **Donate Blood** - `/donate`
6. **Request Blood** - `/request`
7. **Profile** - `/profile`

## Directory Structure 📁

```
blood-bank/
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── donate.html
│   ├── request.html
│   └── profile.html
├── static/
│   ├── css/
│   └── images/
├── app.py
└── database.db
```

## Basic Features ✨

1. **For Donors**
   - Register as donor
   - Schedule donation
   - View donation history

2. **For Patients**
   - Request blood
   - Check request status
   - View available blood types

3. **For Admin**
   - Manage donors
   - Manage blood requests
   - View inventory
   - Generate reports

## How to Start 🚀

1. Install Python
2. Run `pip install -r requirements.txt`
3. Run `python app.py`
4. Open `http://localhost:5000` in your browser