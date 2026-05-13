#!/bin/bash

# mkdirs to hold the files

mkdir apigee
mkdir architecture
mkdir chronicle
mkdir compute-docs
mkdir docs
mkdir functions
mkdir kubernetes
mkdir learn-security-mandiant-academy
mkdir other
mkdir sdk-gcloud-reference
mkdir secure-source-manager
mkdir secure-web-proxy
mkdir security
mkdir security-command-center
mkdir security-compliance
mkdir security-products
mkdir service-mesh
mkdir skus-sku-groups
mkdir software-supply-chain-security-docs
mkdir workflow

# Move files into their dirs and then do "other" (the remaining)

mv apigee*.md apigee
mv architecture*.md architecture
mv chronicle*.md chronicle
mv compute-docs*.md compute-docs
mv docs*.md docs
mv functions*.md functions
mv kubernetes*.md kubernetes
mv learn-security-mandiant-academy*.md learn-security-mandiant-academy
mv sdk-gcloud-reference*.md sdk-gcloud-reference
mv secure-source-manager*.md secure-source-manager
mv secure-web-proxy*.md secure-web-proxy
mv security*.md security
mv security-command-center*.md security-command-center
mv security-compliance*.md security-compliance
mv security-products*.md security-products
mv service-mesh*.md service-mesh
mv skus-sku-groups*.md skus-sku-groups
mv software-supply-chain-security-docs*.md software-supply-chain-security-docs
mv workflow*.md workflow

mv *.md other

# files to prompt every dir

for i in *; do cd $i; files-to-prompt ./ > ../$i.output.md; cd ..; echo $i; done
