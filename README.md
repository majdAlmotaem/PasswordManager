# Password Manager

<!-- LOGO PLACEHOLDER -->
![icon](https://github.com/user-attachments/assets/a8bcccaa-3241-4cc6-9653-1470c7a43a17)


A modern, secure, and user-friendly password manager built with Python and Tkinter.

## Features

- Modern UI/UX: Dark theme, accent colors, and responsive dialogs.
- Secure Storage: All passwords are encrypted using your master password.
- Master Password Security: Master password is hashed (PBKDF2) and never stored in plain text.
- Registration: Sign up with username, email, and password (with confirmation and email validation).
- Password Vault: Add, view (with decryption), and delete passwords for different services.
- Password Strength: Responsive checklist for password strength during creation.
- Notes: Store additional notes with each password entry.
- Logout: Securely log out and return to the login screen.

![Timeline1-ezgif com-gif-maker (1)](https://github.com/user-attachments/assets/7a7788f3-7275-4800-a2c8-efd7e1070bc2)


## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Database Setup

- The app will create a SQLite database (`data/vault.db`) on first run.

### Running the App

```sh
python main.py
```

## Security Notes

- Master password is never stored in plain text.
- All vault entries are encrypted with the master password.
- Passwords are only decrypted in memory when needed.

## Customization

- You can further enhance email validation or add more advanced registration features as needed.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

---

_Add your logo and live demo above!_
