# extract-and-preprocess

# Objective
read a corpus of PDF files to train an LLM to create exam questions with answers and explanations.

### Initial github setup
inital setup was complicated due to the fact that
I tried to upload a huge tokens.txt file.

The offending file was removed from the github cache
and then added to .github file.

git push stil not working
used github's file uploader to manually upload project
files

then in order to synchronize local copy of main branch
with remote, had to use 
git pull origin main --allow-unrelated-histories


### Pre-Installation steps:
As described at https://www.nltk.org/data.html
Run the following from terminal in the project root folder

python -m nltk.downloader all

mkdir /usr/local/share/nltk_data
export NLTK_DATA=/usr/local/share/nltk_data
