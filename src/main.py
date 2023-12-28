import warnings
warnings.filterwarnings("ignore")

import numpy as np
import re
from bs4 import BeautifulSoup
import urllib
import ipaddress
import socket
import requests
import whois
from datetime import date
import time
from urllib.parse import urlparse
import pickle

class PhishingChecker:
    def __init__(self, url, domain, response):
        self.url = url
        self.domain = domain
        self.response = response
        self.protocol = urlparse(url).scheme
        
    def is_domain_https(self):
        try:
            domain_response = whois.whois(self.domain)
            if domain_response is not None:
                return "https" in domain_response.registrar.lower()  # Example - using registrar's information
        except:
            return False

    def is_valid_url(self):
        result = urlparse(self.url)
        return all([result.scheme, result.netloc])

    def is_accessible(self):
        try:
            self.response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

    def UsingIp(self):
        try:
            ipaddress.ip_address(self.url)
            return -1
        except:
            return 1

    def longUrl(self):
        length = len(self.url)
        if length < 54:
            return 1
        if 54 <= length <= 75:
            return 0
        return -1

    def shortUrl(self):
        shortening_services = [
            "bit.ly", "goo.gl", "shorte.st", "go2l.ink", "x.co", "ow.ly", "t.co", "tinyurl", "tr.im", "is.gd", "cli.gs",
            "yfrog.com", "migre.me", "ff.im", "tiny.cc", "url4.eu", "twit.ac", "su.pr", "twurl.nl", "snipurl.com",
            "short.to", "BudURL.com", "ping.fm", "post.ly", "Just.as", "bkite.com", "snipr.com", "fic.kr", "loopt.us",
            "doiop.com", "short.ie", "kl.am", "wp.me", "rubyurl.com", "om.ly", "to.ly", "bit.do", "lnkd.in", "db.tt",
            "qr.ae", "adf.ly", "ity.im", "q.gs", "po.st", "bc.vc", "twitthis.com", "u.to", "j.mp", "buzurl.com", "cutt.us",
            "u.bb", "yourls.org", "x.co", "prettylinkpro.com", "scrnch.me", "filoops.info", "vzturl.com", "qr.net",
            "1url.com", "tweez.me", "v.gd", "tr.im", "link.zip.net"]

        if any(service in self.url for service in shortening_services):
            return -1
        return 1

    def symbol(self):
        return -1 if "@" in self.url else 1

    def redirecting(self):
        if self.url.rfind('//') > 6:
            return -1
        return 1

    def prefixSuffix(self):
        try:
            match = re.findall('\-', self.domain)
            if match:
                return -1
            return 1
        except:
            return -1

    def subDomains(self):
        dot_count = len(re.findall("\.", self.url))
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1

    def check_https(self):
        if self.protocol == "https" or self.is_domain_https():
            return 1
        return -1
    
    def domainRegLen(self):
        try:
            whois_response = whois.whois(self.domain)
            expiration_date = whois_response.expiration_date
            creation_date = whois_response.creation_date

            age = (expiration_date.year - creation_date.year) * 12 + (expiration_date.month - creation_date.month)
            return 1 if age >= 12 else -1
        except:
            return -1

    def favicon(self):
        try:
            if 'favicon' in self.response.text:
                return 1
            return -1
        except Exception as e:
            print(f"Error finding favicon: {e}")
            return -1

    def nonStdPort(self):
        scheme = urlparse(self.url).scheme
        return 1 if scheme not in ('http', 'https') else -1

    def httpsDomainURL(self):
        if "https://" in self.domain:
            return 1
        else :
            return -1

    def requestURL(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        try:
            for img in soup.find_all('img', src=True):
                dots = [x.start(0) for x in re.finditer('\.', img['src'])]
                if self.url in img['src'] or self.domain in img['src'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            for audio in soup.find_all('audio', src=True):
                dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
                if self.url in audio['src'] or self.domain in audio['src'] or len(dots) == 1:
                    success = success + 1
                i = i + 1
            for embed in soup.find_all('embed', src=True):
                dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
                if self.url in embed['src'] or self.domain in embed['src'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            for iframe in soup.find_all('iframe', src=True):
                dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
                if self.url in iframe['src'] or self.domain in iframe['src'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            try:
                percentage = success / float(i) * 100
                if percentage < 22.0:
                    return 1
                elif ((percentage >= 22.0) and (percentage < 61.0)):
                    return 0
                else:
                    return -1
            except:
                return 0
        except:
            return -1

    def anchorURL(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        try:
            i, unsafe = 0, 0
            for a in soup.find_all('a', href=True):
                if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                        url in a['href'] or self.domain in a['href']):
                    unsafe = unsafe + 1
                i = i + 1

            try:
                percentage = unsafe / float(i) * 100
                if percentage < 31.0:
                    return 1
                elif ((percentage >= 31.0) and (percentage < 67.0)):
                    return 0
                else:
                    return -1
            except:
                return -1

        except:
            return -1

    def linksInScriptTags(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        try:
            i, success = 0, 0

            for link in soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', link['href'])]
                if self.url in link['href'] or self.domain in link['href'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            for script in soup.find_all('script', src=True):
                dots = [x.start(0) for x in re.finditer('\.', script['src'])]
                if self.url in script['src'] or self.domain in script['src'] or len(dots) == 1:
                    success = success + 1
                i = i + 1

            try:
                percentage = success / float(i) * 100
                if percentage < 17.0:
                    return 1
                elif ((percentage >= 17.0) and (percentage < 81.0)):
                    return 0
                else:
                    return -1
            except:
                return 0
        except:
            return -1

    def serverFormHandler(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        try:
            if len(soup.find_all('form', action=True)) == 0:
                return 1
            else:
                for form in soup.find_all('form', action=True):
                    if form['action'] == "" or form['action'] == "about:blank":
                        return -1
                    elif self.url not in form['action'] and self.domain not in form['action']:
                        return 0
                    else:
                        return 1
        except:
            return -1

    def infoEmail(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        try:
            if re.findall(r"[mail\(\)|mailto:?]", self.soup):
                return -1
            else:
                return 1
        except:
            return -1

    def abnormalURL(self):
        whois_response = whois.whois(self.domain)
        try:
            if self.response.text == whois_response:
                return 1
            else:
                return -1
        except:
            return -1

    def websiteForwarding(self):
        try:
            if len(self.response.history) <= 1:
                return 1
            elif len(self.response.history) <= 4:
                return 0
            else:
                return -1
        except:
            return -1

    def statusBarCust(self):
        try:
            if re.findall("<script>.+onmouseover.+</script>", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def disableRightClick(self):
        try:
            if re.findall(r"event.button ?== ?2", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def usingPopupWindow(self):
        try:
            if re.findall(r"alert\(", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def iframeRedirection(self):
        try:
            if re.findall(r"[<iframe>|<frameBorder>]", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def ageofDomain(self):
        whois_response = whois.whois(self.domain)
        try:
            creation_date = whois_response.creation_date
            try:
                if (len(creation_date)):
                    creation_date = creation_date[0]
            except:
                pass

            today = date.today()
            age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
            if age >= 6:
                return 1
            return -1

        except:
            return -1

    def dnsRecording(self):
        whois_response = whois.whois(self.domain)
        try:
            creation_date = whois_response.creation_date
            try:
                if (len(creation_date)):
                    creation_date = creation_date[0]
            except:
                pass

            today = date.today()
            age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
            if age >= 6:
                return 1
            return -1
        except:
            return -1

    def websiteTraffic(self):
        try:
            rank = \
            BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + self.url).read(), "xml").find(
                "REACH")['RANK']
            if (int(rank) < 100000):
                return 1
            return 0
        except:
            return -1

    def pageRank(self):
        try:
            rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": self.domain})

            global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
            if global_rank > 0 and global_rank < 100000:
                return 1
            return -1
        except:
            return -1

    def googleIndex(self):
        try:
            site = re.search(self.url, 5)
            if site:
                return 1
            else:
                return -1
        except:
            return 1

    def linksPointingToPage(self):
        try:
            number_of_links = len(re.findall(r"<a href=", self.response.text))
            if number_of_links == 0:
                return 1
            elif number_of_links <= 2:
                return 0
            else:
                return -1
        except:
            return -1

    def statsReport(self):
        try:
            ip_address = socket.gethostbyname(self.domain)
            url_match = re.search(r'at\.ua|usa\.cc|baltazarpresentes\.com\.br', self.url)
            ip_match = re.search(r'146\.112\.61\.108|213\.174\.157\.151', ip_address)

            if url_match or ip_match:
                return -1
            return 1
        except:
            return 1

if __name__ == "__main__":
    base_url = input("Enter URL: ")
    response = requests.get(base_url, allow_redirects=True)
    url = response.url
    domain = urlparse(url).netloc
    start = time.time()
    reasons = []
    columns = []
    checker = PhishingChecker(url, domain, response)

    if checker.is_valid_url() or checker.is_accessible() or checker.is_domain_https():
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

    if result == -1:
        print("The website may be phishing due to following reason:")
        for i in range(len(columns[0])):
            if columns[0][i] == -1:
                print(reasons[i])

    else:
        print("This website is safe to use.")
        print(columns[0])
    end = time.time()
    print("Time Taken:",end-start)

#https://lotto-india.com/