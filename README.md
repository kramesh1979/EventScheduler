# EventAlchemy

EventAlchemy is an intuitive and reliable application designed for easy event scheduling. It combines a user-friendly frontend built with Python Tkinter and a robust backend utilizing MySQL database connectivity. This project aims to simplify event management, offering flexibility and enhanced user experience.

## Features
	•	Intuitive GUI: Powered by Python Tkinter for a smooth and interactive user experience.
	•	Backend Integration: Uses MySQL for secure event data storage and retrieval.
	•	Flexible Scheduling: Supports a variety of event types and schedules.
	•	Enhanced User Feedback: Guides users through event management with error prevention and success confirmations.
## Technologies Used
   ### Frontend
	•	Python Tkinter: Provides the graphical interface, allowing users to interact smoothly with the application.
	•	Dynamic Widgets: Utilizes Tkinter widgets like buttons, labels, entry fields, and tree views to simplify user interaction.

   ### Backend
	•	MySQL Database: Stores user credentials and event data securely.
	•	Database Connection: Python’s mysql-connector library ensures reliable communication between the interface and the database.

## Installation Instructions

   ### Prerequisites
	•	Python 3.x
	•	MySQL Server
	•	Required Python libraries:
	•	mysql-connector-python
	•	tkinter
	•	datetime

   ### Steps to Run Locally

   1. Clone the Repository:

   ```bash
   git clone https://github.com/username/EventScheduler.git
   cd EventScheduler```

	2. Set Up MySQL Database:
      •	Create a new MySQL database named event_scheduler.
      •	Import the provided SQL schema into this database.

	3.	Install Required Python Packages:

   ```bash
   pip install mysql-connector-python```

   4.	Run the Application:

      •	Ensure your MySQL database credentials are correctly set up in the db_connection.py file.
      •	Run the main application script:
      ```bash
      python start.py

   5.	Usage:
         •	Launch the application to interact with the EventAlchemy interface.
         •	Use the provided options to add, view, update, or delete events.
         •	Manage user profiles and event scheduling seamlessly.

## Contributing

	•	Contributions are welcome! If you would like to contribute to the project, please follow these steps:
         1.	Fork the repository.
         2.	Create a new branch (git checkout -b feature-branch).
         3.	Make your changes.
         4.	Push your changes to your fork.
         5.	Submit a pull request.

##  License

	•	This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

	•	Author: Ramesh Kandasamy
	•	Email: ramesh.kandasamy@gmail.com
	•	GitHub: kramesh1979