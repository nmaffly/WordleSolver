# wordleSmith

## Introduction

Welcome to my Wordle Solver project! This website was born out of my genuine enjoyment of playing Wordle and a passion for puzzle solving—both in the traditional sense and in the realm of coding. Combining these interests with my love for web development, I decided to create a tool to assist fellow Wordle-ers and expand my programming skillset.


## Inspiration

Wordle is one of many puzzle games that I enjoy. However, my interest was really piqued after watching a [YouTube video](https://www.youtube.com/watch?v=v68zYyaEmEA) by 3brown1blue, in which he delves into his take on solving Wordle with information theory. I was inspired to take my own approach to solving Wordle as optimally as possible. This project represents not just a techincal challenge, but a personal endeavor to merge my hobbies with my technical skills.

## Development Process

### The Algorithm

The algorithm behind wordleSmith is based on a scoring system that evaluates each potential guess. The system scores words based on the frequency of their letters, both in general and within specific positions, as some letters are more likely to appear in certain spots than others. 

To enhance the solver's efficacy, I integrated common Wordle strategies I often use when playing. This includes strategic "elimination" guesses designed to rapidly narrow down the pool of potential answers, especially useful in tricky situations where nearly the entire word is known except for one or two letters. The algorithm also avoids plural words, which don't appear often in wordle answers.

### Testing and Performance

After rigorous testing—leveraging the New York Times' official answer list as a benchmark—and continuous optimization, the algorithm achieved remarkable success. It can solve 99% of Wordles in 6 guesses or fewer, boasting an impressive average guess count of just 3.8. 

# Technologies

- Flask: Python framework for the backend server and routing.
- Gunicorn: As the HTTP server for Heroku deployment.
- HTML/CSS/JavaScript: For the frontend presentation and interaction.
- Heroku: For app deployment and hosting.

  
