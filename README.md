# Phishing Email Simulator

A comprehensive cybersecurity training platform built with Flask that simulates phishing email campaigns to educate users about email security threats. Features a modern dark theme with neon accents, interactive campaign management, and detailed analytics.

## 🌟 Features

- **Complete Campaign Management**: Create, manage, and track phishing email campaigns
- **User Management**: Admin dashboard for managing target users and departments
- **Interactive Simulator**: Real-time phishing email simulation with recipient tracking
- **Analytics Dashboard**: Detailed metrics on campaign performance and user responses
- **Educational Content**: Built-in training materials and educational resources
- **Responsive Design**: Mobile-first design with modern UI/UX
- **Dark Theme**: Neon green (#00ff9d) and blue (#00b8ff) accents on dark background
- **Real-time Updates**: Live campaign status and recipient interaction tracking

## 📄 Pages

### 1. Marketing Pages
- **Home**: Landing page with cybersecurity awareness content
- **About**: Company information and security threat landscape
- **Projects**: Showcase of cybersecurity projects and initiatives

### 2. Simulator Platform
- **Campaign Dashboard**: Main simulator interface for creating campaigns
- **Admin Panel**: User management and system administration
- **Analytics**: Detailed campaign performance metrics and insights
- **Phishing Pages**: Realistic phishing landing pages for simulation
- **Educational Messages**: Training content for users who interact with campaigns

## 🛠 Technical Implementation

### Backend (Flask)
- **Database**: SQLite with SQLAlchemy ORM
- **API Endpoints**: RESTful API for campaign and user management
- **Template Engine**: Jinja2 with Flask templating
- **Static Files**: Optimized CSS and JavaScript delivery
- **Error Handling**: Comprehensive error handling and validation

### Frontend Technologies
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Custom properties, Flexbox, Grid layouts, animations
- **JavaScript**: ES6+ features, async/await, fetch API
- **Responsive Design**: Mobile-first approach with breakpoints

### Key Features
- **Campaign Creation**: Multi-step campaign setup with template selection
- **User Targeting**: Department and role-based user selection
- **Real-time Tracking**: Live updates on email opens, link clicks, and form submissions
- **Educational Redirects**: Automatic redirection to training materials
- **Analytics Dashboard**: Visual charts and detailed metrics

## 📁 File Structure

```
phishing-email-simulator/
├── backend/
│   └── app.py                 # Flask application with all routes and APIs
├── static/
│   ├── css/
│   │   ├── main.css          # Marketing pages styles
│   │   └── simulator.css     # Simulator-specific styles
│   └── js/
│       ├── app.js            # Marketing pages JavaScript
│       ├── admin.js          # Admin dashboard functionality
│       └── simulator.js      # Campaign management and simulation
├── templates/
│   ├── simulator/
│   │   ├── index.html        # Main simulator dashboard
│   │   ├── admin.html        # User management interface
│   │   ├── analytics.html    # Analytics and reporting
│   │   ├── about.html        # About page
│   │   ├── projects.html     # Projects showcase
│   │   ├── phishing_page.html     # Simulated phishing landing
│   │   └── educational_message.html # Training content
│   └── index.html            # Marketing homepage
├── phishing_simulation.db     # SQLite database (created automatically)
├── README.md                 # This file
└── .gitignore               # Git ignore configuration
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7+ with pip
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git (for cloning the repository)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ElonCoding/Phishing-Email-Simulator-.git
   cd phishing-email-simulator
   ```

2. **Install Python dependencies:**
   ```bash
   pip install flask
   ```

3. **Start the Flask application:**
   ```bash
   cd backend
   python app.py
   ```

4. **Access the application:**
   - Marketing pages: http://localhost:5000
   - Simulator dashboard: http://localhost:5000/simulator
   - Admin panel: http://localhost:5000/admin
   - Analytics: http://localhost:5000/analytics

### Development Setup
For development with auto-reload:
```bash
export FLASK_ENV=development
python backend/app.py
```

## 🎨 Customization

### Theme Colors
Edit CSS custom properties in `css/main.css`:
```css
:root {
    --primary-bg: #121212;
    --secondary-bg: #1a1a1a;
    --accent-green: #00ff9d;
    --accent-blue: #00b8ff;
    --text-light: #ffffff;
    --text-muted: #b3b3b3;
}
```

### Email Templates
Edit email templates in the simulator interface to customize phishing simulation content. Templates include:
- **Urgent Security Update**: Simulates urgent account security notifications
- **Package Delivery**: Mimics shipping notification emails
- **IT Support**: Simulates internal IT support requests
- **Account Verification**: Fake account verification requests

### Campaign Settings
Customize campaign parameters:
- **Difficulty Levels**: Easy, Medium, Hard
- **Attack Vectors**: Different phishing techniques
- **Sender Profiles**: Customizable sender names and emails
- **Timing**: Schedule campaigns for optimal training impact

## 📱 Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🔧 Performance Optimization

### Image Optimization
- Use WebP format for images when possible
- Implement lazy loading for images
- Optimize image sizes for different screen densities

### CSS Optimization
- Minify CSS for production
- Use CSS containment for better performance
- Implement critical CSS inlining

### JavaScript Optimization
- Minify JavaScript for production
- Implement code splitting for large applications
- Use async/defer attributes for non-critical scripts

## 🔒 Security Considerations

- **Educational Purpose**: This simulator is designed for cybersecurity training only
- **Client-side Validation**: All forms include client-side validation
- **Input Sanitization**: Server-side validation implemented in Flask routes
- **HTTPS Recommended**: Use HTTPS in production environments
- **Access Control**: Implement proper authentication for production use
- **Data Privacy**: Ensure compliance with data protection regulations
- **Ethical Use**: Only use on authorized users for training purposes

## 📊 Analytics Integration

The built-in analytics dashboard tracks:
- **Campaign Performance**: Open rates, click rates, submission rates
- **User Behavior**: Individual user interaction patterns
- **Department Metrics**: Performance by department and role
- **Template Effectiveness**: Which phishing templates are most effective
- **Timeline Analytics**: Campaign progress over time
- **Geographic Data**: User location-based insights (if enabled)

## 🔄 Future Enhancements

### Potential Additions
- **Authentication System**: User login and role-based access control
- **Advanced Templates**: More sophisticated phishing email templates
- **Reporting System**: Automated PDF reports for management
- **Integration APIs**: Connect with existing security tools
- **Mobile App**: Companion mobile application for administrators
- **Multi-tenant Support**: Support for multiple organizations
- **Advanced Analytics**: Machine learning for threat detection
- **Real-time Notifications**: Email/SMS alerts for campaign events

### Technical Improvements
- **Database Migration**: Upgrade to PostgreSQL for production
- **Containerization**: Docker support for easy deployment
- **API Documentation**: Swagger/OpenAPI documentation
- **Testing Suite**: Unit and integration tests
- **Performance Optimization**: Caching and query optimization
- **Security Hardening**: Advanced security measures
- **Scalability**: Support for large-scale deployments

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔌 API Endpoints

### Campaign Management
- `GET /api/campaigns` - List all campaigns
- `POST /api/campaigns` - Create new campaign
- `GET /api/campaigns/<id>` - Get campaign details
- `GET /api/campaign-recipients/<id>` - Get campaign recipients

### User Management
- `GET /api/users` - List all users
- `POST /api/users` - Create new user
- `POST /api/seed-users` - Add demo users

### Analytics
- `GET /api/analytics` - Get analytics data
- `GET /api/campaigns/<id>/stats` - Get campaign statistics

### Simulation
- `POST /api/track-email-open/<id>` - Track email opens
- `POST /api/track-link-click/<id>` - Track link clicks
- `POST /api/track-credentials/<id>` - Track credential submissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the code comments
- Review the API endpoints for integration help

---

**Built with ❤️ for cybersecurity education and awareness**