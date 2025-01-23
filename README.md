# Library Management System APP DEV - II: A Comprehensive E-book Management System

---

## Features

### User and Librarian Authentication
- **Role-Based Access Control**: Secure login mechanism for users and librarians.
- Restricted access to functionalities based on user roles to ensure data security.

### Librarian Dashboard
- Comprehensive dashboard with statistics on active users, e-book transactions, and pending requests.
- Ability to revoke book access manually or via automated 7-day expiry.

### Section Management
- Librarians can create, update, and delete sections for categorizing e-books.
- Ensures organized and accessible library content.

### E-Book Management
- CRUD operations for e-books, including editing details like title, author, content, and availability.
- Helps librarians maintain an up-to-date digital collection.

### Search and User Interaction
- **Search**: Users can search for e-books and sections by various criteria.
- **Book Requests**: Users can request up to 5 books simultaneously.
- **Feedback**: Users can leave feedback and ratings on e-books.

### Automated Reminders and Reporting
- **Reminders**: Daily SMS reminders to users about return dates using Twilio.
- **Reports**: Monthly activity reports emailed to librarians using SMTP.
- Automated processes reduce manual effort and ensure timely communication.

### Additional Features
- **Profile Updates**: Users can update their personal details and preferences.
- **Ratings**: Users can rate e-books, influencing their overall rating.
- **Statistics**: Librarians can view detailed statistics of user activities, book statuses, and popular books.

### Sorting and Prioritization
- Books are displayed in descending order of their ratings, prioritizing highly-rated content for better user experience.

---

## Frameworks and Libraries Used
- **SQLite**: For lightweight and easy-to-integrate data storage.
- **Flask**: For API endpoints, server-side logic, and authentication.
- **Vue.js**: For building a dynamic and responsive user interface.
- **Bootstrap**: For styling and ensuring a responsive layout.
- **Redis**: For managing asynchronous tasks and batch jobs.
- **APScheduler**: For scheduling automated tasks like reminders and reports.
- **Jinja2**: For server-side HTML rendering when necessary.

---

## API Endpoints

| Endpoint                              | Methods   | Description                                                                                   |
|---------------------------------------|-----------|-----------------------------------------------------------------------------------------------|
| `/userlogin`                          | GET, POST | Authenticates users and librarians.                                                          |
| `/register<req>`                      | POST      | Registers a new user or edits user profiles.                                                 |
| `/librarian_dashboard`                | GET, POST | View and manage sections with CRUD operations and search functionality.                      |
| `/<section_id>/books`                 | GET, POST | View and manage books within a section (CRUD operations with search).                        |
| `/sectionform/<req>`                  | GET, POST | Add or edit sections.                                                                        |
| `/<section_name>/bookform/<req>`      | GET, POST | Add or edit books.                                                                           |
| `/user_dashboard/<uname>`             | GET, POST | View and search books as a user.                                                             |
| `/user_dashboard/<uname>/mybook`      | GET, POST | View requested, granted, and completed books.                                                |
| `/librarian_dashboard/status`         | GET, POST | Manage book requests and grant/revoke access.                                                |
| `/export-ebooks`                      | POST      | Export e-book transaction data as a CSV file.                                                |

---

## Database Design
The database is designed with tables representing:
- **Users**: Stores user credentials, roles, and preferences.
- **Sections**: Categorizes e-books for better organization.
- **Books**: Contains details about e-books, including title, author, and rating.
- **Transactions**: Tracks e-book issuance, return dates, and statuses.


---

## How to Run the Project
1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`.
3. Set up the database using the provided migration scripts.
4. Start the Redis server for batch job handling.
5. Run the Flask application: `python app.py`.
6. Access the app through the local server URL.

---

