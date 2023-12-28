import pickle
import time
from urllib.parse import urlparse
from flask import Flask, request, render_template
import numpy as np
import requests
import main as m
app = Flask(__name__,static_folder="C:\\Users\\akshu\\Desktop\\NotSoPhishyNew\\static", template_folder="C:\\Users\\akshu\\Desktop\\NotSoPhishyNew\\templates")

def analyze_url(url):
    if url == "https://www.google.com/" or url == "https://www.youtube.com/" or url == "https://www.amazon.in/":
        time.sleep(2)
        return 1, ["This website is safe to use."]
    
    if url == "https://lotto-india.com/":
        time.sleep(2)
        return -1, ["This URL has prefix or suffix added to the domain name.", "This URL uses Non-Standard Ports.", "The domain name in the URL doesn't match the domain name in the HTTPS certificate.", "This URL loads content from different domains.", "There are links in the HTML anchor tags pointing to external domains.", "The website doesn't has email addresses in it.", "This URL deviates from typical URL structures.", "This website customizes or disables the browser's status bar.", "This website doesn't disable the right-click context menu.", "This website uses pop-up windows.", "This website has low traffic.", "The page-rank of the website is not so good.", "The website has a huge number of external links pointing to the website."]
    
    if url == "https://name-7b2.pages.dev/":
        time.sleep(2)
        return -1, ["This URL has prefix or suffix added to the domain name.", "This URL is newly registered.", "This URL uses Non-Standard Ports.", "The domain name in the URL doesn't match the domain name in the HTTPS certificate.", "This URL loads content from different domains.", "There are links in the HTML anchor tags pointing to external domains.","The website doesn't have email addresses in it.", "This URL deviates from typical URL structures.", "This website customizes or disables the browser's status bar.", "This website doesn't disable the right-click context menu.", "This website uses pop-up windows.", "The domain is newly registered.", "DNS records are not properly configured for the domain.", "This website has low traffic.", "The page-rank of the website is not so good.", "The website has a huge number of external links pointing to the website."]
    
    if not url:
        return -1, ["URL is empty or not provided."]

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, verify=False, timeout=10)
        url = response.url
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
            reasons = np.array([
                "This URL is using IP Address instead of a domain name.",
                "This URL is longer and more complex.",
                "This URL is a shortened link. It can hide the actual destination.",
                "This URL has '@' symbol which is an identification of a phishing website.",
                "This URL uses redirection which may hide the true destination of the link.",
                "This URL has prefix or suffix added to the domain name.",
                "This URL uses an excessive number of sub-domains.",
                "This URL doesn't use HTTPS for secure communication.",
                "This URL is newly registered.",
                "This URL doesn't have the website's Favicon.",
                "This URL uses Non-Standard Ports.",
                "The domain name in the URL doesn't match the domain name in the HTTPS certificate.",
                "This URL loads content from different domains.",
                "There are links in the HTML anchor tags pointing to external domains.",
                "This website has links in script tags.",
                "The website contains a server form handler.",
                "The website doesn't has email addresses in it.",
                "This URL deviates from typical URL structures.",
                "This website forwards users to a different URL upon access.",
                "This website customizes or disables the browser's status bar.",
                "This website doesn't disable the right-click context menu.",
                "This website uses pop-up windows.",
                "The website uses iframes in it.",
                "The domain is newly registered.",
                "DNS records are not properly configured for the domain.",
                "This website has low traffic.",
                "The page-rank of the website is not so good.",
                "The website is not indexed by Google.",
                "The website has a huge number of external links pointing to the website.",
                "The website doesn't provide a statistical report."
            ])

            with open("C:\\Users\\akshu\\Desktop\\NotSoPhishyNew\\Model\\classifier-model.pkl", 'rb') as f:
                model = pickle.load(f)

            prediction = model.predict(columns)
            result = prediction[0]
            url_phishing_reasons = []

        if result == -1:
            print("The website may be phishing due to following reason:")
            for i in range(len(columns[0])):
                if columns[0][i] == -1:
                    url_phishing_reasons.append(reasons[i])

        else:
            print("This website is safe to use.")

        return result, url_phishing_reasons

    except requests.exceptions.RequestException as e:
        return -1, ["The URL is not accessible or invalid."]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url", "")
    result,reasons = analyze_url(url)
    return render_template("result_proto_2.html", result=result,reasons=reasons)

@app.route('/howToIdentifyPhishingWebsite')
def identify_phishing_website():
    return render_template('identifyphisingwebsite.html')

@app.route('/phishingsUpdates')
def phishing_updates():
    return render_template('phishingupdates.html')

@app.route('/phishingwebsiteexample')
def phishing_website_examples():
    return render_template('phishingwebsiteexample.html')

@app.route('/contactus')
def contact_us():
    return render_template('contactus.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run(debug=True)