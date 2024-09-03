from random import random
from transformers import AutoTokenizer, AutoModelForCausalLM # type: ignore

class ExamGenerator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_question(self, context):
        prompt = f"Generate a question based on this text: {context}\nQuestion:"
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=100, num_return_sequences=1)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def generate_options(self, question, correct_answer):
        prompt = f"Generate 3 incorrect options for this question and answer:\nQuestion: {question}\nCorrect Answer: {correct_answer}\nIncorrect Options:"
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=200, num_return_sequences=1)
        options = self.tokenizer.decode(output[0], skip_special_tokens=True).split('\n')
        return options[:3]  # Return only the first 3 options

    def create_exam(self, contexts, num_questions):
        exam = []
        for i in range(num_questions):
            context = contexts[i % len(contexts)]  # Cycle through contexts if needed
            question = self.generate_question(context)
            correct_answer = self.generate_question(f"Answer this question: {question}")
            options = self.generate_options(question, correct_answer)
            options.append(correct_answer)
            random.shuffle(options)
            exam.append({
                'question': question,
                'options': options,
                'correct_answer': correct_answer
            })
        return exam

# Usage
model_name = 'your_fine_tuned_model_name'
exam_generator = ExamGenerator(model_name)
processed_texts = []  # Define the variable processed_texts
contexts = processed_texts  # From the previous step
exam = exam_generator.create_exam(contexts, num_questions=10)

# Print the exam
for i, question in enumerate(exam, 1):
    print(f"Question {i}: {question['question']}")
    for j, option in enumerate(question['options'], 1):
        print(f"  {j}. {option}")
    print(f"Correct answer: {question['correct_answer']}\n")