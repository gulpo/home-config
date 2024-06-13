#!/usr/bin/perl
use MIME::Base64;
print encode_base64($ARGV[0]);
