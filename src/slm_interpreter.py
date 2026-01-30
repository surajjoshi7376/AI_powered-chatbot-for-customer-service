from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import json
import re


class QueryInterpreter:
    def __init__(self, model_id="google/flan-t5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        self.model.config.pad_token_id = self.tokenizer.eos_token_id

    def interpret(self, question):
        prompt = f"""
Classify the user query.

Return ONLY valid JSON.
Do not explain anything.

Required keys:
intent, task, expanded_query

Valid intents:
definition, policy, faq, order_status, stock_check, return_policy, shipping

User question:
{question}

JSON:
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False
        )

        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            parsed = json.loads(match.group())
        except Exception:
            parsed = {
        "intent": "general_query",
        "task": "general_query",
        "expanded_query": question
    }

        if not parsed.get("expanded_query"):
            parsed["expanded_query"] = question

        return parsed
