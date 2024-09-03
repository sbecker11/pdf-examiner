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



# Preprocessing Explanation:
1. Authenticate with Hugging Face: The login function from huggingface_hub is called at the beginning of the script to ensure you are authenticated.
2. Download NLTK Data: The necessary NLTK data files (punkt and stopwords) are downloaded.
3. List PDF Files: The list_pdf_files function lists all PDF files in the specified folder.
4. Read Processed Logs: The read_processed_log function reads the success and error log files to get the list of processed files.
5. Extract and Preprocess Text: The script extracts text from each unprocessed PDF file and preprocesses it using NLTK.
6. Tokenize Text: The preprocessed text is tokenized using the Hugging Face tokenizer.
7. Incremental Training: The script sets up a Trainer with the loaded model and tokenized dataset, and trains the model incrementally for each unprocessed PDF file.
8. Save Model State: After processing each batch, the model and tokenizer are saved to ensure that the training state is maintained.
9. Logging: The script logs successful processing and errors to the respective log files.

By following these steps, you can ensure that your script includes the necessary authentication and text preprocessing steps, and that it handles incremental training effectively.

