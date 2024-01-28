#!/bin/bash

#prompt user for input
read -p "Enter your whatsapp access token: " WHATSAPP_ACCESS_TOKEN
read -p "Enter whatsapp API URL (include version): " WHATSAPP_API_URL
read -p "Enter whatsapp webhook verification token: " VERIFY_TOKEN
read -p "Enter whatsapp Number ID: " NUMBER_ID
read -p "Enter path to google service account json file: " SERVICE_ACCOUNT_PATH
read -p "Enter google cloud project ID: " PROJECT_ID
read -p "Enter redis URL (default: redis://localhost:6379): " REDIS_URL

#check if redis url is empty
if [-z "$REDIS_URL"]
then
    REDIS_URL="redis://localhost:6379"
fi

#set environment variables
cat << EOF > .env
WHATSAPP_ACCESS_TOKEN=$WHATSAPP_ACCESS_TOKEN
WHATSAPP_API_URL=$WHATSAPP_API_URL
VERIFY_TOKEN=$VERIFY_TOKEN
NUMBER_ID=$NUMBER_ID
SERVICE_ACCOUNT_PATH=$SERVICE_ACCOUNT_PATH
PROJECT_ID=$PROJECT_ID
REDIS_URL=$REDIS_URL

echo ".env file generated"