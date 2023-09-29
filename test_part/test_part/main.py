import warnings
warnings.filterwarnings("ignore")

import numpy as np
from scipy import stats
import math
import random
from collections import Counter
import itertools
import re
import googlesearch
# import seaborn as sns
from bs4 import BeautifulSoup
import urllib
import ipaddress
import socket
import requests
import whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse
import pickle

class PhishingChecker:
    def __init__(self, url, domain, response):
        self.url = url
        self.domain = domain
        self.response = response

    def is_valid_url(self):
        try:
            result = urlparse(self.url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def is_accessible(self):
        try:
            # response = requests.get(self.url)
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
    # UsingIP = UsingIp(url)

    def longUrl(self):
        if len(self.url) < 54:
            return 1
        if (len(self.url) >= 54 and len(self.url) <= 75):
            return 0
        else:
            return -1
    # LongURL = longUrl(url)

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
        else:
            return 1
    # ShortURL = shortUrl(url)


    def symbol(self):
        if re.findall("@", self.url):
            return -1
        return 1
    # Symbol = symbol(url)


    def redirecting(self):
        if self.url.rfind('//') > 6:
            return -1
        return 1
    # Redirecting = redirecting(url)

    def prefixSuffix(self):
        # domain = urlparse(self.url).netloc
        try:
            match = re.findall('\-', self.domain)
            if match:
                return -1
            return 1
        except:
            return -1
    # PrefixSuffix = prefixSuffix(url)

    def subDomains(self):
        dot_count = len(re.findall("\.", self.url))
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1
    # SubDomains = subDomains(url)

    def check_https(self):
        if re.match(r'^https://', self.url):
            return 1
        elif re.match(r'^http://', self.url):
            return -1
        else:
            return 0
    # HTTPS = check_https(url)

    def domainRegLen(self):
        # domain = urlparse(self.url).netloc
        whois_response = whois.whois(self.domain)
        try:

            expiration_date = whois_response.expiration_date
            creation_date = whois_response.creation_date
            try:
                if (len(expiration_date)):
                    expiration_date = expiration_date[0]
            except:
                pass
            try:
                if (len(creation_date)):
                    creation_date = creation_date[0]
            except:
                pass
            age = (expiration_date.year - creation_date.year) * 12 + (expiration_date.month - creation_date.month)
            if age >= 12:
                return 1
            return -1
        except:
            return -1
    # DomainRegLen = domainRegLen(url)

    def favicon(self):
        try:
            # response = requests.get(self.url)
            self.response.raise_for_status()

            soup = BeautifulSoup(self.response.text, 'html.parser')
            favicon_link = soup.find('link', rel='icon')

            if favicon_link is not None:
                return 1
            else:
                return -1
        except Exception as e:
            print(f"Error: {e}")
            return -1
    # Favicon = favicon(url)

    def nonStdPort(self):
        if urlparse(self.url).port not in (80,443):
            return 1
        else:
            return -1
    # NonStdPort = nonStdPort(url)

    def httpsDomainURL(self):
        if "https://" in self.domain:
            return 1
        else :
            return -1
    # HTTPSDomainURL = httpsDomainURL(url)

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
            # RequestURL = requestURL(url)

    def anchorURL(self):
        # domain = urlparse(self.url).netloc
        # response = requests.get(self.url)
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
    # AnchorURL = anchorURL(url)

    def linksInScriptTags(self):
        # domain = urlparse(self.url).netloc
        # response = requests.get(self.url)
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
    # LinksInScriptTags = linksInScriptTags(url)

    def serverFormHandler(self):
        # response = requests.get(self.url)
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
    # ServerFormHandler = serverFormHandler(url)

    def infoEmail(self):
        # response = requests.get(self.url)
        soup = BeautifulSoup(self.response.text, 'html.parser')
        try:
            if re.findall(r"[mail\(\)|mailto:?]", self.soup):
                return -1
            else:
                return 1
        except:
            return -1
    # InfoEmail = infoEmail(url)

    def abnormalURL(self):
        # response = requests.get(self.url)
        # domain = urlparse(self.url).netloc
        whois_response = whois.whois(self.domain)
        try:
            if self.response.text == whois_response:
                return 1
            else:
                return -1
        except:
            return -1
    # AbnormalURL = abnormalURL(url)

    def websiteForwarding(self):
        # response = requests.get(self.url)
        try:
            if len(self.response.history) <= 1:
                return 1
            elif len(self.response.history) <= 4:
                return 0
            else:
                return -1
        except:
            return -1
    # WebsiteForwarding = websiteForwarding(url)

    def statusBarCust(self):
        # response = requests.get(self.url)
        try:
            if re.findall("<script>.+onmouseover.+</script>", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1
    # StatusBarCust = statusBarCust(url)

    def disableRightClick(self):
        # response = requests.get(self.url)
        try:
            if re.findall(r"event.button ?== ?2", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1
    # DisableRightClick = disableRightClick(url)

    def usingPopupWindow(self):
        # response = requests.get(self.url)
        try:
            if re.findall(r"alert\(", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1
    # UsingPopupWindow = usingPopupWindow(url)

    def iframeRedirection(self):
        # response = requests.get(self.url)
        try:
            if re.findall(r"[<iframe>|<frameBorder>]", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1
    # IframeRedirection = iframeRedirection(url)

    def ageofDomain(self):
        # domain = urlparse(self.url).netloc
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
    # AgeofDomain = ageofDomain(url)

    def dnsRecording(self):
        # domain = urlparse(self.url).netloc
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
    # DNSRecording = dnsRecording(url)

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
    # WebsiteTraffic = websiteTraffic(url)

    def pageRank(self):
        # domain = urlparse(self.url).netloc
        try:
            rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": self.domain})

            global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
            if global_rank > 0 and global_rank < 100000:
                return 1
            return -1
        except:
            return -1
    # PageRank = pageRank(url)

    def googleIndex(self):
        try:
            site = re.search(self.url, 5)
            if site:
                return 1
            else:
                return -1
        except:
            return 1
    # GoogleIndex = googleIndex(url)

    def linksPointingToPage(self):
        # response = requests.get(self.url)
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
    # LinksPointingToPage = linksPointingToPage(url)

    def statsReport(self):
        # domain = urlparse(self.url).netloc
        try:
            url_match = re.search(
                'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',
                self.url)
            ip_address = socket.gethostbyname(self.domain)
            ip_match = re.search(
                '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',
                ip_address)
            if url_match:
                return -1
            elif ip_match:
                return -1
            return 1
        except:
            return 1
    # StatsReport = statsReport(url)

if __name__ == "__main__":
    base_url = input("Enter URL: ")
    response = requests.get(base_url, allow_redirects=True)
    url = response.url
    start = time.time()
    reasons = []
    columns = []
    checker = PhishingChecker(url, domain=urlparse(url).netloc, response = requests.get(url))

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
            "The URL has email addresses in it.",
            "This URL deviates from typical URL structures.",
            "This website forwards users to a different URL upon access.",
            "This website customizes or disables the browser's status bar.",
            "This website disables the right-click context menu.",
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

        with open("C:\\Users\\akshu\\Documents\\NotSoPhishy\\Model\\classifier-model.pkl", 'rb') as f:
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
    end = time.time()
    print("Time Taken:",end-start)

#https://lotto-india.com/

