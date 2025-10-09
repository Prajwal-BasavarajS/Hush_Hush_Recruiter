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
