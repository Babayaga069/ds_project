# Movie Success Analysis: What Makes a Movie a Hit?

## 1. Introduction
This project explores the film industry, specifically focusing on the underlying factors that drive a movie's commercial and critical success. 

To investigate this topic, our project is structured around eight core Research Questions:

1. How strongly does production budget predict box office revenue across different genres and release periods?
2. Which combination of production studio, genre, runtime and release year best explains rating-based movie success for anime movies in the last 26 years?
3. What are trends in the movie industry in terms of genre distribution and box office revenue from 2000 to 2025?
4. How does the historical success over the last 30-40 years of the 10 most popular active directors influence the financial and critical success of their new movie releases?
5. How does the financial and critical success of movie sequels between 2010 and 2024 compare to their original films across franchises?
6. How does film genre, along with production budget, influence the likelihood of receiving an Academy Award nomination?
7. How does pre- and post-release Google search interest relate to the financial and critical success of movies released between 2010 and 2024?
8. How does sticking to typical genre plots lead to greater box office success for fantasy and horror movies (from 2000 to 2025)?

To address these questions, we utilized a combination of APIs and datasets to build a view of the films analyzed:
* **TMDb API:** Our primary source for general movie data (e.g., budget, revenue, genres).
* **OMDb API:** Used to retrieve detailed plot summaries and specific director information.
* **Kaggle Dataset:** Integrated to include historical Academy Award nominations and wins.
* **PyTrends:** Utilized to measure public audience interest and search volume over time.

## 2. Description of the Data Pipeline
Our data pipeline was designed to processes data individually for each specific Research Question. The workflow consists of the following steps:
* **Data Collection:** Instead of downloading the entire database at once, we made specific API requests to TMDb and OMDb tailored to the exact requirements of each individual research question. Where necessary for specific questions, we also integrated data from the Kaggle dataset (Academy Awards) and PyTrends (audience interest).
* **Data Cleaning & Processing:** The data was cleaned and preprocessed specifically for the respective research question it was meant to answer. 
* **Data Storage:** All of our Data was stored as csv files. 

## 3. Website Architecture and Deployment
Our web application was developed to provide an interactive interface for exploring the answers to our research questions. 

* **Tech Stack:** The frontend and backend logic of the website were built in Python using Dash. We also utilized plotly within Dash to create the interactive visualizations.
* **Data Connection:** The Dash application does not make live API calls. Instead, it connects to the data by directly reading the pre-processed, question-specific CSV files.
* **Deployment:** The finalized Dash application is deployed and hosted on Render. 

You can access the live web application here: (https://data-science-project-2025-group13.onrender.com/)

## 4. How to Use the Application & Highlights
Our web application is designed to be interactive.

**Getting Started:**
1. **Homepage:** Upon opening the application, you will land on the homepage, which provides a brief overview of the project.
2. **Navigation:** From the homepage, use the navigation menu to jump to the specific pages dedicated to each of our 8 Research Questions.
3. **Interactive Analysis:** On each RQ page, you can interact directly with the diagrams. Use the available parameter controls (like dropdowns or sliders).

## 5. Explanation on Marking of Code via LLM
We used a straightforward tagging system: you will find the keyword LLM in the comments, immediately followed by a brief explanation of how the AI was used for that specific section. 





