# 🧠 Vulnerability Detector – LLM Powered by Ollama & DeepSeek

Ce projet repose sur **Ollama** et le modèle **deepseek-coder:6.7b** pour la détection de code vulnérable dans des projets OpenSource en se basant uniquement sur la description des CVE.

---

## 🚀 Installation rapide

### 1. Installer Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Vérifiez l’installation :

```bash
ollama --version
```

---

### 2. Télécharger le modèle `deepseek-coder:6.7b`

```bash
ollama run deepseek-coder:6.7b
```

> 📥 Cela déclenchera le téléchargement du modèle. Une fois terminé, vous serez dans le prompt interactif.

Quittez le prompt avec :

```bash
/bye
```

---

### 3. Cloner ce dépôt et créer le modèle personnalisé

```bash
git clone https://votre-repo-git-url.git
cd votre-repo-git-folder
```

> Le fichier `Modelfile` est déjà présent dans ce dépôt.

Créez votre modèle :

```bash
ollama create vulnerability_detector -f ./Modelfile
```

---

### 4. Utiliser le modèle personnalisé

```bash
ollama run vulnerability_detector
```

> ❌ Quittez la session avec `/bye`

---

## 🔍 À propos du `Modelfile`

Le `Modelfile` définit comment le modèle est construit. Il permet :

- De partir d’un modèle existant (`FROM`)
- D'ajouter un comportement spécifique (`SYSTEM`)

Exemple :

```Dockerfile
FROM deepseek-coder:6.7b
SYSTEM "You are a vulnerability detection assistant. Analyze code for security issues."
```

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

Une fois le modèle téléchargé, **aucune connexion internet n’est requise**. Le LLM tourne entièrement en **local**, sans cloud.

---

## 📋 Commandes utiles

| Description                      | Commande                                        |
|----------------------------------|-------------------------------------------------|
| Installer Ollama                 | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Télécharger un modèle            | `ollama run deepseek-coder:6.7b`               |
| Quitter le prompt                | `/bye`                                          |
| Créer un modèle personnalisé     | `ollama create vulnerability_detector -f ./Modelfile` |
| Lancer le modèle personnalisé    | `ollama run vulnerability_detector`            |
| Voir les modèles installés       | `ollama list`                                   |

---

## 🧑‍💻 Contributeurs

- TAHRI Bahaaeddine
- MOREL Mathilde
- GOSSET Arthur
