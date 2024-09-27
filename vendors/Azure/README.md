# Getting all the Azure docs

https://github.com/microsoftDocs/azure-docs/

then move all the markdown files to a filename with the full path in ../azure-docs-secur:

```
find . -type f -name "*.md" | grep -i secur | while read filepath; do
  newpath=$(echo "$filepath" | sed 's|^\./||' | sed 's/\//-/g')
  cp "$filepath" "../azure-docs-secur/$newpath"
  echo "$filepath"
done
```

then smash them all together ("pip3 install files-to-prompt"):

```
files-to-prompt ./ > ../azure-security-docs-all.md
```

and upload them to the chatbot.
