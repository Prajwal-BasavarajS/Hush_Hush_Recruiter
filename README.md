Hush Hush recruiter

Hush Hush recruiter is an automated recruitment tool written in Python 3 that automates the entire analysis process of selecting potential candidate for Doodle firm. The secretive process automatically sents email to an candidate if he is selected for a potential role at Doodle.

Recruiter wants to ensure that

The algorithm to hire a candidate cannot be deterministic
The data points of potential candidates can be picked over the data source from internet.
The interface to provide the coding solutions should be invalidated after a specified period

Overview

Through API we try to connect with each datasources which will provide the details on activities availble on the activities with their application. All the datasources with normalised score will be populated to database which is common for all the source . From the source we implement our selection algorithm which will list down the potentional candidates and their position.

We pick each of the candidates and sent them an email based which will have all the link for the doodle challenge.

Data sources

We are picking GitHub as our main data Source 

Architecture

<img width="1440" height="810" alt="image" src="https://github.com/user-attachments/assets/b654158d-eb26-4175-8266-8c9911af38e1" />



We employ a Logistic Regression model enhanced with probability-based prediction techniques to intelligently evaluate and shortlist the top 25 most suitable candidates from the aggregated database. Each shortlisted candidate is then automatically notified via email, which includes a secure, time-bound link to an online coding environment. Within this environment, candidates must complete a programming challenge designed to assess their technical proficiency under realistic conditions. Once the submissions are received, the system performs a comprehensive evaluation by combining the coding performance score with the model’s predicted probability score, resulting in a ranked list of candidates. This ranked output is then presented to the HR manager, who uses these data-driven insights — alongside organizational priorities — to make the final hiring decisions, determining which candidates will advance in the recruitment process..

