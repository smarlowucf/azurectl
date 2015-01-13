#!/bin/bash
# this script turns the base64 encoded publish settings embedded cert
# into a pem certificate usable with the Microsoft Azure python SDK
# Here is the article that will explain you how to download the
# publishing profile:
#
# https://www.windowsazure.com/en-us/manage/linux/common-tasks/manage-certificates/
#

publish_settings=$1

if [ ! -e "$publish_settings" ];then
    echo "Usage: service <publish_settings_file>"
fi

if ! grep -q ManagementCertificate $publish_settings;then
    echo "No ManagementCertificate found in $publish_settings"
    exit 1
fi

grep ManagementCertificate $publish_settings |\
    cut -f2 -d\" > /tmp/cert.base64
python -c 'print open("/tmp/cert.base64", "rb").read().decode("base64")' >\
    /tmp/cert.pfx && rm -f /tmp/cert.base64

openssl pkcs12 -in /tmp/cert.pfx -nodes -passin pass: &&\
    rm -f /tmp/cert.pfx
