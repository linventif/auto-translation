#!/usr/bin/env python3
# translate_json.py

import json
import sys
from pathlib import Path
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm

# Map langues → modèles MarianMT locaux (clonnés dans ./models/)
MODEL_MAP = {
    "fr": "models/opus-mt-en-fr",
    "de": "models/opus-mt-en-de",
    "es": "models/opus-mt-en-es",
    "it": "models/opus-mt-en-it",
    "nl": "models/opus-mt-en-nl",
    "pl": "models/opus-mt-en-pl",
    "ru": "models/opus-mt-en-ru",
    "tr": "models/opus-mt-en-tr",
}

def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def unflatten_dict(flat: dict, sep: str = ".") -> dict:
    result = {}
    for compound_key, value in flat.items():
        keys = compound_key.split(sep)
        d = result
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value
    return result

def load_translator(model_path: str):
    """
    Charge le tokenizer et le modèle MarianMT depuis le dossier local.
    """
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    model     = MarianMTModel.from_pretrained(model_path)
    return tokenizer, model

def translate_single_text(text: str, tokenizer, model) -> str:
    """
    Traduit un texte unique
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_length=512, num_beams=1, do_sample=False)
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated

def translate_file(input_path: Path):
    # Lecture du JSON d'entrée
    data = json.loads(input_path.read_text(encoding="utf-8"))
    flat = flatten_dict(data)
    
    print(f"📊 {len(flat)} clés à traduire en {len(MODEL_MAP)} langues")
    print(f"� Traitement ligne par ligne pour plus de stabilité")

    # Traduire pour chaque langue
    with tqdm(total=len(flat) * len(MODEL_MAP), desc="Traduction globale", unit="texte") as pbar:
        for lang, model_dir in MODEL_MAP.items():
            pbar.set_description(f"Traduction en {lang}")
            tokenizer, model = load_translator(model_dir)
            translated_flat = {}

            for key, text in flat.items():
                translated_text = translate_single_text(text, tokenizer, model)
                
                # Vérifications
                if not translated_text:
                    raise ValueError(f"Valeur vide pour la clé {key} dans {lang}")
                
                translated_flat[key] = translated_text
                pbar.update(1)

            # Reconstruire la structure imbriquée et écrire le fichier
            nested = unflatten_dict(translated_flat)
            out_file = input_path.parent / f"{lang}.json"
            out_file.write_text(json.dumps(nested, ensure_ascii=False, indent=2), encoding="utf-8")
            pbar.set_description(f"✅ {lang}.json sauvegardé")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python translate_json.py <path/to/en.json>")
        sys.exit(1)
    translate_file(Path(sys.argv[1]))
