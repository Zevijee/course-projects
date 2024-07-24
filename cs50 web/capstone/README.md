# Daily Task Manager

## Description

I have created a comprehensive daily task manager to effectively document and manage my daily tasks. This project stands out as a unique and robust task management solution. While a similar concept was briefly covered in one of the lectures, this implementation goes beyond the scope of the lecture demonstration in terms of complexity and functionality.

## Distinctiveness

This daily task manager distinguishes itself by providing a feature-rich user experience. Each task is associated with a specific time of day, urgency level, and targeted completion date. Users can create lists for today's tasks or any future day. Additionally, they can access and review past task lists. The system allows marking tasks as completed, deleting tasks, and editing task details. All these operations are performed asynchronously using JavaScript and API fetch calls to the Django backend. The backend utilizes Python and Django framework, and tasks are stored in a Django model. The task manager dynamically updates the task lists based on the selected date and provides real-time feedback to the user.

## Complexity

This project's complexity lies in its extensive user experience features. Tasks are organized based on the time of day, urgency, and target date, ensuring effective task management. The application leverages JavaScript and API calls to interact with the backend, enabling seamless task creation, editing, and deletion. Tasks are persistently stored in the Django model, allowing users to access and manage them across different sessions. The task manager offers the flexibility to view today's tasks, check past lists, or plan future lists. Additionally, the system displays a random motivational mantra, updated using JavaScript, providing users with daily inspiration. The greeting message adapts to the time of day, creating a personalized experience.

## Project Structure

The project structure is organized as follows:

- **urls.py**: Defines all the project's URL routes.
- **layout.html**: Provides the basic HTML layout for the project and includes imports for CSS and JavaScript files.
- **index.html**: Serves as the default landing page, allowing users to create new tasks for the current day and view all tasks for the day.
- **register.html**: Provides a user registration form.
- **login.html**: Offers a login form for users to authenticate.
- **create_future_list.html**: Displays a page where users can view, edit, and create tasks for a future list.
- **see_past_list.html**: Presents a page where users can access and review past task lists.
- **index.js**: Contains the JavaScript logic for sending API calls to create, edit, delete, and load tasks for the current day. It also handles updating the motivational mantra and greeting based on the time of day.
- **mantra.js**: Includes an array of motivational mantras, which is loaded directly into the index.js file for use.
- **layout.css**: Defines custom CSS styles for the project, enhancing its visual appeal and usability.

## How to Run

To run the Daily Task Manager project, follow these steps:

1. Ensure you have Python and Django installed on your system.
2. Open a terminal or command prompt and navigate to the project's root directory.
3. Run the following command to start the Django development server:
4. The terminal will display a local server address (e.g., `http://127.0.0.1:8000/`).
5. Open a web browser and enter the local server address to access the Daily Task Manager application.

This project offers a comprehensive and intuitive daily task management solution, empowering users to efficiently plan, organize, and track their tasks with ease.
