# Blog Content Generator

## Overview

The Blog Content Generator is a Flask-based web application designed to streamline the process of generating blog content. The application allows users to generate engaging topics within a specified niche and subsequently create well-structured blog posts based on those topics.

## Problems It Solves

1. **Time-Consuming Content Creation**: Writing blog posts can be time-consuming and challenging, especially when trying to come up with engaging topics and structured content. This app automates the generation of topics and the creation of blog posts, saving users valuable time.

2. **Lack of Inspiration**: Often, content creators struggle with writer's block or lack inspiration for new topics. The app provides a steady stream of fresh, relevant topics within a given niche, helping to overcome creative blocks.

3. **Quality and Structure**: Ensuring blog posts are well-structured and of high quality can be difficult. The app generates blog posts that follow a predefined structure, ensuring consistency and quality.

## Features

- **Topic Generation**: Users can generate a list of engaging topics within a specified niche, incorporating various viral elements to increase appeal.
- **Article Generation**: Users can create well-structured and engaging blog posts based on the generated topics.
- **Delete All Articles**: An admin feature to delete all articles from the database for easy management and maintenance.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/kbtanvir/blog-writer-ai.git
   cd blog-content-generator
   ```

2. **Create a Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

5. **Run the Application**:
   ```sh
   flask run
   ```

## Usage

1. **Generate Topics**:
   - Navigate to the topic generation page.
   - Enter the desired niche and the number of topics to generate.
   - Click "Generate" to receive a list of engaging topics.

2. **Generate Articles**:
   - Select a generated topic.
   - Navigate to the article generation page.
   - Click "Generate" to create a well-structured blog post based on the selected topic.

3. **Delete All Articles**:
   - Send a POST request to `/delete_all` to remove all articles from the database.
   - Example using `curl`:
     ```sh
     curl -X POST http://localhost:5000/delete_all
     ```

## Code Structure

- **app.py**: The main application file containing route definitions and application setup.
- **models.py**: Defines the database models.
- **templates/**: Contains the HTML templates for the web pages.
- **static/**: Contains static files like CSS and JavaScript.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.


## Contact

For questions or support, please open an issue in this repository.

---

Happy blogging!
```

### Explanation

- **Overview**: Provides a brief introduction to the application.
- **Problems It Solves**: Describes the main problems the application addresses.
- **Features**: Lists the key features of the application.
- **Installation**: Detailed steps to set up the application locally.
- **Usage**: Instructions on how to use the application.
- **Code Structure**: Describes the main files and directories in the project.
- **Contributing**: Guidelines for contributing to the project.
- **License**: Information about the project's license.
- **Contact**: Information on how to get support or ask questions.

This `README.md` file will help users understand the purpose of your application, how to install and use it, and how to contribute. Adjust the repository URL and other details as needed.
