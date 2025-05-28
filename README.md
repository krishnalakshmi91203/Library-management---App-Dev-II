# Library Management System APP DEV - II: A Comprehensive E-book Management System

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/78953cc1-a244-41b6-98b3-a2c0be35e6c9" width="70%" style="margin-left: 10%;">
</div>

---

## Features

### User and Librarian Authentication

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/6a634fb7-209c-42d5-9d1b-b92702cdd861" width="48%">
  <img src="https://github.com/user-attachments/assets/fcef253a-7512-4154-8118-33cc93cad636" width="48%">
</div>

- **Role-Based Access Control**: Secure login mechanism for users and librarians.
- Restricted access to functionalities based on user roles to ensure data security.

### Librarian Dashboard

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/7530ff92-5cbe-49ef-8bf9-9b88ba44c6d7" width="48%" height="110%">
  <img src="https://github.com/user-attachments/assets/0ac92e3a-427f-4137-822c-9a91d07eaafa" width="48%">
</div>

- Comprehensive dashboard with statistics on active users, e-book transactions, and pending requests.
- Ability to revoke book access manually or via automated 7-day expiry.

### Section Management

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/454c5b95-ef30-46d7-a1cd-bca1a5a970b4" width="48%">
  <img src="https://github.com/user-attachments/assets/cb356367-392c-4cd7-bc8e-528219ef1ac6" width="48%">
    <img src="https://github.com/user-attachments/assets/a5680c9c-e87d-4a22-a409-ba1fac9af8a2" width="48%">
</div>

- Librarians can search, create, update, and delete sections for categorizing e-books.
- Ensures organized and accessible library content.

### E-Book Management

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/dbb018bb-901c-4e2e-8772-9b271e4d63d5" width="48%">
  <img src="https://github.com/user-attachments/assets/8828cbc5-2d64-4053-a40d-0aca3264a83c" width="48%">
    <img src="https://github.com/user-attachments/assets/98a51c04-8d6d-4e2f-8a28-3b27961de80c" width="48%">
    <img src="https://github.com/user-attachments/assets/6d46aa23-330e-49f8-a8d2-1df23e3f8516" width="48%">
</div>

- CRUD operations for e-books, including editing details like title, author, content, and availability.
- Helps librarians can search e-books and maintain an up-to-date digital collection.

### Search and User Interaction

<div style="display: flex; justify-content: center; align-items: center;">
    <img src="https://github.com/user-attachments/assets/61bd6906-2b8d-4cad-9d7e-e1425089a9db" width="48%">
  <img src="https://github.com/user-attachments/assets/da5ae882-98e5-492b-8386-3962e2ef86db" width="48%">
  <img src="https://github.com/user-attachments/assets/1b072585-5979-42fd-bc59-ea4caaa4da01" width="48%">
    <img src="https://github.com/user-attachments/assets/2db0b582-2944-42e2-9d5c-9a5339a1b351" width="48%">
</div>

- **Search**: Users can search for e-books and sections by various criteria.
- **Book Requests**: Users can request up to 5 books simultaneously.
- **Feedback**: Users can leave feedback and ratings on e-books.

### Automated Reminders and Reporting
- **Reminders**: Daily SMS reminders to users about return dates using Twilio.
- **Reports**: Monthly activity reports emailed to librarians using SMTP.
- Automated processes reduce manual effort and ensure timely communication.

### Additional Features

<div style="display: flex; justify-content: center;">
  <img src="https://github.com/user-attachments/assets/3453fdad-6600-449c-8a8c-282f4beb3b43" width="48%">
  <img src="https://github.com/user-attachments/assets/a35eb622-8e14-4116-89f1-d3e3671b8f10" width="48%">
  <img src="https://github.com/user-attachments/assets/90510877-cfcb-40c0-b0ad-9c4e61e5f943" width="48%">
</div>

- **Profile Updates**: Users can update their personal details and preferences.
- **Ratings**: Users can rate e-books, influencing their overall rating.
- **Statistics**: Librarians can view detailed statistics of user activities, book statuses, and popular books.

### Sorting and Prioritization
- Books are displayed in descending order of their ratings, prioritizing highly-rated content for better user experience.

---
## 📽️ Demo Video: Features & Functionality

[Watch the Demo Video](https://drive.google.com/file/d/1Nx8zZkuIDyMMH1DZNYfvvqUhmqmqTP7n/view?usp=drive_link)

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

