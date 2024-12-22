#!/bin/bash
set +ex

VERSION="4.0.13"
URL="https://github.com/select2/select2/archive/refs/tags/${VERSION}.zip"
OUTPUT_ZIP="dist.zip"
curl -L -o $OUTPUT_ZIP $URL
unzip $OUTPUT_ZIP
rm $OUTPUT_ZIP

rm -dr js_lib_select2/static/js_lib_select2
mv select2-${VERSION}/dist js_lib_select2/static/js_lib_select2
rm -dr select2-${VERSION}
git add -v js_lib_select2/static/js_lib_select2
