## Drowsiness Detection System

A Python-based real-time drowsiness detection system using OpenCV. This system monitors eye closure duration and blink rate via webcam, providing real-time alerts to help prevent accidents caused by fatigue.

#Features
1. Face and Eye Detection:
   Leverages Haar cascade classifiers for detecting facial features and eyes.
   
3. Real-time Alerts:
   Triggers alerts if drowsiness is detected based on eye closure duration.
   
5. Blink Rate Monitoring:
   Tracks the user's blink rate and calculates blinks per minute.
   
# Requirements
1. Python: Version 3.x
2. Libraries:
> OpenCV
> NumPy

# Installation
1. Clone the Repository:
git clone https://github.com/diyaaistwal/drowsiness-detection.git
cd drowsiness-detection

2. Install Dependencies: Install the required libraries using:
pip install -r requirements.txt

3. Run the Script: Start the drowsiness detection system:
python main.py

# How It Works
1. Initialization:
A webcam is initialized with a resolution of 1280x720 pixels.
Haar cascades are used to detect faces and eyes.

2. Eye and Blink Monitoring:
The system calculates the total eye area and evaluates eye closure duration.
Detects blinks and calculates the blink rate (blinks per minute).

3. Drowsiness Detection:

If eyes remain closed for more than 1.5 seconds, the system displays a "DROWSY ALERT!" message and highlights the user status in red.
Displays the time eyes have been closed and current blink rate on the screen.

4. Real-time Visual Feedback:
Shows rectangles around detected faces and eyes.
Displays the current status (Active, Eyes Closing, or DROWSY!).

5. Exit the Program:
Press q to quit the application.

# Project Structure

drowsiness-detection/
├── main.py                 # Main script for drowsiness detection
├── haarcascades/           # Haar cascade XML files for face and eye detection
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
└── LICENSE                 # Project license

# Demo
Include screenshots or GIFs of the system in action to give users a clear idea of its functionality.

# Contributing
Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch:
git checkout -b feature-name
3. Commit your changes:
git commit -m "Add feature description"
4. Push the branch:
git push origin feature-name
5. Open a Pull Request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
> Haar cascade classifiers are based on the work of Paul Viola and Michael Jones.
> Inspired by safety concerns for drivers and machinery operators.

# Contact
For queries or suggestions, feel free to reach out:

Email: diya.istwal@gmail.com
GitHub: diyaaistwal

