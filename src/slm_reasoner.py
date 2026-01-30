from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class ReasonerSLM:
  def __init__(self, model_id="Qwen/Qwen2.5-1.5B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

  def respond(self, user_question, interpreted, retrieved, db_context=""):
    # ----------------------------
    # Build context
    # ----------------------------
    if retrieved:
        context = "\n".join(r["chunk"] for r in retrieved[:3])
    else:
        context = "No relevant knowledge found."

    system_prompt = f"""
You are a professional customer support assistant.

RULES:
- Use ONLY the information in the context.
- Never guess or guarantee outcomes.
- If order-related details are required, ask for the order number.
- If the user greets you or asks how you are, respond politely as a customer support agent
  and offer help with orders, shipping, returns, or refunds.
- Do NOT say you are an AI or mention emotions.
- Respond clearly in 1–2 sentences.

CONTEXT:
{context}

{db_context}
""".strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]

    input_ids = self.tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True
    ).to(self.model.device)

    outputs = self.model.generate(
        input_ids,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.3,
        top_p=0.9,
        eos_token_id=self.tokenizer.eos_token_id
    )

    # 🔑 CRITICAL PART: decode ONLY newly generated tokens
    generated_tokens = outputs[0][input_ids.shape[-1]:]
    answer = self.tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    return answer
