import pickle
import time
from urllib.parse import urlparse
import numpy as np
import requests
import main as m
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data['text']
        response = requests.get(text, allow_redirects=True)
        url = response.url
        checker = m.PhishingChecker(url, domain=urlparse(url).netloc, response = requests.get(url))

        if checker.is_valid_url() or checker.is_accessible():
            columns = np.array([checker.UsingIp(), checker.longUrl(), checker.shortUrl(), checker.symbol(),
                            checker.redirecting(), checker.prefixSuffix(), checker.subDomains(), checker.check_https(),
                            checker.domainRegLen(), checker.favicon(), checker.nonStdPort(), checker.httpsDomainURL(),
                            checker.requestURL(), checker.anchorURL(), checker.linksInScriptTags(),
                            checker.serverFormHandler(),
                            checker.infoEmail(), checker.abnormalURL(), checker.websiteForwarding(),
                            checker.statusBarCust(),
                            checker.disableRightClick(), checker.usingPopupWindow(), checker.iframeRedirection(),
                            checker.ageofDomain(), checker.dnsRecording(), checker.websiteTraffic(), checker.pageRank(),
                            checker.googleIndex(), checker.linksPointingToPage(), checker.statsReport()])

            columns = columns.reshape(1, -1)

            with open("C:\\Users\\akshu\\Documents\\NotSoPhishy\\Model\\classifier-model.pkl", 'rb') as f:
                model = pickle.load(f)

                prediction = model.predict(columns)
                result = prediction[0]
            reasons_arr=[]
            if result == -1:
            #     for i in range(len(columns[0])):
            #         if columns[0][i] == -1:
            #             reasons_arr.append(reasons[i])
                processed_text = "The website may be phishing"
            else:
                processed_text = "This website is safe to use."
        return jsonify({'processedText': processed_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
