import pandas as pd
import requests
import random

# Step 1: Load the full list of German abusive words from GitHub
def load_german_abusive_words():
    # URL to the raw list of German profanity from GitHub
    url = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/de"
    response = requests.get(url)
    response.raise_for_status()

    # Parse the words from the response text
    words = set(
        word.strip().lower()
        for word in response.text.splitlines()
        if word.strip() and not word.startswith("#")
    )
    return list(words)

# Step 2: Process a sentence into tokens and token_labels
def process_text(text, label, abusive_words_set):
    if not isinstance(text, str):
        text = ""

    words = text.split()
    if label == 1:
        word_labels = [
            1 if word.lower().strip(".,!?\"'") in abusive_words_set else 0
            for word in words
        ]
    else:
        word_labels = [0] * len(words)
    return words, word_labels

# Step 3: Generate synthetic abusive rows with a mix of abusive words
def generate_synthetic_abusive_rows(abusive_words_list, count=1000):
    synthetic_data = []

    for _ in range(count):
        sentence_length = random.randint(3, 7)
        words = random.choices(abusive_words_list, k=sentence_length)
        sentence = " ".join(words)
        tokens, labels = process_text(sentence, 1, set(abusive_words_list))
        synthetic_data.append({'tokens': tokens, 'token_labels': labels})
    
    return pd.DataFrame(synthetic_data)

# Step 4: Main function to combine original and synthetic abusive data
def convert_text_csv_with_synthetic(text_csv_path, output_csv_path=None, num_synthetic_rows=1000):
    abusive_words_list = load_german_abusive_words()
    abusive_words_set = set(abusive_words_list)

    # Load and clean the original CSV
    original_df = pd.read_csv(text_csv_path)
    original_df = original_df.dropna(subset=['text', 'label'])

    # Process original rows
    original_tokens = []
    original_labels = []

    for _, row in original_df.iterrows():
        tokens, token_labels = process_text(row['text'], row['label'], abusive_words_set)
        original_tokens.append(tokens)
        original_labels.append(token_labels)

    original_data = pd.DataFrame({
        'tokens': original_tokens,
        'token_labels': original_labels
    })

    # Generate synthetic abusive data
    synthetic_data = generate_synthetic_abusive_rows(abusive_words_list, num_synthetic_rows)

    # Combine both original and synthetic data
    combined_df = pd.concat([original_data, synthetic_data], ignore_index=True)

    # Save to CSV if a path is provided
    if output_csv_path:
        combined_df.to_csv(output_csv_path, index=False)

    return combined_df

# -------------------------------
# 👇 Example usage of the script
# -------------------------------
if __name__ == "__main__":
    text_csv_path = "German.csv"  # Path to your German text + label CSV
    output_csv_path = "combined_german_with_synthetic.csv"  # Output path

    # Run the conversion with 1000 synthetic abusive rows
    result_df = convert_text_csv_with_synthetic(text_csv_path, output_csv_path, num_synthetic_rows=1000)

    print("✅ Dataset created with", len(result_df), "rows (including synthetic).")
    print(result_df.head())
