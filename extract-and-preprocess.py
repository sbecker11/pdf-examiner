import os
import requests
from datetime import datetime
from PyPDF2 import PdfFileReader
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from huggingface_hub import login

# authentidcate with Hugging Face
login()

# Define paths
DEFAULT_FOLDER_PATH = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Books")
log_file = "./success_log.txt"
error_log_file = "./error_log.txt"

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Function to list all PDF files in the folder
def list_pdf_files(folder):
    return [f for f in os.listdir(folder) if f.endswith('.pdf')]

# Function to read log files and get processed files
def read_processed_log(success_log, error_log):
    processed_files = set()
    if os.path.exists(success_log):
        with open(success_log, 'r') as f:
            processed_files.update(line.split(',')[0] for line in f.readlines())
    if os.path.exists(error_log):
        with open(error_log, 'r') as f:
            processed_files.update(line.split(',')[0] for line in f.readlines())
    return processed_files

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        reader = PdfFileReader(f)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
    return text

# Function to preprocess text using NLTK
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]  # Remove punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]  # Remove stopwords
    return tokens

# Function to tokenize text using Hugging Face tokenizer
def tokenize_text(tokens, tokenizer):
    return tokenizer(' '.join(tokens), padding="max_length", truncation=True, max_length=512)["input_ids"]

# Load the selected model and tokenizer from Hugging Face Hub
model_name = "AWS-Sage"
tokenizer = GPT2Tokenizer.from_pretrained(model_name, use_auth_token=True)
model = GPT2LMHeadModel.from_pretrained(model_name, use_auth_token=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
    push_to_hub=False  # Set to False since we are not pushing to the hub in this script
)

# Main processing function
def process_pdfs():
    pdf_files = list_pdf_files(DEFAULT_FOLDER_PATH)
    print(f"Found {len(pdf_files)} PDF files in the folder '{DEFAULT_FOLDER_PATH}'.")

    processed_files = read_processed_log(log_file, error_log_file)
    total_tokens = 0

    for pdf_file in pdf_files:
        if pdf_file in processed_files:
            print(f"Skipping already processed file: {pdf_file}")
            continue
        
        pdf_path = os.path.join(DEFAULT_FOLDER_PATH, pdf_file)
        try:
            text = extract_text_from_pdf(pdf_path)
            tokens = preprocess_text(text)
            tokenized_input = tokenize_text(tokens, tokenizer)
            dataset = Dataset.from_dict({"input_ids": [tokenized_input]})
            
            # Train the model incrementally
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=dataset,
            )
            trainer.train()
            
            # Save the model after each batch
            model.save_pretrained("./results")
            tokenizer.save_pretrained("./results")
            
            with open(log_file, 'a') as sf:
                sf.write(f"{pdf_file},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"Processed '{pdf_file}': {len(tokens)} tokens sent.")
        except Exception as e:
            with open(error_log_file, 'a') as ef:
                ef.write(f"{pdf_file},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{str(e)}\n")
            print(f"Error processing '{pdf_file}': {str(e)}")

if __name__ == "__main__":
    process_pdfs()