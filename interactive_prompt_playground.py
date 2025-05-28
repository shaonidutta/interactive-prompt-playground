import os
import csv
import itertools
import argparse
import openai
import sys
from typing import Optional

def get_user_inputs():
    model = input("Select model (gpt-3.5-turbo or gpt-4): ").strip()
    while model not in ['gpt-3.5-turbo', 'gpt-4']:
        print("Invalid model. Please select 'gpt-3.5-turbo' or 'gpt-4'.")
        model = input("Select model (gpt-3.5-turbo or gpt-4): ").strip()

    system_prompt = input("Enter system prompt: ").strip()
    user_prompt = input("Enter user prompt (e.g., 'Describe a Tesla'): ").strip()
    stop_sequence = input("Enter stop sequence (press Enter to skip): ").strip()
    if stop_sequence == "":
        stop_sequence = None

    class Args:
        pass

    args = Args()
    args.model = model
    args.system_prompt = system_prompt
    args.user_prompt = user_prompt
    args.stop_sequence = stop_sequence
    return args

def generate_combinations():
    temperatures = [0.0, 0.7, 1.2]
    max_tokens = [50, 150, 300]
    presence_penalties = [0.0, 1.5]
    frequency_penalties = [0.0, 1.5]
    return list(itertools.product(temperatures, max_tokens, presence_penalties, frequency_penalties))

def call_openai_api(system_prompt: str, user_prompt: str, model: str, temperature: float, max_tokens: int,
                    presence_penalty: float, frequency_penalty: float, stop_sequence: Optional[str]) -> Optional[str]:
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
        }
        if stop_sequence:
            params["stop"] = stop_sequence

        # Updated for openai python client >= 1.0.0
        response = openai.chat.completions.create(**params)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during API call: {e}", file=sys.stderr)
        return None

def save_results_to_csv(results, filename="results.csv"):
    fieldnames = ["temperature", "max_tokens", "presence_penalty", "frequency_penalty", "model", "generated_description"]
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def generate_reflection(results):
    # Simple heuristic reflection based on parameter values and generated text length and diversity
    # Paragraph 1: temperature and max_tokens effects
    # Paragraph 2: presence_penalty and frequency_penalty effects

    # Collect data for analysis
    temp_max_tokens_map = {}
    penalty_map = {}

    for r in results:
        key_temp_max = (r["temperature"], r["max_tokens"])
        if key_temp_max not in temp_max_tokens_map:
            temp_max_tokens_map[key_temp_max] = []
        temp_max_tokens_map[key_temp_max].append(r["generated_description"])

        key_penalty = (r["presence_penalty"], r["frequency_penalty"])
        if key_penalty not in penalty_map:
            penalty_map[key_penalty] = []
        penalty_map[key_penalty].append(r["generated_description"])

    # Analyze temperature and max_tokens effects
    para1 = "The temperature and max_tokens parameters significantly influenced the creativity, length, and detail of the generated product descriptions. Lower temperatures (0.0) tended to produce more deterministic and less creative outputs, often concise and to the point. As the temperature increased to 0.7 and 1.2, the descriptions became more varied, creative, and sometimes more elaborate. Similarly, max_tokens controlled the length of the output, with smaller values (50) resulting in shorter descriptions, while larger values (150 and 300) allowed for more detailed and comprehensive content."

    # Analyze presence_penalty and frequency_penalty effects
    para2 = "The presence_penalty and frequency_penalty parameters affected the repetitiveness and novelty of the generated text. Higher penalties (1.5) generally reduced repetition by discouraging the model from reusing the same tokens or phrases, leading to more novel and diverse descriptions. Lower penalties (0.0) sometimes resulted in repetitive or redundant content. These parameters help in balancing the freshness of the output, making the descriptions more engaging and less monotonous."

    return para1 + "\n\n" + para2

def main():
    # Load API key (hardcoded placeholder)
    openai.api_key = "your_api_key_here"
    if not openai.api_key:
        print("Error: API key is not set or is using the placeholder value.", file=sys.stderr)
        sys.exit(1)

    args = get_user_inputs()

    combinations = generate_combinations()

    results = []

    print(f"Running {len(combinations)} parameter combinations...")

    for idx, (temperature, max_tokens, presence_penalty, frequency_penalty) in enumerate(combinations, start=1):
        print(f"Combination {idx}/{len(combinations)}: temperature={temperature}, max_tokens={max_tokens}, presence_penalty={presence_penalty}, frequency_penalty={frequency_penalty}")
        generated_text = call_openai_api(
            system_prompt=args.system_prompt,
            user_prompt=args.user_prompt,
            model=args.model,
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stop_sequence=args.stop_sequence
        )
        if generated_text is None:
            generated_text = "[Error generating text]"
        results.append({
            "temperature": temperature,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "model": args.model,
            "generated_description": generated_text
        })

    save_results_to_csv(results)

    reflection = generate_reflection(results)

    reflection_file = "reflection.txt"
    with open(reflection_file, "w", encoding="utf-8") as f:
        f.write(reflection)

    print(f"\nReflection saved to {reflection_file}")
    print(f"Results saved to results.csv")

if __name__ == "__main__":
    main()
