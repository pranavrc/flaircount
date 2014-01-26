#!/usr/bin/env python

import requests
import json
import pylab as pl
import numpy as np

class FlairCount:
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.api = 'http://reddit.com/r/' + self.subreddit + '/api/flairlist.json?limit=1000&after='

    def build_data(self):
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
        values = data.values()
        labels = data.keys()

        fig = pl.figure(figsize = (12, 10))
        ax = pl.subplot(111)
        width = 0.8 
        rects = ax.bar(range(len(labels)), values, width = width)

        ax.set_title('/r/Cricket flair distribution')
        ax.set_ylabel('Subscriber count')
        ax.set_xticks(np.arange(len(labels)) + width / 2)
        ax.set_xticklabels(labels, rotation = 90, size='x-small')

        for ii, rect in enumerate(rects):
            height = rect.get_height()
            pl.text(rect.get_x() + rect.get_width() / 2., 1.02 * height, '%s' % (values[ii]), ha = 'center', va = 'bottom', fontsize = 'xx-small')

        pl.savefig(self.subreddit + '_subreddit_flair_distribution.jpg')

if __name__ == "__main__":
    a = FlairCount('cricket')
    c = a.build_data()
    a.build_chart(c)
