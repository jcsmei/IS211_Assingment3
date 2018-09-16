#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211_Assingment3. A simple program for text processing."""

import argparse
import csv
import datetime
import operator
import re
import urllib2

def downloadData(url):
    """A function for downloading data.

        Args:
            url (string): a link for the data download.

        Returns:
            data : Data provded by the URL.

        Examples:
            >>> abc = downloadData(
            "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv")
    """
    datafile = urllib2.urlopen(url)
    return datafile


def processData(datafile):
    """A function to process data from URL.

        Args:
            datafile (csv): A CSV file provided bu the URL.

        Returns:
            msg (string): A message for image stats.

        Examples:
            >>> processData(abc)
            Image requests account for 78.8% of all requests.
            The most used browser is Chrome.
    """
    csvData =  csv.reader(datafile)
    date_format = "%Y-%m-%d %H:%M:%S"
    dayHour = {i:0 for i in range(0, 24)}
    clicks = 0
    imgCount = 0

    chrome = 0
    msie = 0
    safari = 0
    firefox = 0

    for row in csvData:
        result = {"path": row[0], "date": row[1], "browser": row[2],
                  "status": row[3], "size": row[4]}
        date = datetime.datetime.strptime(result["date"], date_format)
        dayHour[date.hour] = dayHour[date.hour] + 1
        
        clicks += 1
        if re.search(r"\.(?:jpg|jpeg|gif|png)$", result["path"], re.I | re.M):
            imgCount +=1
        elif re.search("chrome", result["browser"], re.I):
            chrome += 1
        elif re.search("msie", result["browser"], re.I):
            msie += 1
        elif re.search("firefox", result["browser"], re.I):
            firefox += 1
        elif re.search("safari", result["browser"], re.I) and not re.search(
            "chrome", result["browser"], re.I):
            safari += 1

    browsers = {"Chrome": chrome, "MSIE": msie, "Safari": safari, "Firefox": firefox}
    imgRequests = (float(imgCount) / clicks) * 100

    print "Image requests account for {0:0.1f}% of all requests.".format(imgRequests)
    print "The most used browser is %s." % (max(browsers.iteritems(), key=operator.itemgetter(1))[0])

    sortOrder = sorted(dayHour.items(), key=operator.itemgetter(1))
    sortOrder.reverse()
    for i in sortOrder:
        print "Hour %02d has %s hits." % (i[0], i[1])


def main():
    """Data CSV data, process CSV data, display CSV data.

        Returns:
            A message returning the stats of a the most populat browsers used.

        Example:
            >>> 
            Please enter a valid URL.
            >>> abc = downloadData("http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv")
            >>> processData(abc)
            Image requests account for 78.8% of all requests.
            The most used browser is Chrome.
            Hour 04 has 1813 hits.
            Hour 01 has 1808 hits.
            Hour 03 has 1797 hits.
            Hour 02 has 1795 hits.
            Hour 00 has 1793 hits.
            Hour 05 has 994 hits.
            Hour 23 has 0 hits.
            ...
            Hour 06 has 0 hits.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="Enter URL to CSV file.")
    args = parser.parse_args()

    if args.url:
        try:
            csvData = downloadData(args.url)
            processData(csvData)
        except urllib2.URLError as e:
            print "Invalid URL."
    else:
        print "Please enter a valid URL."

if __name__ == "__main__":
    main()
