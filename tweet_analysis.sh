#!/bin/bash
read -p "Enter the file would you want to analyze (remember to add .csv): " fileName

echo We are going to compare the frequency of 5 words in fileName 
read -p "Enter the first word you'd like to search for: " word1
read -p "Enter the second word you'd like to search for: " word2
read -p "Enter the third word you'd like to search for: " word3
read -p "Enter the fourth word you'd like to search for: " word4
read -p "Enter the fifth word you'd like to search for: " word5

# This will clean the file to delete the urls

countWord1=$(cat $fileName | grep -Ein "\b$word1 " | wc -l)
countWord2=$(cat $fileName | grep -Ein "\b$word2 " | wc -l)
countWord3=$(cat $fileName | grep -Ein "\b$word3 " | wc -l)
countWord4=$(cat $fileName | grep -Ein "\b$word4 " | wc -l)
countWord5=$(cat $fileName | grep -Ein "\b$word5 " | wc -l)

python3 bargraphing.py $word1 $word2 $word3 $word4 $word5 $countWord1 $countWord2 $countWord3 $countWord4 $countWord5