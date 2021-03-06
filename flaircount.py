#!/usr/bin/env python

import requests
import json
import pylab as pl
import numpy as np
import sys

class FlairCount:
    ''' Class wrapper for fetching data and generating stats. '''
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.api = 'http://reddit.com/r/' + self.subreddit + '/api/flairlist.json?limit=1000&after='
        self.saved_image = None

    def build_data(self):
        ''' Fetch data from api and populate dict with subscriber count for each flair. '''
        after = ''
        flairs = {}

        while True:
            data = json.loads(requests.get(self.api + after).content)

            for user in data['users']:
                flair = user['flair_css_class']

                if flair in flairs:
                    flairs[flair] += 1
                else:
                    flairs[flair] = 1

            if 'next' in data:
                after = data['next']
            else:
                break

        return flairs

    def build_chart(self, data):
        ''' Plot a bar chart with the acquired data. '''
        values = data.values()
        labels = data.keys()

        fig = pl.figure(figsize = (12, 10))
        ax = pl.subplot(111)
        width = 0.8
        rects = ax.bar(range(len(labels)), values, width = width)

        ax.set_title('/r/' + self.subreddit + ' flair distribution')
        ax.set_ylabel('Subscriber count')
        ax.set_xticks(np.arange(len(labels)) + width / 2)
        ax.set_xticklabels(labels, rotation = 90, size='x-small')

        # For displaying the corresponding value above each bar.
        for ii, rect in enumerate(rects):
            height = rect.get_height()
            pl.text(rect.get_x() + rect.get_width() / 2., 1.02 * height, '%s' % (values[ii]), ha = 'center', va = 'bottom', fontsize = 'xx-small')

        self.saved_image = self.subreddit + '_subreddit_flair_distribution.jpg'
        pl.savefig(self.saved_image)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: python flaircount.py <subreddit>'
    else:
        a = FlairCount(sys.argv[1])
        data = a.build_data()
        a.build_chart(data)
        print data
        print 'Saved to: ' + a.saved_image
