<div align="center">
<h1>SCHEDU</h1>

### **A School Management Web Application**
</div>

## Table of Contents
- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [Authors](#authors)

---

## About
![Untitled design (copy)](https://github.com/iAdamo/Schedu/assets/106432903/f6a42b5c-b3e6-4ab5-b6a8-f3999e73eea8)

This repository contains the source code for a web application called "SCHEDU" designed for school management.<br>

Schedu is a comprehensive web application designed for managing various aspects of a school, including user registration, student information, teacher management, and more.

The SCHEDU School Management System isn't just a portfolio project; it's a collective desire to revolutionize the way schools operate. As a team, we've felt the frustrations of data mismanagement, sky-high administrative costs, and the tediousness of tasks like slow registrations process and misplaced files. That's why we've come together with a shared vision: to create a solution that transforms the educational sector.

- A command interpreter to manipulate data without a visual interface, like in a Shell (perfect for development and debugging)
- A website (the front-end) that shows the final product to everybody: static and dynamic
- A database or files that store data (data = objects)
- An API that provides a communication interface between the front-end and your data (retrieve, create, delete, update them)

Link to the deployed project page: [schedu app](https://adam-02.schedu.tech)

Link to the project’s landing page: [schedu](https://schedu.tech)

Read more about the project on our [blog](https://linkedin/in/adamsanusi)

---

## Features
- **Administrator Dashboard:** Secure login and registration for administrators.
- **User Management:** Administrators can register teachers, students, and guardians directly through the web application.
- **Role-Based Access:** Different user roles (administrator, teacher, student, guardian) with specific permissions.
- **Student Dashboard:** Students can log in to access relevant information.
- **Intuitive User Interface:** An easy-to-use interface for seamless navigation.
- **API Integration:** A RESTful API for communication between the front-end and the database.
- **Profile Management:** Users can update their profiles and view their schedules.                     

## Getting Started
Follow these steps to get started with Schedu:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/iAdamo/schedu.git
   ```

2. **Install Python virtual environment requirements:**
   ```bash
   cd Schedu
   python3 -m venv schedu
   pip install -r requirements.txt
   ```

3. **Run the Web Application:**
   ```bash
   python3 -m web.app
   ```
4. **Run the API:**
   ```bash
   python3 -m api.v1.app
   ```
   The web application will be accessible at `http://localhost:5000`.

---


## Usage
1. **Administrator Login:**
   - Navigate to the administrator login page.
   - Enter your credentials to log in: School ID and password are in the file.json but the password is hashed. Use `admin` as the password.

2. **User Registration:**
   - On the administrator dashboard, find the option to register new users.
   - Complete the registration form for teachers, students, or guardians.

3. **User Log In:**
   - Users (teachers, students, guardians) can log in using the credentials provided during registration.
   - Students can access their personalized dashboard.

---


## Contributing
If you're interested in contributing to the development of Schedu, we welcome your contributions. Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/iAdamo/schedu/blob/main/LICENSE) file for details.

---

## **`Authors`**
#### [**Adam Sanusi Babatunde**](https://linkedin/in/adamsanusi) | [**Olaoluwa Hassan**](https://linkedin/in/hassan-olaoluwa) | [**Linda Ihuoma Nwachukwu**](https://linkedin/in/linda-nwachukwu)
