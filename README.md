# auto-translation

Automatic JSON translation tool using local MarianMT models for multiple languages.

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd auto-translation
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download translation models

#### Option A: Automatic download (Recommended)

```bash
./download_models.sh
```

#### Option B: Manual download

Download the required MarianMT models from Hugging Face:

```bash
# Create models directory
mkdir -p models

# Clone each translation model
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-fr models/opus-mt-en-fr
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-de models/opus-mt-en-de
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-es models/opus-mt-en-es
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-it models/opus-mt-en-it
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-nl models/opus-mt-en-nl
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-pl models/opus-mt-en-pl
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-ru models/opus-mt-en-ru
git clone https://huggingface.co/Helsinki-NLP/opus-mt-en-tr models/opus-mt-en-tr
```

**Note:** Each model is approximately 300MB. Total download size: ~2.4GB

## Usage

```bash
python translate_json.py <input_file.json>
```

## Supported Languages

The tool translates from English to:

-   🇫🇷 French (fr)
-   🇩🇪 German (de)
-   🇪🇸 Spanish (es)
-   🇮🇹 Italian (it)
-   🇳🇱 Dutch (nl)
-   🇵🇱 Polish (pl)
-   🇷🇺 Russian (ru)
-   🇹🇷 Turkish (tr)

## Features

-   ✅ Batch translation with progress bar
-   ✅ Preserves JSON structure
-   ✅ Local translation models (no API required)
-   ✅ Error handling and validation
