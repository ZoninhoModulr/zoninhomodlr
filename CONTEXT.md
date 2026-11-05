# BIBLE DU PROJET — AGENCE DE COMMUNICATION VIRTUELLE & STUDIO JSX (SaaS)

## 1. Vision & Concept Général
- **Concept :** Une plateforme SaaS (logiciel par abonnement mensuel via Stripe) qui agit comme une véritable agence de communication virtuelle où chaque pôle (Directeur Stratégique, Rédacteur, Community Manager, Ingénieur Scripts Adobe) est incarné par un agent IA spécialisé.
- **Équipe fondatrice :** 
  - **Simon :** Product Owner, Direction Artistique, Graphisme, Architecture IA & Vibe Coding.
  - **Camil :** Associé Business, Testeur produit, Stratégie commerciale & Opérations.
- **Stratégie de lancement juridique :** Démarrage agile en micro-entreprise (zéro frais fixes) pour tester le marché local et encaisser les premiers abonnements via Stripe, avant bascule vers une société (SARL/SAS) avec Camil lorsque le chiffre d'affaires décolle.

## 2. Double Positionnement & Modèle d'Abonnement
Le logiciel cible deux profils complémentaires avec deux paliers tarifaires :

### A. Offre "Pilote" (Cible : PME, Artisans, Dirigeants novices — env. 29€ à 39€/mois)
- **Usage :** Pilotage ultra-simple de la communication sans jargon.
- **Doctrine Visuelle "Zéro Fake IA" :** Interdiction des images générées par IA génériques et lisses (type "nanobanana") qui détruisent la Direction Artistique.
  1. Valorisation des **vraies photos de terrain** (prises au smartphone) sublimées par des légendes stratégiques.
  2. Pour les promotions ou annonces sans photo : intégration future d'un générateur de **Smart Templates** (gabarits typographiques épurés et cartes d'annonces pré-dessinées où l'IA injecte uniquement le texte et les couleurs de la marque).

### B. Offre "Studio Pro" (Cible : Graphistes, Motion Designers, Agences — env. 49€ à 59€/mois)
- **Usage :** Inclut toute l'offre Pilote + l'atelier d'ingénierie créative Adobe.
- **Valeur ajoutée :** Génération de scripts mathématiques ExtendScript (`.jsx`) pour automatiser les tâches complexes ou répétitives dans Adobe Illustrator, After Effects (et plus tard InDesign), accompagnée d'un Mentor technique Adobe.

## 3. Identité de Marque, Direction Artistique & Ergonomie Visuelle
- **Neutralité & Zéro donnée résiduelle de test :** Le SaaS est désormais intégralement personnalisable. Toutes les anciennes données de test (cas Bogotá, références résiduelles à un chef cuisinier) ont été définitivement purgées du code source, de la persistance et des prompts IA au profit d'un ancrage dynamique strict aux données configurées par l'utilisateur.
- **Identité cible du SaaS :**
  - **Nom & Logo :** Piste autour de *Modulaire* / *Modulr*, avec un logo monogramme typographique fort et minimaliste (une lettre iconique comme un "M", dans l'esprit d'Adobe ou Notion).
  - **Baseline :** L'idée d'une *"agence de communication complète au creux de la main"*.
  - **Charte Graphique Dark Mode & Douceur Visuelle :** Bannir les dégradés bleu/violet clichés des outils IA. Adopter un **Dark Mode chaleureux et profond** relevé par le vert sauge `#85a363` (ou orange électrique `#f59e0b`).
  - **Doctrine Visuelle "Fluide & Adoucie pour Novices" :**
    - **Fin des blocs cubiques et rigides :** Arrondis généreux et harmonieux (`border-radius` de 14px à 18px sur toutes les cartes, panneaux, volets et conteneurs).
    - **Formes Soft-Pill / Pilule Douce :** Badges d'étapes (`.step-badge`), boutons d'action (`border-radius: 24px`) et indicateurs d'état pour un toucher visuel agréable et accueillant.
    - **Micro-interactions & Hover dynamique :** Réaction délicate de tous les éléments interactifs au survol (légère élévation `translateY(-2px)`, halo lumineux doux `#85a363` et transition cubique fluide) éliminant l'impression d'interface figée.
    - **Allègement du poids visuel :** Interlignage aéré (1.6), bordures allégées en opacité translucide (`rgba(255,255,255,0.09)`), et dégradés de fond discrets pour ne jamais submerger les dirigeants novices sous des murs de texte.
  - **Doctrine Iconographique : Remplacement progressif des Emojis par des Icônes Vectorielles SVG Minimalistes :**
    - **Décision de Design :** Abandon progressif des emojis standards d'OS (hétérogènes et connotés "bricolage") au profit d'une bibliothèque vectorielle SVG sur-mesure, fine et unifiée (`stroke-width: 1.8px`, viewBox 24x24, géométrie épurée).
    - **Direction Artistique & Palette :** Icônes monochromes adaptées au Dark Mode avec accentuation dynamique en vert sauge signature (`#85a363`).
    - **Intégration Fluide :** Composant et helpers dédiés (`get_svg_icon`, `render_icon_label`) injectables directement dans les en-têtes de pages, cartes du parcours guidé, badges et boutons d'action avec micro-animations au survol (`scale(1.12)`).
    - **Bénéfice :** Niveau de finition haut de gamme immédiat (façon Linear, Notion ou suite Adobe) tout en renforçant la clarté pour les novices.

## 4. Architecture & Ergonomie Actuelles (`app.py` & `agents.py`)
- **Gestion de la Barre Latérale (Sidebar) Fermée par Défaut :**
  - Au lancement de l'application, la barre latérale est configurée pour être repliée par défaut (`initial_sidebar_state="collapsed"` dans `st.set_page_config`).
  - L'écran s'ouvre directement en pleine largeur, garantissant un environnement épuré, calme et non saturé pour le dirigeant.
  - La sidebar reste accessible via l'icône discrète en haut à gauche et contient exclusivement l'identité de profil et le sélecteur de modèle LLM.

- **Refonte Totale du Header (Navigation Rectangulaire SaaS & Pastille Profil) :**
  - **Logo Cliquable vers l'Accueil (Haut Gauche) :**
    - Le bouton "Accueil" textuel disparaît du menu central pour alléger la barre de navigation.
    - Il est remplacé par le logo officiel de l'entreprise (ou un monogramme élégant `✨` si aucun logo n'est téléversé) placé tout en haut à gauche, qui sert de lien direct et cliquable vers l'Accueil.
    - Le nom de l'entreprise et ses 4 attributs clés (Secteur · Ville · Portée · Marché) sont présentés immédiatement à côté du logo.
  - **Pastille Ronde / Capsule Profil Utilisateur (Haut Droite) :**
    - Remplacement du pavé de profil par une capsule arrondie moderne et discrète (`👤 {Prénom} {Nom} · {Rôle}`, ex : *Simon Zoni · Dirigeant*), cliquable pour ouvrir instantanément l'espace "Mon Compte & Entreprise".
  - **Barre de Navigation Rectangulaire Unifiée (Style SaaS Pro) :**
    - Remplacement des boutons séparés par un bloc rectangulaire unifié et discret (`.saas-nav-container`) qui s'étend harmonieusement sur la largeur du header.
    - Les 6 sections (`🎯 Stratégie`, `💡 Marketing`, `📅 Planning`, `⚙️ Création`, `📸 Studio`, `🏢 Mon Compte`) s'affichent à l'intérieur du conteneur sans bordures séparatrices rigides, avec un effet de survol (hover) subtil et élégant.
    - L'onglet actif se distingue par un fond doux translucide et un liseré vert sauge signature (`#85a363`).

- **Nettoyage de la Fiche Entreprise (Filtres & Valeurs Vides) :**
  - Helper centralisé `format_vault_field(key, val)` : si un champ du profil d'entreprise (secteur, ville, portée, typologie de marché, description ADN, ton) n'a pas été renseigné par l'utilisateur ou correspond à une ancienne valeur de test, l'application affiche proprement la mention en italique discret *"Non renseigné"*.
  - Fini les textes résiduels incohérents ou les zones blanches déstructurantes.

- **Valorisation & Refonte de l'Atelier "Création & Scripts Adobe (ExtendScript JSX)" :**
  - La page est structurée comme un véritable atelier d'ingénierie créative et d'automatisation graphique pour les studios et graphistes.
  - **Extension aux 5 Grands Logiciels de la Suite Adobe (`st.selectbox`) :**
    - `🎨 Adobe Illustrator (.jsx) — Tracés vectoriels, courbes de Bézier, nuanciers & calques`
    - `🎬 Adobe After Effects (.jsx) — Motion design procédural, animations de calques & keyframes`
    - `📄 Adobe InDesign (.jsx) — Grilles modulaires, gabarits, styles typographiques & pagination`
    - `🖼️ Adobe Photoshop (.jsx) — Compositions automatisées, calques de réglage & formats web`
    - `🎞️ Adobe Premiere Pro (.jsx) — Montage dynamique, marqueurs, organisation chutier & exports`
  - **Interaction Dynamique entre Presets et Chat (Itération Continue) :**
    - Les modèles de scripts ne sont plus des blocs de code figés et aveugles. Dès qu'un preset est cliqué, il s'exécute, prévisualise le code et s'injecte comme **Script de Base Actif** (`jsx_active_base_script`) dans le chat d'assistance.
    - L'utilisateur peut immédiatement personnaliser ce script sur-mesure (ex: dimensions à 1200x800, traits d'une épaisseur de 10px, teintes rouge vif, ajout de calques) via des puces de modification rapide ou en saisie libre.
    - Le moteur [`agent_ingenieur_adobe_jsx`](agents.py) reçoit le `base_code` pour adapter fidèlement l'existant sans casser la syntaxe ES3.
  - **Gestion Dynamique des Presets Utilisateur (Boîte à Outils Persistante) :**
    - L'interface propose deux sous-onglets : *Presets Standards* (catalogue officiel) et *Mes Presets Personnalisés* (`state["custom_jsx_presets"]`).
    - L'utilisateur peut enregistrer en un clic n'importe quel script généré et affiné dans ses presets (via le bouton popover *⭐ Sauvegarder en Preset* dans le chat), créer des presets manuellement ou supprimer les presets obsolètes via un bouton `🗑️`.
  - **Tiroir Latéral Persistant & Bouton Flottant (Mentor Adobe Déporté) :**
    - Fin de l'ouverture du chatbot au milieu du flux de lecture vertical : le mentor s'ouvre dans un véritable **panneau latéral secondaire** (`col_drawer`, `.adobe-persistent-drawer`) à droite de l'écran, laissant l'atelier de création 100% stable et fluide à gauche.
    - Accessible à tout moment, qu'on soit tout en haut ou tout en bas de page, via le bouton d'en-tête et un **bouton flottant persistant** (`.floating-mentor-trigger`) fixé en bas à droite de l'écran.
  - **Suppression du Jargon Technique & Mise en Avant de la Puissance Graphique :**
    - Remplacement des explications de code pour développeurs (ES3, IIFE, variables) par 4 cartes d'inspiration visuelle démontrant pourquoi le vectoriel procédural surpasse les images matricielles (raster) de Midjourney ou Firefly :
      1. *Courbes de Bézier Pures* : précision mathématique infinie à toute échelle, aucun pixel flou, parfait pour l'impression ou l'enseigne.
      2. *Calques Nommés & Modifiables* : structures de calques natives éditables à 100% par les graphistes.
      3. *Respect Strict de Charte* : injection rigoureuse des codes HEX officiels de la marque sans dérive colorimétrique.
      4. *3h de Dessin en 3s* : création instantanée de grilles modulaires, gabarits et déclinaisons de formats.

- **Allègement des Titres & Épurage Visuel (Fin des préfixes "Étape X") :**
  - Suppression radicale des lourdeurs du type *"Étape 1..."*, *"Étape 2..."* dans tous les en-têtes de pages, badges, onglets et cartes de parcours.
  - Titres sobres, courts, élégants et orientés design (`Stratégie & Boussole de Marque`, `Marketing & Offres Commerciales`, `Planning Éditorial`, `Création & Scripts Adobe`, `Studio & Social Ads`).

- **Formulaires Épurés & Guidage par Placeholders :**
  - Suppression des longs textes de démonstration pré-remplis qu'il fallait effacer manuellement à l'onboarding.
  - Utilisation systématique de `placeholder="..."` en gris clair pour guider le dirigeant avec des exemples inspirants sans polluer la saisie.

- **Rendu HTML Sécurisé & Infaillible (`render_html`) :**
  - Résolution définitive du bug d'affichage HTML brut (où des balises `<div style="...">` s'affichaient textuellement suite à l'interprétation CommonMark des indentations supérieures à 4 espaces).
  - Centralisation de l'affichage HTML dans le helper `render_html(html_str)` qui nettoie l'indentation parasite et exécute `st.markdown(..., unsafe_allow_html=True)`.

- **Généralisation des Sous-Menus Visuels :** Système d'onglets animés (`st.tabs`) standardisé avec barre indicatrice fluide `#85a363`, garantissant une navigation haut de gamme dans toutes les sections à sous-catégories.
- **Accueil Asymétrique :** Colonne "Boussole de Marque" fixe à gauche (avec mentions "Non renseigné" si profil incomplet) + parcours progressif en 5 cartes distinctes à droite.

- **Stratégie & Boussole de Marque (`render_strategic_identity_card`) :**
  - **Approche pédagogique :** Explication claire des 3 buts d'une stratégie de communication pour un dirigeant novice.
  - **Mini-tunnel de cadrage en 3 colonnes :**
    1. *Secteur & Positionnement* (métier, axe de différenciation, preuve).
    2. *Cibles prioritaires* (multiselect sur segments qualifiés + zone géographique).
    3. *Objectif commercial du moment* (acquisition, fidélisation CRM, lancement d'offre, autorité).
  - **Restitution visuelle :** Restitution sous forme de *Fiche d'Identité Stratégique* (Fondations, Objectifs Cognitif / Affectif / Conatif, Leviers psychologiques, Tunnel de conversion) avec des accents sobres.

- **Pôle Marketing 360° (3 sous-onglets distincts) :**
  - **Sous-onglet 1 : Stratégie de Marché & Offre Commerciale :**
    - Consultant stratégique senior (`agent_strategie_marche_offre`) ancré dans la ville et le secteur du commerce configuré.
    - Diagnostic de positionnement, benchmarks locaux et justifications de la grille tarifaire (prix premium / marge).
    - Conception d'offres packagées ("Offre Irrésistible" avec promesse forte, livrables et prix psychologique) avec ajout direct au catalogue, au planning ou test au Studio en un clic.
  - **Sous-onglet 2 : Campagnes d'E-mailing (CRM & Fidélisation) :**
    - Gestion des contacts clients (import de fichiers `.csv` / `.txt` ou copier-coller avec extraction regex et dédoublonnage automatique).
    - Générateur d'e-mails commerciaux percutants (`agent_campagne_mailing`) avec 3 propositions d'objets, corps de texte fluide et **analyse psychologique de conversion** expliquant le levier d'action.
    - Configuration d'envoi externe (Brevo API ou mode simulation validée), téléchargement en `.txt` et validation en un clic.
  - **Sous-onglet 3 : R&D & Idées Produits :**
    - Veille sectorielle automatisée par l'IA (`agent_veille_proactive_rd`) orientable par thématique.
    - **Boîte à Idées Proactive :** 3 propositions concrètes et actualisées en permanence avec deux actions immédiates : *🔬 Approfondir l'étude* ou *📸 Ouvrir directement au Studio*.
    - Banc d'essai R&D sur mesure avec possibilité d'ajouter le produit validé aux offres officielles et de programmer son lancement au calendrier.

- **Planning Visuel Mensuel & Automatisation Meta :**
  - Vrai calendrier mensuel visuel (grille interactive mois par mois) avec sélection de dates précises.
  - Codes couleurs par statut : **Gris** (Brouillon), **Orange** (À valider), **Vert** (Prêt / Auto-post).
  - Boutons d'action parfaitement alignés verticalement.
  - Panneau de configuration **Meta Graph API (Instagram & Facebook)** activable avec deux modes : *Publication 100% automatique* ou *Validation manuelle en un clic avant envoi*.

- **Création Graphique & Scripts Adobe :**
  - **Prise en charge intégrale des 5 Majeurs Adobe :** Illustrator, After Effects, InDesign, Photoshop, Premiere Pro.
  - **Scripts 1-Clic Connectés au Chat :** Catalogue de 20 templates exécutables immédiatement et injectés comme script de base actif pour personnalisation itérative en langage naturel (dimensions, épaisseurs, couleurs).
  - **Gestion Dynamique des Presets :** Boîte à outils personnalisée permettant d'enregistrer tout script affiné dans ses presets (`state["custom_jsx_presets"]`), d'en ajouter manuellement et de les supprimer en un clic (`🗑️`).
  - **Panneau Latéral / Tiroir Persistant du Mentor Adobe :** Déporté sur la droite (`col_drawer`, `.adobe-persistent-drawer`), accessible à tout moment via l'en-tête et un bouton flottant persistant (`.floating-mentor-trigger`) en bas à droite sans perturber le flux central.
  - **Valorisation Artistique & Technique :** Remplacement du jargon développeur par la démonstration de la supériorité des courbes vectorielles pures et des calques natifs face aux artefacts matriciels de l'IA.
  - **Téléchargement direct `.jsx` :** Extraction automatique du code et bouton `st.download_button`.
  - **Doctrine ExtendScript ES3 Robuste :** Respect strict des normes Adobe (IIFE, calques nommés, gestion d'erreurs, `beginUndoGroup` / `endUndoGroup`, RGBColor).

- **Studio de Création & Social Ads (2 sous-onglets distincts) :**
  - **Sous-onglet 1 : Publications Organiques (Meta) :**
    - Valorisation des vraies photos de terrain avec analyse sémiologique et rédaction de légendes captivantes.
    - Choix précis de la cible : *Instagram & Facebook (Cross-posting simultané)*, *Instagram seul* ou *Facebook seul*.
    - Enregistrement direct dans le calendrier mensuel avec statut « À valider ».
  - **Sous-onglet 2 : Social Ads & Budgets :**
    - **Dashboard de pilotage publicitaire :** Métriques clés (Dépenses engagées vs Plafond, Portée & Impressions, CPC moyen & CTR, ROAS et Prospects générés).
    - **Suivi graphique hebdomadaire :** Évolution des investissements et des clics sans dépendance externe lourde.
    - **Pilotage budgétaire & Enchères par l'IA :** Réglage du budget mensuel et de l'objectif d'optimisation (Prospects WhatsApp/DM, ROAS banquets, Notoriété locale).
    - **Gestionnaire de campagnes & IA Copywriter Ads (`agent_meta_ads_copywriter`) :** Génération de copies publicitaires (variantes Primary Text, Titres d'accroche percutants, recommandations de ciblage et d'enchères) et déploiement en direct.
    - **Architecture Modulaire Meta Marketing API (`MetaMarketingAPIConnector`) :** Prête pour la production avec gestion transparente du mode Sandbox et bascule immédiate vers Meta Graph API v19.0 (`https://graph.facebook.com/v19.0/`) lors de l'insertion des clés réelles (`access_token`, `ad_account_id`, `pixel_id`).

- **Espace Dédié : « 🏢 Mon Compte & Entreprise » :**
  - **Division claire en deux parties structurées :**
    - **Partie A — Profil Utilisateur :** Prénom (`user_first_name`), Nom (`user_last_name`), Rôle dans l'entreprise (`user_role`, ex : Dirigeant, Fondateur).
    - **Partie B — Profil Entreprise & Stratégie :**
      - Nom de l'entreprise (`brand_name`), Secteur d'activité principal (`business_type`), Ville ou implantation principale (`location`, ex : Vesoul).
      - **Portée géographique de la cible (Dropdown) :** *Local / De proximité*, *National*, *International*.
      - **Typologie de marché (Dropdown) :** *B2C / Grand public*, *B2B / Professionnels*, *Mixte (B2C & B2B)*.
      - Typologie de clientèle cible détaillée (`client_type`) et Description courte / ADN de la marque (`short_dna`).
      - Synchronisation Fiche & Avis clients Google Maps (`agent_analyse_profil_google_maps`).
    - **Partie C — Logo Officiel de l'Entreprise :** Téléversement du logo d'entreprise (PNG, JPG, JPEG, SVG) avec mise à jour globale et immédiate sur tout le site (notamment l'avatar en haut à gauche via `user_profile_avatar.png`), et option de réinitialisation.
    - **Partie D — Charte Graphique & Ligne Éditoriale :** Palette de couleurs (Principale, Secondaire, Accent), Ton de communication principal, Directives stylistiques et Repères typographiques.
  - **Ancrage dynamique temps réel dans tous les agents IA (`format_brand_vault_context`) :**
    - Les agents IA (Stratégie Red Team, Marché & Offre, Campagne Mailing, Veille R&D, Plan de communication, Studio de création, Meta Ads) récupèrent 100% de ces variables en temps réel.
    - Toute suggestion ou rédaction est obligatoirement calibrée sur la ville réelle, la portée géographique, le type de marché (B2B ou B2C) et l'ADN de la marque.
  - **Aperçu Visuel Temps Réel (Carte d'Identité IA) :** Colonne de droite présentant la carte d'identité dynamique de l'entreprise avec son logo, ses badges de portée/marché, ses swatchs couleurs et son ton de communication.

## 5. Feuille de Route & Fonctionnalités Futures à Développer
1. **Scripts JSX contextuels sur fichiers ouverts :** Permettre aux scripts générés d'agir sur la sélection active (`app.activeDocument.selection`) d'un fichier Illustrator déjà ouvert par le graphiste.
2. **Bibliothèque de "Smart Snippets" JSX :** Catalogue de scripts pré-optimisés (grilles isométriques, palettes, exports multi-calques) paramétrables en un clic par l'IA.
3. **Extension Native Adobe (Panel CEP / UXP) :** Transformer l'atelier Création en véritable panneau flottant dans Illustrator et After Effects.
4. **Dictée Vocale / Journal du Dirigeant :** Module permettant au gérant de parler naturellement au micro pour briefer l'agence sans écrire.
5. **Générateur de Smart Templates (Offre Novice) :** Créateur de visuels d'annonces/promos propres basé sur des gabarits HTML/Canvas ou SVG maîtrisés graphiquement.
6. **Transition intégrale vers le Design System SVG Vectoriel :** Remplacement systématique de tous les emojis restants par la bibliothèque d'icônes vectorielles SVG sur-mesure pour parachever l'élégance sobre de l'application.
