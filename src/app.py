import pickle
from urllib.parse import urlparse
from flask import Flask, request, render_template
import numpy as np
import requests
import main as m
import os
app = Flask(__name__,static_folder='UI Part',template_folder='templates')

def analyze_url(url):
    checker = m.PhishingChecker(url, domain=urlparse(url).netloc, response = requests.get(url))

    if not checker.is_valid_url() or not checker.is_accessible():
        result = -1
    else:
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

        with open("Model\\classifier-model.pkl", 'rb') as f:
            model = pickle.load(f)

        prediction = model.predict(columns)
        result = prediction[0]
    return result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url", "")
    result = analyze_url(url)
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=False)
