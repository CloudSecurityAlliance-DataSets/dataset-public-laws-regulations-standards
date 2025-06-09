#!/bin/bash
#########################
#
# Get all the sitemaps
#
# Get the main sitemap list
#
rm sitemap_index.xml
wget https://docs.aws.amazon.com/sitemap_index.xml
#
# remove the extra language ones
#
grep -oP '(?<=<loc>)[^<]+' sitemap_index.xml | grep -v "docs.aws.amazon.com/[a-z][a-z]_[a-z][a-z]/" | grep "secur" > sitemap-urls-secur.txt
grep -oP '(?<=<loc>)[^<]+' sitemap_index.xml | grep -v "docs.aws.amazon.com/[a-z][a-z]_[a-z][a-z]/" > sitemap-urls.txt
#
# Get all the sub sitemaps for "secur" (secure, security)
#
wget -x -i sitemap-urls-secur.txt
#
# Move this to a separate directory
#
mv ./docs.aws.amazon.com ./docs.aws.amazon.com-sitemaps-secur

#########################
#
# Extract all the URLs
#
find ./docs.aws.amazon.com-sitemaps-secur/ -type f | xargs grep -hoP '(?<=<loc>)[^<]+' > all-urls-secur.txt
#
# There shouldn't be any duplicates but let's make sure
#
sort ./all-urls-secur.txt |  grep -v "https://docs\.aws\.amazon\.com/[a-z][a-z]_[a-z][a-z]/" | uniq > ./all-urls-secur-uniq.txt
#
# Cleanup
#
#rm -rf ./docs.aws.amazon.com-sitemaps
########################
#
# Split into files of 1000
#
#split -l 1000 -d -a 3 all-urls-uniq.txt all-urls-uniq-
#
#for file in all-urls-uniq-[0-9][0-9][0-9]; do mv $file $file.txt; done
