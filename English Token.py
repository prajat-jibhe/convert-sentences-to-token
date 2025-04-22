import pandas as pd

# Step 1: Load the list of abusive words from a CSV
def load_abusive_words(profanity_csv_path):
    """
    Load abusive words from a CSV file with a column named 'Profanity'.
    Returns a set of lowercased abusive words for quick lookup.
    """
    profanity_df = pd.read_csv(profanity_csv_path)
    # Make sure to drop NaNs and strip whitespace
    return set(profanity_df['Profanity'].dropna().str.lower().str.strip())

# Step 2: Tokenize text and assign labels to each token
def process_text(text, label, abusive_words):
    """
    Tokenizes the input text and labels each word.
    If the sentence is labeled abusive (label == 1), we label each word as:
        1 → if the word is in the abusive words list
        0 → otherwise
    If the sentence is not abusive, all tokens are labeled 0.
    Handles missing or non-string text safely.
    """
    # Convert text to string safely
    if not isinstance(text, str):
        text = ""
    
    # Basic whitespace tokenizer
    words = text.split()

    # Label tokens
    if label == 1:
        word_labels = [
            1 if word.lower().strip(".,!?\"'") in abusive_words else 0
            for word in words
        ]
    else:
        word_labels = [0] * len(words)

    return words, word_labels

# Step 3: Main function to convert the full CSV
def convert_text_csv(text_csv_path, profanity_csv_path, output_csv_path=None):
    """
    Main function to load data, process each row, and output the result.
    Parameters:
        text_csv_path: Path to CSV file with 'text' and 'label' columns
        profanity_csv_path: Path to CSV file with 'Profanity' column
        output_csv_path: Optional path to save output CSV
    Returns:
        A pandas DataFrame with columns 'tokens' and 'token_labels'
    """
    # Load abusive words
    abusive_words = load_abusive_words(profanity_csv_path)
    
    # Load main text CSV
    text_df = pd.read_csv(text_csv_path)

    # Optional: Drop rows where 'text' or 'label' is missing
    text_df = text_df.dropna(subset=['text', 'label'])

    all_tokens = []
    all_token_labels = []

    # Process each row
    for _, row in text_df.iterrows():
        tokens, token_labels = process_text(row['text'], row['label'], abusive_words)
        all_tokens.append(tokens)
        all_token_labels.append(token_labels)

    # Build result DataFrame
    result_df = pd.DataFrame({
        'tokens': all_tokens,
        'token_labels': all_token_labels
    })

    # Save result to CSV if specified
    if output_csv_path:
        result_df.to_csv(output_csv_path, index=False)

    return result_df

# -----------------------------
# 👇 Example usage of the script
# -----------------------------
if __name__ == "__main__":
    # Replace these paths with your actual file locations
    text_csv_path = "C:/Users/Prajat/Downloads/New folder/English.csv"
    profanity_csv_path = "C:/Users/Prajat/Downloads/New folder/profanity_en.csv"
    output_csv_path = "C:/Users/Prajat/Downloads/New folder/tokenized_output.csv"

    # Run the conversion
    result_df = convert_text_csv(text_csv_path, profanity_csv_path, output_csv_path)

    # Print first few rows to check
    print(result_df.head())
