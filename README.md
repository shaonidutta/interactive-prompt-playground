# Interactive Prompt Playground

This project provides a Python script to experiment with different prompt configurations and OpenAI GPT model parameters to generate product descriptions. It is designed as an educational tool to help users understand how various parameters affect text generation.

## Features

- Allows user input of:
  - System prompt
  - User prompt
  - Model selection (`gpt-3.5-turbo` or `gpt-4`)
  - Optional stop sequence (e.g., newline `\n`, period `.`, double newline `\n\n`, or custom tokens)
- Runs the prompt through all combinations of:
  - Temperature: 0.0, 0.7, 1.2
  - Max Tokens: 50, 150, 300
  - Presence Penalty: 0.0, 1.5
  - Frequency Penalty: 0.0, 1.5
- Saves all generated product descriptions and input parameters in a CSV file (`results.csv`)
- Generates a 2-paragraph reflection analyzing how the parameters influenced the outputs, saved in `reflection.txt`
- Includes error handling and uses the OpenAI API securely via environment variable for the API key

## How to Run

1. Ensure you have Python 3.7+ installed.
2. Install the OpenAI Python package if not already installed:

   ```
   pip install openai
   ```

3. Set your OpenAI API key in the script file `interactive_prompt_playground.py` by replacing the placeholder string `"your_api_key_here"` with your actual API key.

   > **Note:** The API key is now hardcoded in the script instead of being loaded from an environment variable.

   Example in `interactive_prompt_playground.py`:
   ```python
   openai.api_key = "your_actual_api_key_here"
   ```

4. Run the script from the terminal with:

   ```
   python interactive_prompt_playground.py
   ```

   The script will prompt you to enter:
   - Model selection (`gpt-3.5-turbo` or `gpt-4`)
   - System prompt
   - User prompt (e.g., "Describe a Tesla")
   - Optional stop sequence (press Enter to skip)

   Valid stop sequence examples include:
   - Newline character: `\n`
   - Period: `.`
   - Double newline: `\n\n`
   - Custom tokens or phrases marking the end of desired output

## Output

- The script will generate a `results.csv` file containing all parameter combinations and their corresponding generated product descriptions.
- A `reflection.txt` file will be created with a summary analysis of how the parameters affected the outputs.

## Summary

This script is an interactive playground for exploring how different OpenAI GPT model parameters influence text generation, specifically for product descriptions. It helps users learn about the effects of temperature, max tokens, presence penalty, and frequency penalty on creativity, length, detail, repetitiveness, and novelty of generated text.
