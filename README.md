# Not So Phishy

## Introduction

**Not So Phishy** is a project designed to combat the prevalent threat of phishing attacks, which are among the most common cyber-attacks today. Unlike traditional hacking methods that target system vulnerabilities, phishing relies on exploiting human errors through social engineering.

Our solution empowers users with tools that leverage machine learning to recognize intricate patterns that may go unnoticed by humans. Our machine learning model, trained on a dataset of over 10,000 samples, assesses URLs before users click on them, providing real-time predictions about their trustworthiness. Our website also offers features such as a list of potential phishing sites identified by our model and a search bar for users to assess suspicious URLs instantly.

## Requirements

Before running the **Not So Phishy** project, ensure you have the following dependencies installed, which can be found in the `requirements.txt` file:

- Flask
- python-whois
- python-googlesearch
- scikit-learn==1.2.2

To install these dependencies, use the following command:

```bash
pip install -r requirements.txt
```

## Instructions to Run

Follow these steps to run the **Not So Phishy** project:

1. Clone the repository:

   ```bash
   git clone https://github.com/akshubawa/NotSoPhishy.git
   ```

2. Navigate to the project directory:

   ```bash
   cd notSoPhishy
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the project's dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the Flask application:

   ```bash
   python src/app.py
   ```

7. Access the **Not So Phishy** web interface in your web browser by navigating to `http://localhost:5000`.

Now, you can use the provided features to assess URLs for potential phishing threats and access information about reported phishing attacks worldwide.

Stay vigilant against phishing attacks with **Not So Phishy**! If you have any questions or need assistance, please don't hesitate to reach out.

# Screenshots
<img src="./assets/Screenshot 0.png">
<img src="./assets/Screenshot 1.png">
<img src="./assets/Screenshot 2.png">
<img src="./assets/Screenshot 3.png">
<img src="./assets/Screenshot 4.png">
<img src="./assets/Screenshot 5.png">
