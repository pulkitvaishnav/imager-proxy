#!/bin/bash

# Generate self hosted certificate
openssl req -newkey rsa:2048 -nodes -keyout ./nginx/privkey.pem -x509 -days 36500 -out ./nginx/certificate.pem -subj "/C=US/ST=NRW/L=Earth/O=CompanyName/OU=IT/CN=www.example.com/emailAddress=email@example.com"


