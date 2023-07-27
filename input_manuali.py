import libreria_ai_per_tutti as ai
import json
import vertexai
from vertexai.preview.language_models import ChatModel
import time

gpt_3_5_turbo_wins = 0
vertex_ai_wins = 0
gpt_3_5_total_time = 0
vertex_ai_total_time = 0

def create_output_file():
    """Crea un file di output per salvare i risultati del test."""
    with open("output.txt", "w", encoding="utf-8") as output_file:
        output_file.write("")

prompt = input("prompt: ")

def call_gpt3(prompt):
    """Chiama l'API di OpenAI per generare un testo a partire da un prompt."""
    start_time = time.time()
    response = ai.gpt_call(messages=[
        {"role": "user", "content": prompt}
    ],
    )
    end_time = time.time()
    # Add time to total time
    global gpt_3_5_total_time
    gpt_3_5_total_time += end_time - start_time
    print(f"gpt3: {response}")
    return response

def call_bison(prompt):
    start_time = time.time()
    vertexai.init(project="script-ai-per-tutti", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat()
    response = chat.send_message(prompt, **parameters)
    end_time = time.time()
    # Add time to total time
    global vertex_ai_total_time
    vertex_ai_total_time += end_time - start_time
    response = response.text
    print(f"Vertex AI: {response}")
    return response

def gauntlet(prompt, answer_1, answer_2):
    """Valuta la qualità di due risposte e determina quale è migliore."""
    response = ai.gpt_call(
        engine="gpt-4",
        messages=[
            {"role": "system", "content": f"You are an expert evaluator of AI models. Your job is to determine which of the two models is better at answering questions. You have two answers to this prompt: {prompt}"},
            {"role": "user", "content": f"gpt-3.5-turbo answer: {answer_1}\nvertex-ai answer: {answer_2}"}
        ],
        functions=[
            {
                "name": "better_answer",
                "description": "Determine which model provided the best answer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "winning_model": {
                            "type": "string",
                            "description": "The model with the best answer.",
                            "enum": ["gpt-3.5-turbo", "vertex-ai"]
                        },
                        "reason": {
                            "type": "string",
                            "description": "The reason why the model won."
                        }
                    },
                    "required": ["winning_model", "reason"]
                }
            }
        ],
        function_call="better_answer",
    )
    response = json.loads(response)
    chicken_winner = json.loads(response['arguments'])['winning_model']
    reason = json.loads(response['arguments'])['reason']
    print(f"winner: {chicken_winner}")
    print(f"reason: {reason}")
    return chicken_winner, reason

def append_results(prompt, answer_1, answer_2, winner, reason):
    """Aggiunge i risultati del test al file di output."""
    with open("output.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f"prompt: {prompt}\n")
        output_file.write(f"answer 1: {answer_1}\nanswer 2: {answer_2}\nwinner: {winner}\nreason: {reason}")

def main():
    create_output_file()
    answer_1 = call_gpt3(prompt)
    answer_2 = call_bison(prompt)
    winner, reason = gauntlet(prompt, answer_1, answer_2)
    append_results(prompt, answer_1, answer_2, winner, reason)

if __name__ == "__main__":
    main()