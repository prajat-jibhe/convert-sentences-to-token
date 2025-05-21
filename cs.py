#English
import pandas as pd
import requests
import random
import ast
from collections import Counter
import time

def fetch_profane_words():
    url = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en"
    response = requests.get(url)
    words = response.text.splitlines() if response.status_code == 200 else []
    return set(w.strip() for w in words if w.strip())

def fetch_urban_double_meanings(n=100):
    """
    Fetches n random Urban Dictionary entries and returns words/phrases likely to have double meanings.
    """
    double_meanings = set()
    for _ in range(n):
        try:
            resp = requests.get("https://api.urbandictionary.com/v0/random", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for entry in data.get("list", []):
                    word = entry.get("word", "").strip()
                    definition = entry.get("definition", "").lower()
                    # Heuristic: look for 'double meaning', 'innuendo', 'slang', 'can also mean', 'sexual', etc.
                    if any(
                        kw in definition
                        for kw in [
                            "double meaning", "innuendo", "slang", "can also mean", "sexual", "ambiguous", "euphemism"
                        ]
                    ):
                        double_meanings.add(word)
            time.sleep(0.3)  # Avoid rate limiting
        except Exception as e:
            continue
    return double_meanings

def fetch_synonyms(word):
    url = f"https://api.datamuse.com/words?rel_syn={word}"
    response = requests.get(url)
    if response.status_code == 200:
        return [item['word'] for item in response.json()]
    return []

def flatten_tokens(tokens_col):
    all_tokens = []
    for tokens in tokens_col:
        if isinstance(tokens, str):
            tokens = ast.literal_eval(tokens)
        all_tokens.extend(tokens)
    return all_tokens

def flatten_labels(labels_col):
    all_labels = []
    for labels in labels_col:
        if isinstance(labels, str):
            labels = ast.literal_eval(labels)
        all_labels.extend(labels)
    return all_labels

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    tokens = flatten_tokens(df['tokens'])
    labels = flatten_labels(df['token_labels'])

    label_counts = Counter(labels)
    profane_count = label_counts[1]
    non_profane_count = label_counts[0]
    print(f"Label 0: {non_profane_count}, Label 1: {profane_count}")

    profane_words = fetch_profane_words()
    print("Fetching double-meaning words from Urban Dictionary (may take a minute)...")
    double_meaning_words = fetch_urban_double_meanings(100)
    print(f"Found {len(double_meaning_words)} double-meaning words.")

    all_profane_candidates = profane_words | double_meaning_words

    print("Fetching synonyms for profane words (this may take a minute)...")
    for word in random.sample(list(profane_words), min(30, len(profane_words))):
        all_profane_candidates.update(fetch_synonyms(word))

    existing_profane = set([t for t, l in zip(tokens, labels) if l == 1])
    new_profane_candidates = list(all_profane_candidates - existing_profane)
    random.shuffle(new_profane_candidates)

    needed = non_profane_count - profane_count
    if needed <= 0:
        print("Dataset already balanced.")
        return

    new_profane_words = []
    for word in new_profane_candidates:
        if len(new_profane_words) < needed:
            new_profane_words.append(word)
        else:
            break

    while len(new_profane_words) < needed:
        for word in new_profane_candidates:
            if len(new_profane_words) < needed:
                new_profane_words.append(word)
            else:
                break
        random.shuffle(new_profane_words)

    new_rows = [{'tokens': str([word]), 'token_labels': str([1])} for word in new_profane_words[:needed]]

    df_new = pd.DataFrame(new_rows)
    df_balanced = pd.concat([df, df_new], ignore_index=True)
    df_balanced = df_balanced.sample(frac=1).reset_index(drop=True)

    df_balanced.to_csv(output_csv, index=False)
    all_labels = flatten_labels(df_balanced['token_labels'])
    print("New label counts:", Counter(all_labels))
    print(f"Balanced dataset saved to {output_csv}")

if __name__ == "__main__":
    main("C:/Users//Downloads/New folder/tokenized_output english.csv", "balanced_output_dataset.csv")



#Spanish
import pandas as pd
import requests
import random
import ast
from collections import Counter
import time

def fetch_profane_words():
    # Spanish LDNOOBW list
    url = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/es"
    response = requests.get(url)
    words = response.text.splitlines() if response.status_code == 200 else []
    return set(w.strip() for w in words if w.strip())

def fetch_urban_double_meanings(n=100):
    """
    Fetches n random Urban Dictionary entries and returns Spanish words/phrases likely to have double meanings.
    """
    double_meanings = set()
    for _ in range(n):
        try:
            resp = requests.get("https://api.urbandictionary.com/v0/random", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                for entry in data.get("list", []):
                    word = entry.get("word", "").strip()
                    definition = entry.get("definition", "").lower()
                    # Heuristic: Look for Spanish words and double meaning cues
                    # Simple check: word contains only Spanish letters and definition has Spanish keywords
                    if any(c in word for c in "áéíóúñ") or any(kw in definition for kw in ["significa", "puede ser", "doble sentido", "sexual", "ambigua", "eufemismo"]):
                        double_meanings.add(word)
            time.sleep(0.3)
        except Exception as e:
            continue
    return double_meanings

def fetch_synonyms(word):
    # Datamuse Spanish synonyms
    url = f"https://api.datamuse.com/words?rel_syn={word}&v=es"
    response = requests.get(url)
    if response.status_code == 200:
        return [item['word'] for item in response.json()]
    return []

def flatten_tokens(tokens_col):
    all_tokens = []
    for tokens in tokens_col:
        if isinstance(tokens, str):
            tokens = ast.literal_eval(tokens)
        all_tokens.extend(tokens)
    return all_tokens

def flatten_labels(labels_col):
    all_labels = []
    for labels in labels_col:
        if isinstance(labels, str):
            labels = ast.literal_eval(labels)
        all_labels.extend(labels)
    return all_labels

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    tokens = flatten_tokens(df['tokens'])
    labels = flatten_labels(df['token_labels'])

    label_counts = Counter(labels)
    profane_count = label_counts[1]
    non_profane_count = label_counts[0]
    print(f"Label 0: {non_profane_count}, Label 1: {profane_count}")

    profane_words = fetch_profane_words()
    print("Obteniendo palabras de doble sentido de Urban Dictionary (esto puede tardar un poco)...")
    double_meaning_words = fetch_urban_double_meanings(100)
    print(f"Encontradas {len(double_meaning_words)} palabras de doble sentido.")

    all_profane_candidates = profane_words | double_meaning_words

    print("Obteniendo sinónimos de palabras malsonantes (esto puede tardar un poco)...")
    for word in random.sample(list(profane_words), min(30, len(profane_words))):
        all_profane_candidates.update(fetch_synonyms(word))

    existing_profane = set([t for t, l in zip(tokens, labels) if l == 1])
    new_profane_candidates = list(all_profane_candidates - existing_profane)
    random.shuffle(new_profane_candidates)

    needed = non_profane_count - profane_count
    if needed <= 0:
        print("El dataset ya está balanceado.")
        return

    new_profane_words = []
    for word in new_profane_candidates:
        if len(new_profane_words) < needed:
            new_profane_words.append(word)
        else:
            break

    while len(new_profane_words) < needed:
        for word in new_profane_candidates:
            if len(new_profane_words) < needed:
                new_profane_words.append(word)
            else:
                break
        random.shuffle(new_profane_words)

    new_rows = [{'tokens': str([word]), 'token_labels': str([1])} for word in new_profane_words[:needed]]

    df_new = pd.DataFrame(new_rows)
    df_balanced = pd.concat([df, df_new], ignore_index=True)
    df_balanced = df_balanced.sample(frac=1).reset_index(drop=True)

    df_balanced.to_csv(output_csv, index=False)
    all_labels = flatten_labels(df_balanced['token_labels'])
    print("Nuevos conteos de etiquetas:", Counter(all_labels))
    print(f"Dataset balanceado guardado en {output_csv}")

if __name__ == "__main__":
    main("C:/Users/Prajat/Downloads/New folder/tokenized_output spanish.csv", "balanced_output_dataset_sp.csv")

