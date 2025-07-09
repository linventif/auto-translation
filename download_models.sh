#!/bin/bash

# Script pour télécharger tous les modèles MarianMT
echo "📥 Téléchargement des modèles de traduction MarianMT..."

# Créer le dossier models s'il n'existe pas
mkdir -p models

# Liste des modèles à télécharger
models=(
    "opus-mt-en-fr"
    "opus-mt-en-de"
    "opus-mt-en-es"
    "opus-mt-en-it"
    "opus-mt-en-nl"
    "opus-mt-en-pl"
    "opus-mt-en-ru"
    "opus-mt-en-tr"
)

total=${#models[@]}
current=0

for model in "${models[@]}"; do
    current=$((current + 1))
    echo "📦 [$current/$total] Téléchargement de $model..."
    
    if [ -d "models/$model" ]; then
        echo "⚠️  Le modèle $model existe déjà, mise à jour..."
        cd "models/$model" && git pull && cd ../..
    else
        git clone "https://huggingface.co/Helsinki-NLP/$model"
    fi
    
    if [ $? -eq 0 ]; then
        echo "✅ $model téléchargé avec succès"
    else
        echo "❌ Erreur lors du téléchargement de $model"
        exit 1
    fi
done

echo ""
echo "🎉 Tous les modèles ont été téléchargés avec succès!"
echo "📊 Taille totale: ~2.4GB"
echo "🚀 Vous pouvez maintenant utiliser: python translate_json.py <fichier.json>"
