# Getting all the AWS docs

run get-all-sitemaps-secur-files.sh

then run convert-html-to-markdown-in-place.py

then move all the markdown files to a filename with the full path:

```
find . -type f -name "*.md" | while read filepath; do
  newpath=$(echo "$filepath" | sed 's|^\./||' | sed 's/\//-/g')
  mv "$filepath" "$newpath"
done
```

then smash them all together ("pip3 install files-to-prompt"):

```
files-to-prompt ./ > ../aws-security-docs-all.md
```

and upload them to the chatbot.
