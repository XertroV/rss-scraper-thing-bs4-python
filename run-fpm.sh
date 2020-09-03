#!/usr/bin/env bash

cd $HOME/src/rss-scraper-thing-bs4-python
(date | tee cron-01-time.log \
&& python3 -m pip install --user -r requirements.txt \
&& python3 fpm.py | tee cron-02-rss.log \
&& git add fpm.xml \
&& git commit -m "update fpm $(date)" \
&& git push
) 2>&1 | tee ./cron-00-full.log
