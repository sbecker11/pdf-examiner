import sys
import os
import PyPDF2
from datetime import datetime
import nltk

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    
    print(f"Number of tokens: {len(tokens)}")
    return tokens

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_pdf_file(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    tokens = preprocess_text(text)
    return text, tokens

def read_processed_log(log_file, error_log_file):
    processed_files = set()
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as lf:
            processed_files.update(line.split(',')[0] for line in lf.read().splitlines())
    
    if os.path.exists(error_log_file):
        with open(error_log_file, 'r') as ef:
            processed_files.update(line.split(',')[0] for line in ef.read().splitlines())
    
    print(f"Found {len(processed_files)} files already processed.")
    return processed_files

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract-and-preprocess.py <folder_path> <tokens_file>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    tokens_file = sys.argv[2]
    log_file = 'processed_files.log'
    error_log_file = 'error_files.log'
    
    DEFAULT_FOLDER_PATH = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Books")
    DEFAULT_TOKENS_FILE = os.path.join(os.getcwd(), "tokens.txt")
    
    if folder_path in ['default', '-']:
        folder_path = DEFAULT_FOLDER_PATH
    if tokens_file in ['default', '-']:        
        tokens_file = DEFAULT_TOKENS_FILE

    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        sys.exit(1)

    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files in the folder '{folder_path}'.")

    processed_files = read_processed_log(log_file, error_log_file)
    total_tokens = 0

    for pdf_file in pdf_files:
        if pdf_file in processed_files:
            print(f"Skipping already processed file: {pdf_file}")
            continue
        
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            print(f"Processing '{pdf_file}'...")
            text, tokens = process_pdf_file(pdf_path)
            num_tokens = len(tokens)
            num_chars = len(text)
            num_words = len(text.split())
            
            with open(tokens_file, 'a') as tf:
                tf.write(' '.join(tokens) + '\n')
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a') as lf:
                lf.write(f"{pdf_file},{timestamp},{num_chars},{num_words},{num_tokens}\n")
            
            total_tokens += num_tokens
            print(f"Processed '{pdf_file}': {num_tokens} tokens added. Total tokens: {total_tokens}")
        except Exception as e:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(error_log_file, 'a') as ef:
                ef.write(f"{pdf_file},{timestamp},{str(e)}\n")
            print(f"Error processing '{pdf_file}': {str(e)}")

if __name__ == "__main__":
    main()