# Farm Visit Management System

A modern, comprehensive web application for managing farm visits and agricultural assessments. Built with Flask, featuring a beautiful responsive UI and secure admin functionality.

## Features

### 🚀 Core Features

- **Modern Farm Visit Form**: Comprehensive data collection for farm visits
- **JSON Data Storage**: All data is stored in a local JSON file
- **Admin Dashboard**: Password-protected admin interface
- **Search & Filter**: Advanced search and filtering capabilities
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Statistics**: Live dashboard with visit statistics

### 📋 Form Sections

1. **Farmer Details**: Name, ID, contact info, location, GPS coordinates
2. **Visit Details**: Date, type, officer, time spent
3. **Observations**: Crops, livestock, issues identification
4. **Recommendations**: Advice, follow-up planning
5. **Follow-up Actions**: Training needs, referrals, additional notes

### 🔐 Admin Features

- **Secure Login**: Password-protected admin access
- **Data Management**: View all farm visit entries
- **Delete Entries**: Remove unwanted entries
- **Search & Filter**: Find specific entries quickly
- **Statistics Dashboard**: Overview of visit data

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download

Download the project files to your local machine.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Access the Application

- **Main Form**: http://localhost:5000
- **Admin Login**: http://localhost:5000/admin
- **Default Admin Password**: `admin123`

## Usage

### For Field Officers

1. Navigate to the main form page
2. Fill out all required fields (marked with \*)
3. Add detailed observations and recommendations
4. Submit the form
5. Data is automatically saved to the JSON file

### For Administrators

1. Click "Admin Login" on the main page
2. Enter the admin password (`admin123`)
3. View all farm visit entries
4. Use search and filter options to find specific entries
5. Delete entries if needed
6. Monitor statistics and trends

## File Structure

```
Farm_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data.json             # Data storage (created automatically)
└── templates/
    ├── index.html        # Main farm visit form
    ├── admin_login.html  # Admin login page
    └── admin_dashboard.html # Admin dashboard
```

## Configuration

### Security Settings

⚠️ **Important**: Change these default values in production:

1. **Admin Password**: Edit `ADMIN_PASSWORD` in `app.py`
2. **Secret Key**: Change `app.secret_key` in `app.py`

### Data Storage

- All data is stored in `data.json`
- The file is created automatically on first run
- Data format is human-readable JSON

## Features in Detail

### Form Features

- **Responsive Design**: Works on all device sizes
- **Form Validation**: Client-side and server-side validation
- **Auto-save**: Prevents data loss
- **File Upload**: Support for photo uploads
- **GPS Integration**: Coordinate input for farm locations

### Admin Dashboard Features

- **Real-time Search**: Instant search across all fields
- **Advanced Filtering**: Filter by visit type, date, officer
- **Statistics**: Live counters for total entries, monthly visits, etc.
- **Delete Confirmation**: Safe deletion with confirmation
- **Responsive Layout**: Mobile-friendly admin interface

### Data Management

- **JSON Storage**: Simple, portable data format
- **Automatic Backups**: Data is preserved between sessions
- **Export Ready**: JSON format allows easy data export
- **No Database Required**: Simple file-based storage

## Customization

### Styling

The application uses modern CSS with:

- Gradient backgrounds
- Card-based layouts
- Smooth animations
- Font Awesome icons
- Inter font family

### Adding New Fields

1. Add the field to the HTML form in `templates/index.html`
2. Update the form processing in `app.py`
3. Display the field in `templates/admin_dashboard.html`

### Changing Colors

Edit the CSS variables in the template files:

- Primary color: `#4facfe`
- Secondary color: `#667eea`
- Background gradient: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`

## Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Change the port in app.py
   app.run(debug=True, port=5001)
   ```

2. **Permission Errors**

   ```bash
   # Ensure write permissions for data.json
   chmod 644 data.json
   ```

3. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Data Recovery

- The `data.json` file contains all your data
- Make regular backups of this file
- If corrupted, you can restore from backup

## Security Considerations

### Production Deployment

1. **Change Default Password**: Update `ADMIN_PASSWORD`
2. **Use HTTPS**: Configure SSL certificates
3. **Environment Variables**: Store sensitive data in environment variables
4. **Regular Backups**: Backup `data.json` regularly
5. **Access Control**: Restrict server access

### Data Privacy

- All data is stored locally
- No external data transmission
- Consider data retention policies
- Implement user access controls if needed

## Support

For issues or questions:

1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure proper file permissions
4. Check the console for error messages

## License

This project is open source and available under the MIT License.

---

**Note**: This is a development version. For production use, please implement proper security measures and data backup procedures.