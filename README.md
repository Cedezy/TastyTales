# Wanderlust - Travel Blog Application

A full-featured travel blog application built with Python, Flask, and SQLAlchemy. Share your travel adventures, explore destinations, and connect with fellow wanderers from around the world.

## Features

- **User Authentication**: Register, login, and secure session management with password hashing
- **Travel Stories**: Create, edit, and delete travel posts with destination, travel date, content, and image uploads
- **Destination Tracking**: Add location/destination and travel dates to your stories
- **Image Upload**: Upload and automatically resize travel photos
- **Search Functionality**: Search travel stories by title, content, or destination
- **Comments**: Add and delete comments on travel stories
- **Dark Mode**: Toggle between light and dark themes with persistent preferences
- **Pagination**: Browse travel stories with pagination support
- **User Profiles**: View traveler profiles with their adventures
- **Responsive Design**: Modern, mobile-friendly UI perfect for sharing on the go

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment**:
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Run the application**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. **Create an account** and start sharing your travel adventures! 🌍✈️

## Project Structure

```
Rem/
├── app.py                 # Main Flask application
├── models.py             # SQLAlchemy database models
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── create_post.html
│   ├── edit_post.html
│   ├── post_detail.html
│   ├── search.html
│   └── profile.html
├── static/               # Static files
│   ├── css/
│   │   ├── base.css
│   │   ├── index.css
│   │   ├── login.css
│   │   ├── register.css
│   │   ├── create_post.css
│   │   ├── edit_post.css
│   │   ├── post_detail.css
│   │   ├── search.css
│   │   └── profile.css
│   ├── js/
│   │   └── darkmode.js
│   └── uploads/          # Uploaded travel photos
└── README.md
```

## Database Models

- **User**: Stores user information, authentication data, and dark mode preference
- **Post**: Stores travel stories with title, content, image path, location, travel date, and metadata
- **Comment**: Stores comments on travel stories with user and timestamp information

## Travel Blog Features

- **Destination Tags**: Add location/destination to each travel story
- **Travel Dates**: Record when you visited each destination
- **Photo Galleries**: Upload and display beautiful travel photos
- **Story Sharing**: Share your travel experiences, tips, and recommendations
- **Exploration**: Search and discover travel stories by destination

## Security Features

- Passwords are hashed using Werkzeug's password hashing
- Session management with Flask-Login
- Secure file uploads with validation
- CSRF protection (Flask's built-in protection)

## Configuration

Edit `config.py` to customize:
- Secret key for sessions
- Database URI
- Upload folder path
- Maximum file size
- Allowed file extensions
- Image dimensions

## Optional Enhancements

The application includes:
- ✅ Pagination for travel stories
- ✅ Profile page for travelers
- ✅ Image resizing for uploads
- ✅ Dark mode with persistent preferences
- ✅ Destination and travel date tracking
- ✅ Location-based search

## License

This project is open source and available under the MIT License.

---

**Happy Travels! 🌍✈️🗺️**
