from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
import torch
import os


class ValdevianTranslator:
    def __init__(self, model_name):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch.set_num_threads(14)
        print(f"Using device: {self.device}")

        # Load the pretrained translation model and tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir="D:\\huggingface\\hub", model_max_length=512)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir="D:\\huggingface\\hub").to("cuda")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Load the dataset
        with open(f"{current_dir}\\output.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Create the translation dictionary
        self.dataset = {}
        for line in lines:
            try:
                word, translation = line.strip().lower().split("\t")
                word = word.lower()  # Convert word to lowercase
                translation = translation.replace('æ', 'ya')  # Replace 'æ' with 'ae'
                self.dataset[word] = translation.lower()  # Convert translation to lowercase
            except ValueError:
                print(f"Error: Unable to split line '{line.strip()}' into two values")
    
    def generate_response(self, input_text):
        input_words = input_text.lower().replace("æ", "ya").split()
        output_words = []
        for input_word in input_words:
            # Check for exact match first
            if input_word in self.dataset:
                input_text = f"{self.dataset[input_word]}"
            else:
                # Check for partial matches
                for word in self.dataset:
                    if input_word in word:
                        input_text = f"{self.dataset[word]}"
                        break

            input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
            model_outputs = self.model.generate(input_ids, max_length=512)
            model_decoded = self.tokenizer.batch_decode(model_outputs, skip_special_tokens=True)
            output_words.append(model_decoded[0])
        output_text = " ".join(output_words)
        print(output_text)
        return output_text
    def train(self, model_name):
        valdtrans = ValdevianTranslator(model_name=model_name)
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=5,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset
        )
        trainer.train(model_path=model_name if os.path.isdir(model_name) else None)

