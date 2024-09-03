extract-and-preprocess

### Initial github setup
the files in this project were manually
uploaded to the repo using github's file uploader page.

then in order to synchronize local copy of main branch
with remote, had to use 
git pull origin main --allow-unrelated-histories


### Pre-Installation steps:
As described at https://www.nltk.org/data.html
Run the following from terminal in the project root folder

python -m nltk.downloader all

mkdir /usr/local/share/nltk_data
export NLTK_DATA=/usr/local/share/nltk_data
