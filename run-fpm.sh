#!/usr/bin/env bash

cd $HOME/src/rss-scraper-thing-bs4-python \
&& date > ./cron-01-time.log \
&& python3 fpm.py > ./cron-02-rss.log \
&& git add fpm.xml \
&& git commit -m "update fpm $(date)" \
&& git push
