# Holidays Survey

![Holidays Survey mockup](/assets/readme-files/main-image.png)

This python project generates a survey (a holiday survey by default) and then displays the results by applying filters based on the age group and gender questions.
The most remarkable feature about the project is the ability to configure the entire survey from the linked google sheet, from the title, the introductory messages, the questions and answers, to the goodbye message.

All changes can be done just changing linked cells in the google sheet.

The project can be viewed here: https://holiday-survey-87184cd3dbf0.herokuapp.com/

## Table of Contents
1. [User Experience](#user-experience-ux)
    - [Project Goals](#project-goals)
    - [User Stories](#user-stories)
    - [Data Model](#data-model)
    - [Flowchart](#flowchart)
2. [Features](#features)
    - [Title screen](#title-screen)
    - [Main menu](#main-menu)
    - [Taking the survey](#taking-the-survey)
    - [Retake survey or show results](#retake-survey-or-show-results)
    - [View results](#view-results)
    - [Exit screen](#exit-screen)
3. [Technololgies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks, Libraries and Programmes](#frameworks-libraries-and-programmes)
4. [Testing](#testing)
    - [Testing User Stories](#testing-user-stories)
    - [Code Validation](#code-validation)
    - [Feature Testing](#feature-testing)
    - [Bugs](#bugs)
6. [Deployment](#deployment)
6. [Credit](#credit)
    - [Content](#content)
    - [Media](#media)
    - [Code](#code)
7. [Acknowledgements](#acknowledgements)

## User experience (UX)

### Project Goals

- Collect user answer for survey.
- Store data in a google sheet.
- Show survey result in a convenient format.
- show the questions and results in a tidy and clear way.
- Get a 100% reconfigurable format from the google sheet file.
- Implement data validation for all inputs.

### User Stories

- As a user, I would like to understand the program purpose.
- As a user, I would like to be able to choose whether to take the survey, show results or exit the program.
- As a user, I would like to be able to review my answers before submitting.
- As a user, I would like to be able to discard my answers and get the survey again.
- As a user, I would like to be able to see the survey result filtered by age group or gender.
- As a user, I would like to be able to choose which age group or gender I want to see the results of.
- As a user, I would like to be able to see different filtered result before exit.

### Data Model

The program uses a google sheet to store the information collected from the survey.

The google sheet also contains the questions as the column head, and the possible answers listed within each column.

A pandas dataframe is used to display the results tables.





