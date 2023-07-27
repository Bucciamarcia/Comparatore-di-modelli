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

def generate_prompt_list():
    """Genera una lista di prompt che verranno utilizzati per comparare e valutare la qualità di due modelli di intelligenza artificiale."""
    prompts = ai.gpt_call(engine="gpt-4",
    messages=[
        {"role": "user", "content": "Generate an array of 10 prompts that will be used to compare and evaluate the quality of two artificial intelligence models. The prompts should all focus on creating code, either Python, Javascript, or php. The code you ask to generate should be at the level where a junior programmer (2 years of experience) should be able to do it with a lot of effort, but wouldn't be too hard for a senior programmer. Prompts can be long. Generate prompts that will require either a lot of creativity (to evaluate the creativity of the models) or lot of reasoning (to evaluate the reasoning of the models). Always give enough context in your prompt, so that the evaluator has the material to evaluate the quality of the answer. In your prompts, ask the models to elaborate on the answer, so that the evaluator can evaluate the quality of the reasoning. If appropriate, ask the model to provide a conclusion or reccomendation."}
    ],
    functions=[
    {
      "name": "interrogate_models",
      "description": "Use the list of prompts to determine which model is better at answering questions.",
      "parameters": {
        "type": "object",
        "properties": {
          "prompts": {
            "type": "array",
            "description": "The list of prompts to use to interrogate the models.",
            "items": {
                "type": "string"
            }
          }
        },
        "required": ["prompts"]
      }
    }
  ],
  function_call="interrogate_models",
  temperature=1
  )
    prompts = json.loads(prompts)
    prompts_list = json.loads(prompts['arguments'])['prompts']
    print(json.dumps(prompts_list, indent=4))
    return prompts_list

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
            {"role": "system", "content": f"You are an expert evaluator of AI models. Your job is to determine which of the two models gives a better answer to the prompt. Base your answers on holistic factors such as the correctness of the response, depth of the answers, reasoning abilities, how well it follows the prompt, etc. This is the prompt that the two AI models were given: {prompt}"},
            {"role": "user", "content": f"* model 1 answer: {answer_1}\n* model 2 answer: {answer_2}"}
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
                            "enum": ["model-1", "model-2"]
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

def update_counters(winner):
    """Aggiorna i contatori dei modelli vincitori."""
    global gpt_3_5_turbo_wins
    global vertex_ai_wins
    if winner == "model-1":
        gpt_3_5_turbo_wins += 1
    elif winner == "model-2":
        vertex_ai_wins += 1

def append_results(prompt, answer_1, answer_2, winner, reason):
    """Aggiunge i risultati del test al file di output."""
    with open("output.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f"prompt: {prompt}\n\n")
        output_file.write(f"answer 1: {answer_1}\n\nanswer 2: {answer_2}\n\nwinner: {winner}\nreason: {reason}\n\n--------------\n\n")

def calculate_final_score(prompts):
    """Calcola il punteggio finale dei due modelli e scrive i dati nel file di output e in console."""
    gpt_3_5_average_time = gpt_3_5_total_time / len(prompts)
    vertex_ai_average_time = vertex_ai_total_time / len(prompts)
    with open("output.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f"gpt-3.5-turbo wins: {gpt_3_5_turbo_wins} / {len(prompts)}\nvertex-ai wins: {vertex_ai_wins} / {len(prompts)}\n\n")
        output_file.write(f"gpt-3.5-turbo average time: {gpt_3_5_average_time}\nvertex-ai average time: {vertex_ai_average_time}")
    print(f"gpt-3.5-turbo wins: {gpt_3_5_turbo_wins} / {len(prompts)}")
    print(f"vertex-ai wins: {vertex_ai_wins} / {len(prompts)}")

def main():
    create_output_file()
    prompts = generate_prompt_list()
    for prompt in prompts:
        answer_1 = call_gpt3(prompt)
        answer_2 = call_bison(prompt)
        winner, reason = gauntlet(prompt, answer_1, answer_2)
        update_counters(winner)
        append_results(prompt, answer_1, answer_2, winner, reason)
    calculate_final_score(prompts)

if __name__ == "__main__":
    main()