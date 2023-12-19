# Classification-of-Twitter-users-based-on-a-health-criterion
This project aims to recognize whether a Twitter user suffers from an underlying disease based on their recent tweets.

This is done by gathering and processing tweets to train several machine learning models like Support Vector Machines, Random Forest, Logistic
Regression ,and LightGBM.

Here is a brief description for different files provided in this project:
- `Constants.py`: Contains constants and configurations used throughout the project.
- `queries.py`: Contains functions for scraping Twitter data related to specific diseases.
- `TweetProcessingToolkits.py`:  Contains utility functions for processing and cleaning Twitter text data.
- `UserSearch.py`: Contains functions for scraping tweets from users who mentioned being diagnosed with specific diseases and storing user-level tweet data.
