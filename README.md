# 🧠 Vulngard

Ce projet repose sur **Ollama** et le modèle **deepseek-coder:6.7b** pour la détection de code vulnérable dans des projets OpenSource en se basant uniquement sur la description des CVE.

---

## 🚀 Installation rapide

### 1. Installer Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Vérifiez l'installation :

```bash
ollama --version
```

---

### 2. Télécharger le modèle `deepseek-coder:6.7b`

```bash
ollama pull deepseek-coder:6.7b
```

---

### 3. Cloner ce dépôt et créer le modèle personnalisé

```bash
git clone git@github.com:nwOLXTYv/VulnGuard.git
cd VulnGuard
```

> Le fichier `Modelfile` est déjà présent dans ce dépôt.

Créez votre modèle :

```bash
ollama create Michel -f ./Modelfile
```

---

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🛠️ Utilisation du script VulnGuard

VulnGuard est un outil d'analyse de vulnérabilités qui utilise les modèles Ollama pour évaluer les vulnérabilités de code. Voici comment l'utiliser :

### Exécution du script

```bash
python3 vulnguard.py
```

### Fonctionnement pas à pas

1. **Sélection du modèle** : Le script liste automatiquement les modèles Ollama disponibles sur votre système.
   - Par défaut, il utilise `Michel` s'il est disponible
   - Vous pouvez sélectionner un autre modèle par son numéro ou son nom

2. **Saisie des informations** :
   - Description de la CVE (Common Vulnerabilities and Exposures)
   - Emplacement du fichier concerné
   - Code diff à analyser (terminé par une ligne contenant uniquement "END")

3. **Analyse de la vulnérabilité** : Le script envoie ces informations au modèle Ollama sélectionné

4. **Affichage des résultats** : L'analyse est présentée sous forme de rapport détaillé

---

## 🧠 Pourquoi `deepseek-coder:6.7b` ?

Nous avons testé plusieurs modèles avec différentes tailles (nombre de nœuds) pour trouver le **meilleur compromis entre qualité et rapidité**.

- `deepseek-coder:6.7b` a montré d'excellents résultats
- Fonctionne bien sur une carte graphique 16 Go (ex: AMD RX 7800XT)

📌 Si vous souhaitez explorer d'autres modèles, visitez :

👉 [https://ollama.com/search](https://ollama.com/search)

Modifiez simplement la ligne `FROM` du `Modelfile`, par exemple :

```Dockerfile
FROM mistral:7b
```

> 💡 Le suffixe `:6.7b`, `:34b`, etc. correspond au **nombre de nœuds**.  
> Plus il est élevé, meilleures sont les performances... mais plus la génération est lente.

---

## 📴 Fonctionnement hors ligne

Une fois le modèle téléchargé, **aucune connexion internet n'est requise**. Le LLM tourne entièrement en **local**, sans cloud.

---

## 🔧 Configuration avancée

### Template de prompt personnalisé

Par défaut, le script utilise un template situé dans `./docs/user-prompt.txt`. Vous pouvez créer votre propre template avec les variables suivantes :
- `{{CVE_DESCRIPTION}}` : Description de la CVE
- `{{File_Location}}` : Emplacement du fichier
- `{{DIFF_HUNK}}` : Code diff à analyser

---

## 📋 Commandes utiles

| Description                      | Commande                                         |
|----------------------------------|--------------------------------------------------|
| Installer Ollama                 | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Télécharger un modèle            | `ollama pull <model_name>`                       |
| Quitter le prompt                | `/bye`                                           |
| Créer un modèle personnalisé     | `ollama create Michel -f ./Modelfile`            |
| Lancer le modèle personnalisé    | `ollama run Michel`                              |
| Voir les modèles installés       | `ollama list`                                    |
| Lancer VulnGuard                 | `python3 vulnguard.py`                           |

---

## 🧑‍💻 Contributeurs

- TAHRI Bahaaeddine
- MOREL Mathilde
- GOSSET Arthur