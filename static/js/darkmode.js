document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');
    const body = document.body;
    
    if (!darkModeToggle) return;
    
    // Check localStorage first (for non-authenticated users or fallback)
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    const isAuthenticated = body.classList.contains('dark-mode') || 
                          (body.querySelector('.navbar') && document.querySelector('.nav-link[href*="logout"]'));
    
    // Initialize dark mode from user preference or localStorage
    if (!isAuthenticated && savedDarkMode) {
        body.classList.add('dark-mode');
        updateIcon(true);
    }
    
    darkModeToggle.addEventListener('click', function() {
        const isDark = body.classList.toggle('dark-mode');
        
        // Update icon
        updateIcon(isDark);
        
        // If user is authenticated, save to database
        if (isAuthenticated) {
            fetch('/toggle_dark_mode', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log('Dark mode preference saved:', data);
            })
            .catch(error => {
                console.error('Error saving dark mode preference:', error);
            });
        } else {
            // Save to localStorage for non-authenticated users
            localStorage.setItem('darkMode', isDark);
        }
    });
    
    function updateIcon(isDark) {
        if (darkModeIcon) {
            darkModeIcon.className = isDark ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
        }
    }

    // Update icon on page load based on current state
    if (body.classList.contains('dark-mode')) {
        updateIcon(true);
    }
});


