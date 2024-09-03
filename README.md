# extract-and-preprocess

# Objective
read a corpus of PDF files to train an LLM to create exam questions with answers and explanations.

### Dealing with git push failure
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

Still whenever I run git push I get the following:

> git push
fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

This article saved my life, explaining how to resolve the git push RPC error.
https://medium.com/swlh/everything-you-need-to-know-to-resolve-the-git-push-rpc-error-1a865fd1ebea

### Pre-Installation steps:
As described at https://www.nltk.org/data.html
Run the following from terminal in the project root folder

python -m nltk.downloader all

mkdir /usr/local/share/nltk_data
export NLTK_DATA=/usr/local/share/nltk_data
