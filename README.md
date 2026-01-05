# 📊 Streamlit Demo Dashboard

Application de démonstration Streamlit avec dashboard interactif pour Azure Web App.

## 🚀 Fonctionnalités

- **Dashboard Principal** : Métriques clés, graphiques interactifs, données temps réel
- **Analytics Avancées** : Patterns de trafic, heatmaps, métriques de performance
- **Analyse Géographique** : Distribution mondiale, focus Canada, cartes interactives
- **Données Générées** : Simulation de données réalistes pour la démonstration

## 📁 Structure

```
streamlit-demo/
├── app.py                    # Application principale
├── requirements.txt          # Dépendances Python
├── pages/
│   ├── 1_📈_Analytics.py    # Page analytics avancées
│   └── 2_🗺️_Geographic.py   # Page analyse géographique
└── utils/
    └── data_generator.py     # Fonctions de génération de données
```

## 🛠️ Installation et Exécution

### Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Azure Web App
Cette structure est compatible avec la configuration Azure Web App :
- Point d'entrée : `app.py`
- Port : 8000
- Commande : `python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0`

## 📊 Contenu du Dashboard

### Page Principale
- Métriques clés (ventes, utilisateurs, revenus, conversions)
- Graphiques de tendances
- Analyse des revenus avec moyenne mobile
- Barres de progression des objectifs
- Tableau de données filtrable

### Analytics Avancées
- Patterns de trafic par heure/jour
- Heatmap du trafic hebdomadaire
- Métriques de performance (taux de rebond, durée session)
- Données horaires sur 90 jours

### Analyse Géographique
- Carte mondiale avec métriques par pays
- Focus sur le Canada par province
- Scatter plots performance
- Comparaisons régionales

## 🎯 Utilisation

1. **Déployez l'infrastructure Azure** avec le repo `create-azure-webapp-streamlit`
2. **Copiez ce code** dans votre repository applicatif
3. **Configurez le CI/CD** pour déployer vers Azure Web App
4. **Personnalisez** les données et visualisations selon vos besoins

## 🔧 Personnalisation

- Modifiez `utils/data_generator.py` pour vos sources de données
- Ajoutez de nouvelles pages dans le dossier `pages/`
- Customisez les graphiques et métriques dans `app.py`
- Adaptez le style et la configuration dans `st.set_page_config()`

## 📦 Dépendances

- `streamlit>=1.28.0` : Framework web
- `pandas>=2.0.0` : Manipulation de données
- `numpy>=1.24.0` : Calculs numériques
- `plotly>=5.15.0` : Graphiques interactifs

Compatible avec Python 3.11 sur Azure Web App Linux.