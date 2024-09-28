#!/bin/bash
#########################
#
# Get all the sitemaps
#
# Get the main sitemap list
#
rm sitemap.xml
wget https://cloud.google.com/sitemap.xml
#
# remove the extra language ones
#
grep -oP '(?<=<loc>)[^<]+' sitemap.xml > sitemap-urls.txt
#
# Get all the sub sitemaps for "secur" (secure, security)
#
wget -x -i sitemap-urls.txt
#
# Move this to a separate directory
#
mv ./cloud.google.com ./cloud.google.com-sitemaps-secur



grep -hoP '(?<=<loc>)[^<]+' ./cloud.google.com-sitemaps-secur/sitemap_* | grep -i secur > all-urls.txt

grep -v java all-urls.txt | grep -v "/python/" | grep -v "/nodejs/" | grep -v "/php/" | grep -v "/ruby/" | grep -v "/dotnet" | grep -v "/cpp/" | grep -v "/go/" \
    | grep -v "/beta/" | grep -v "/v[0-9]beta[0-9]/" | grep -v "/v[0-9]p[0-9]beta[0-9]/" | grep -v "/v[0-9]beta/"  | grep -v ".v1beta1$" \
    | grep -v "/v[0-9]alpha[0-9]/" | grep -v "/alpha/" \
    | grep -v "hl=" \
    | grep -v "https://cloud.google.com/security-command-center/docs/reference/rest/v1/" | grep -v "https://cloud.google.com/service-mesh/v1.1[0-9]/" | grep -v "https://cloud.google.com/service-mesh/v1.2[0-1]/" \
    | grep -v "https://cloud.google.com/apigee/docs/hybrid/v1.9/" | grep -v "https://cloud.google.com/apigee/docs/hybrid/v1.1[0-2]/" \
    | grep -v "https://cloud.google.com/distributed-cloud/edge/1.[5-6]" | grep -v "https://cloud.google.com/distributed-cloud/edge/1.7.0" \
    | sort > all-urls-secur.txt

wget -x -i all-urls-secur.txt

convert-all-google-files-to-markdown-in-place.py ./cloud.google.com

# then move all the markdown files to a filename with the full path in ../azure-docs-secur:

mkdir gcp-docs-secur

cd cloud.google.com

find . -type f -name "*.md" | grep -i secur | while read filepath; do
  newpath=$(echo "$filepath" | sed 's|^\./||' | sed 's/\//-/g')
  cp "$filepath" "../gcp-docs-secur/$newpath"
  echo "$filepath"
done

cd ..

# then smash them all together ("pip3 install files-to-prompt"):

files-to-prompt ./gcp-docs-secur > gcp-security-docs-all.md

#and upload them to the chatbot.
