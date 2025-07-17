# Flask User Authentication App

This is a simple Flask-based web application for user authentication. It allows users to register, log in, change passwords, and includes basic password complexity and common password checks.

## Features

- User registration with password complexity requirements
- Login with hashed credentials
- Password change functionality
- PIN-based authentication for password changes
- Logging of failed login attempts
- Checks against a list of common passwords

## Requirements

- Python 3.x
- Flask
- passlib

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**
   ```sh
   pip install flask passlib
   ```

3. **Create required files:**
   - `info.txt` (can be empty or contain sample user data)
   - `CommonPassword.txt` (add common passwords, one per line)

4. **Run the app:**
   ```sh
   python app.py
   ```

5. **Open your browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

## File Structure

- `app.py` — Main application file
- `info.txt` — Stores user credentials (hashed)
- `CommonPassword.txt` — List of common passwords to check against
- `templates/` — HTML templates for the app

## Notes

- Do **not** store real user data or sensitive information in `info.txt` if you are sharing this repository.
- For demonstration/educational use only.

---

**Author:**

Only for educational purposes.
