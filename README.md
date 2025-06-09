# Football Match Result Prediction Web Application

This project is a web application that allows users to explore historical football match data, fetch live (post-match) data into the system, and predict future match outcomes using machine learning models. The project covers approximately 25 years of data from six major football leagues (Premier League, Ligue 1, Bundesliga, Serie A, La Liga, Süper Lig).

## ⚽ Project Description

Developed for football enthusiasts and data aficionados, this platform makes exploring past matches and predicting future outcomes easier than ever. With data collected from six major leagues since the year 2000, users can filter matches, compare statistics, and generate smart predictions. Our goal is to connect curiosity with data-driven insights.

## ✨ Key Features

*   **Data Collection:**
    *   Historical football match data is collected from sources like FBREF and stored in a database (SQLite).
    *   Live (post-match) data is collected using web scraping techniques with Selenium & ChromeDriver.
    *   Collected data includes: Home and away team information, audience count, referee name, match score, match week, player statistics, expected goals (xG) values, etc.
*   **Frontend Development:**
    *   A user-friendly and intuitive interface has been designed using HTML, CSS, JavaScript, and Bootstrap.
    *   Data exchange with the backend is handled via AJAX and Fetch API.
    *   User Registration and Login functionalities.
    *   Data Viewing: Filterable match data by league and season.
    *   Live Data Fetching: Allows users to import the latest match data for a specific league, season, and date into the system.
    *   Prediction: Users can get match result predictions by entering match details (Teams, xG, Audience, Stadium, Referee, etc.).
*   **Backend Development:**
    *   A scalable and secure backend has been built using the Django framework.
    *   SQLite database management is handled using Django ORM.
    *   User authentication and authorization are secured with Django Authentication.
*   **Data Analysis and Feature Selection:**
    *   Exploratory Data Analysis (EDA) techniques are applied to enhance the model's accuracy.
    *   If necessary, feature extraction techniques are applied to improve model performance.
*   **Model Training and Prediction:**
    *   The prepared dataset is trained using various machine learning algorithms (Logistic Regression, Random Forest, etc.) or artificial neural networks.
    *   The accuracy of trained models is evaluated, and the most optimized model is selected.
    *   The trained model is integrated into the web application to activate the match score prediction system.

## 🛠️ Technologies Used

*   **Frontend:** HTML, CSS, JavaScript, Bootstrap
*   **Backend:** Python, Django
*   **Database:** SQLite (with Django ORM)
*   **Data Collection/Scraping:** Python, Selenium, ChromeDriver
*   **Data Analysis & Machine Learning:** Python, Pandas, NumPy, Scikit-learn
*   **Project Management & Collaboration:** Trello

## 🚀 Setup and Execution

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/keremtanil/football_match_result_prediction.git
    cd football_match_result_prediction
    ```
2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # For Windows:
    venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install Required Libraries:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file should be present in the project. If not, you can create one with `pip freeze > requirements.txt`.)*
4.  **Install ChromeDriver for Web Scraping:**
    *   Ensure you have Google Chrome browser installed on your system.
    *   Download the [ChromeDriver](https://chromedriver.chromium.org/downloads) compatible with your Chrome version.
    *   Place the downloaded `chromedriver.exe` (or `chromedriver` for macOS/Linux) in your project's root directory or add it to your system's PATH.
5.  **Apply Database Migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **(Optional) Create a Superuser (for the admin panel):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```
8.  Access the application in your browser at `http://127.0.0.1:8000/`.

## 📖 Usage

1.  After opening the application, use the "Register" option to create a new account or "Login" to sign in with your existing account.
2.  **View Data:** Access detailed data of past matches by selecting the league and season.
3.  **Fetch Live Data:** Update your database with the latest match data from the web by selecting a specific league, season, and date.
4.  **Predict:** Get match result predictions by entering the required match information (League, Year, Teams, xG values, Audience, Stadium, Referee).

## 📈 Development Process (Agile)

This project was developed using Agile software development principles. The development process was divided into iterative sprints and tracked via a Trello board.

*   **Sprint 1 Focus Areas:** Data Collection, Data Processing, Data Saving, Basic Interface Development.
*   **Sprint 2 Focus Areas:** Machine Learning Model Creation, Testing, Performance Optimization, Debugging, Prediction Interface Enhancements.
*   Emphasis was placed on user stories, sprint goals, and delivering Potentially Shippable Increments/Minimum Viable Products.

![Trello Board Example](https://i.imgur.com/your_trello_screenshot_link.png)
*(You can add a link to a screenshot of your Trello board here.)*

## ⚠️ Limitations and Known Issues

*   **Data Incompleteness:** Some historical match data may be missing, especially for older seasons. This may affect the accuracy of predictions.
*   **Prediction Model Accuracy:** The machine learning model may not generalize equally well to every league, and real-time events (such as injuries, weather, or player changes) are not taken into account. Predictions are primarily based on historical data.
*   **No Live Scores:** The platform does not provide live scores or real-time match statistics while matches are being played. The "Fetch Live Data" feature collects data after matches have concluded.
*   **General League Statistics:** General league statistics such as standings or top scorers are not included in the system.
*   **Platform:** Available only as a web application. There is no mobile app version.
*   **League Coverage:** The dataset is limited to the six specified major leagues (Premier League, Ligue 1, Bundesliga, Serie A, La Liga, Süper Lig). Friendlies, national cups, etc., are not included.
*   **Visual Content:** Visual content such as match footage, highlights, or in-depth tactical analyses is not provided.

## 🧑‍💻 Team Members

*   Hatice Kandemir
*   Köksal Kerem Tanıl
*   Defne Turğut
