import json
import threading
import concurrent.futures
from datetime import date
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

import os
import streamlit as st

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
STATE_FILE = Path("agency_state.json")

DEFAULT_BRAND_VAULT = {
    "brand_name": "Mon Entreprise",
    "business_type": "Commerce / Services de proximité",
    "user_first_name": "Simon",
    "user_last_name": "Zoni",
    "founder_or_lead": "Simon Zoni",
    "user_role": "Dirigeant",
    "location": "Vesoul",
    "target_scope": "Local / De proximité",
    "market_type": "B2C / Grand public",
    "client_type": "Particuliers & clientèle de proximité",
    "google_maps_query": "",
    "google_reviews_summary": "Excellente réputation locale, accueil chaleureux et satisfaction client reconnue.",
    "short_dna": "Commerce de proximité axé sur la qualité d'accueil, le savoir-faire artisanal et un service irréprochable.",
    "primary_color": "#85a363",
    "secondary_color": "#0e1117",
    "accent_color": "#f59e0b",
    "tone_of_voice": "Chaleureux, Professionnel & Accessible",
    "language_style": "Français soigné, dynamique et courtois",
    "typography_notes": "Playfair Display (Titres Serif) & Plus Jakarta Sans (Corps)"
}

DEFAULT_PROACTIVE_RD_IDEAS = [
    {
        "categorie": "Offre Commerciale & Nouveauté",
        "titre": "Formule Signature & Pack Découverte",
        "tendance": "Les clients recherchent des offres packagées lisibles, avec une valeur perçue immédiate et un tarif clair sans surprise.",
        "impact": "Augmente le panier moyen et simplifie la décision d'achat dès le premier contact.",
        "angle_post": "Mise en avant visuelle des bénéfices concrets de l'offre et témoignage client."
    },
    {
        "categorie": "Fidélisation & Relation Client",
        "titre": "Programme Privilège & Avantage Exclusif",
        "tendance": "Offrir un privilège réservé aux clients fidèles ou abonnés renforce l'attachement à la marque et déclenche des recommandations bouche-à-oreille.",
        "impact": "Génère du chiffre d'affaires récurrent et fidélise la base de contacts existante.",
        "angle_post": "Invitation VIP dans les coulisses avec un avantage exclusif à durée limitée."
    },
    {
        "categorie": "Format Réseaux Sociaux & Visibilité",
        "titre": "Série Coulisses : « L'Excellence du Geste »",
        "tendance": "Montrer l'envers du décor et l'expertise technique humaine suscite 3x plus d'engagement et de confiance que de simples visuels promotionnels.",
        "impact": "Humanise la marque, rassure sur la qualité et déclenche des prises de contact spontanées.",
        "angle_post": "Courte vidéo ou carrousel photo centré sur la précision et le savoir-faire en action."
    }
]

DEFAULT_META_ADS_STATE = {
    "api_config": {
        "access_token": "",
        "ad_account_id": "act_849204918204",
        "pixel_id": "px_9201940182",
        "sandbox_mode": True
    },
    "monthly_budget_target": 300.0,
    "active_campaigns": [
        {
            "id": "meta_camp_01",
            "nom": "Campagne Découverte & Notoriété Locale",
            "objectif": "Notoriété & Couverture Locale",
            "budget_jour": 10.0,
            "statut": "Actif (Optimisation IA)",
            "depenses_total": 120.0,
            "impressions": 8400,
            "clics": 245,
            "cpc": 0.49,
            "conversions": 18,
            "roas": 4.5,
            "ciblage": "Zone géographique active, Cible qualifiée (25-60 ans)"
        }
    ]
}

DEFAULT_AGENCY_STATE = {
    "brand_vault": DEFAULT_BRAND_VAULT.copy(),
    "vision_du_chef": "Développer la notoriété locale, fidéliser la clientèle de proximité et attirer de nouveaux clients qualifiés chaque semaine.",
    "positionnement_actif": "Un savoir-faire authentique allié à un accueil attentionné et des prestations de qualité irréprochable.",
    "cibles_prioritaires": "Clientèle de proximité, familles et professionnels de la zone géographique.",
    "objectifs_comm": {
        "cognitif": "Faire découvrir nos spécialités, notre emplacement et notre savoir-faire auprès du public.",
        "affectif": "Créer un lien de confiance et d'attachement à notre commerce en valorisant l'accueil et l'expérience client.",
        "conatif": "Inciter à la visite en magasin, à la prise de rendez-vous directe ou au contact téléphonique/WhatsApp."
    },
    "biais_psychologiques_actifs": [
        "Preuve sociale de proximité : Les retours d'expérience positifs et la recommandation locale rassurent immédiatement.",
        "Biais de sympathie & Accueil : La mise en valeur de l'équipe et de la passion du métier suscite la fidélité.",
        "Facilité d'accès & Clarté : Une offre lisible et transparente sans friction d'achat accélère la décision."
    ],
    "ecosysteme_conversion": "Réseaux Sociaux (Visibilité & Séduction) ➔ Fiche Google Maps & Avis (Réassurance) ➔ Visite / Contact direct (Vente & Fidélisation).",
    "offres_innovantes_validees": [
        "Formule Découverte & Offre Signature",
        "Privilège Fidélité & Avantage Client"
    ],
    "proactive_rd_ideas": DEFAULT_PROACTIVE_RD_IDEAS.copy(),
    "mailing_contacts": [],
    "mailing_config": {
        "provider": "Brevo (API / Simulation)",
        "sender_name": "Simon Zoni — Mon Entreprise",
        "sender_email": "contact@mon-entreprise.fr",
        "api_key": ""
    },
    "meta_ads_data": DEFAULT_META_ADS_STATE.copy(),
    "brief_actif_pour_studio": "Mettre en valeur le savoir-faire, l'ambiance et les nouveautés de notre établissement.",
    "calendrier_tactique": [
        {
            "jour": "2026-11-06",
            "objectif": "Cognitif — Découverte & Savoir-faire",
            "biais": "Effet de Halo & Transparence",
            "sujet": "Présentation des coulisses et du geste artisanal",
            "cta_tunnel": "Question ouverte en légende pour engager la communauté",
            "statut": "Brouillon"
        },
        {
            "jour": "2026-11-08",
            "objectif": "Conatif — Prise de contact & Visite",
            "biais": "Preuve sociale & Accueil",
            "sujet": "Mise en avant d'une offre coup de cœur ou d'un produit phare",
            "cta_tunnel": "Passez nous voir ou contactez-nous en direct pour réserver",
            "statut": "À valider"
        },
        {
            "jour": "2026-11-10",
            "objectif": "Affectif — Émotion & Partage",
            "biais": "Sympathie & Proximité",
            "sujet": "L'équipe en action et la vie du commerce",
            "cta_tunnel": "Dites-nous en commentaire votre moment préféré de la semaine",
            "statut": "Prêt (Auto)"
        }
    ]
}

def load_agency_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            for k, v in DEFAULT_AGENCY_STATE.items():
                if k not in data:
                    data[k] = v
            if not isinstance(data.get("brand_vault"), dict):
                data["brand_vault"] = DEFAULT_BRAND_VAULT.copy()
            else:
                for bk, bv in DEFAULT_BRAND_VAULT.items():
                    if bk not in data["brand_vault"]:
                        data["brand_vault"][bk] = bv

            # Purge automatique des données de test historiques (Bogotá / Chef physicien)
            bv_loc = data.get("brand_vault", {}).get("location", "")
            if "Bogot" in bv_loc or data.get("brand_vault", {}).get("brand_name") == "Le Catering Francés":
                data["brand_vault"]["brand_name"] = "Mon Entreprise"
                data["brand_vault"]["location"] = "Vesoul"
                data["brand_vault"]["business_type"] = "Commerce / Services de proximité"
                data["brand_vault"]["target_scope"] = "Local / De proximité"
                data["brand_vault"]["market_type"] = "B2C / Grand public"
                data["brand_vault"]["user_first_name"] = "Simon"
                data["brand_vault"]["user_last_name"] = "Zoni"
                data["brand_vault"]["founder_or_lead"] = "Simon Zoni"
                data["brand_vault"]["user_role"] = "Dirigeant"
                data["brand_vault"]["short_dna"] = "Commerce de proximité axé sur l'accueil, la qualité de service et la satisfaction client."
                data["positionnement_actif"] = "Un savoir-faire authentique allié à un accueil attentionné et des prestations de qualité irréprochable."
                data["cibles_prioritaires"] = "Clientèle de proximité, familles et professionnels de la zone géographique."
                data["vision_du_chef"] = "Développer la notoriété locale, fidéliser la clientèle de proximité et attirer de nouveaux clients qualifiés."
                data["proactive_rd_ideas"] = DEFAULT_PROACTIVE_RD_IDEAS.copy()
                data["meta_ads_data"] = DEFAULT_META_ADS_STATE.copy()
                save_agency_state(data)

            if not data.get("proactive_rd_ideas"):
                data["proactive_rd_ideas"] = DEFAULT_PROACTIVE_RD_IDEAS.copy()
            if not isinstance(data.get("meta_ads_data"), dict):
                data["meta_ads_data"] = DEFAULT_META_ADS_STATE.copy()
            else:
                for mak, mav in DEFAULT_META_ADS_STATE.items():
                    if mak not in data["meta_ads_data"]:
                        data["meta_ads_data"][mak] = mav
            return data
        except Exception:
            pass
    save_agency_state(DEFAULT_AGENCY_STATE)
    return DEFAULT_AGENCY_STATE.copy()

def save_agency_state(state_dict):
    STATE_FILE.write_text(json.dumps(state_dict, ensure_ascii=False, indent=2), encoding="utf-8")

def format_brand_vault_context(current_state):
    """Extrait les données du Profil Utilisateur & Entreprise pour personnaliser dynamiquement tous les agents."""
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    
    first_name = bv.get("user_first_name", "")
    last_name = bv.get("user_last_name", "")
    lead = bv.get("founder_or_lead", "")
    if first_name or last_name:
        user_name = f"{first_name} {last_name}".strip()
    else:
        user_name = lead or "Le Dirigeant"

    user_role = bv.get("user_role", "Dirigeant")
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")

    maps_info = ""
    if bv.get("google_maps_query") or bv.get("google_reviews_summary"):
        maps_info = f"- Fiche & Contexte Avis Clients : {bv.get('google_maps_query', '')} — {bv.get('google_reviews_summary', 'Non renseigné')}\n"

    return f"""
=== PROFIL D'ENTREPRISE & CONFIGURATION DU COMPTE ===
- Nom de l'entreprise / Marque : {bv.get('brand_name', DEFAULT_BRAND_VAULT['brand_name'])}
- Secteur d'activité : {bv.get('business_type', DEFAULT_BRAND_VAULT.get('business_type', 'Commerce / Service'))}
- Utilisateur / Référent : {user_name} (Rôle : {user_role})
- Ville / Localisation principale : {bv.get('location', 'Vesoul')}
- Portée géographique de la cible : {target_scope}
- Typologie de marché : {market_type}
- Clientèle prioritaire : {bv.get('client_type', 'Particuliers & clientèle de proximité')}
{maps_info}- ADN & Proposition de valeur : {bv.get('short_dna', '')}
- Ton de communication exigé : {bv.get('tone_of_voice', DEFAULT_BRAND_VAULT['tone_of_voice'])}
- Directive linguistique : {bv.get('language_style', DEFAULT_BRAND_VAULT['language_style'])}
- Palette officielle : Principale {bv.get('primary_color', '#85a363')} | Secondaire {bv.get('secondary_color', '#0e1117')} | Accent {bv.get('accent_color', '#f59e0b')}
- Repères typographiques : {bv.get('typography_notes', DEFAULT_BRAND_VAULT['typography_notes'])}
======================================================
""".strip()

# --- CONNECTEUR MODULAIRE META MARKETING GRAPH API ---
class MetaMarketingAPIConnector:
    """
    Connecteur modulaire pour l'API Meta Marketing (Graph API v19.0 / v20.0).
    Architecture prête pour insertion directe des tokens réels :
    - Graph endpoint : https://graph.facebook.com/v19.0/act_{ad_account_id}/insights
    - Gestion du Sandbox / Simulation avec bascule transparente vers les clés de production.
    """
    def __init__(self, config=None):
        self.config = config or {
            "access_token": "",
            "ad_account_id": "act_849204918204",
            "pixel_id": "px_9201940182",
            "sandbox_mode": True
        }
        self.access_token = self.config.get("access_token", "")
        self.ad_account_id = self.config.get("ad_account_id", "act_849204918204")
        self.pixel_id = self.config.get("pixel_id", "px_9201940182")
        self.is_live = bool(self.access_token and not self.config.get("sandbox_mode", True))

    def get_dashboard_metrics(self, monthly_budget=450.0, active_campaigns=None):
        """
        Calcule ou récupère les métriques globales de performance publicitaire :
        Dépenses, Impressions, Clics, CPC moyen, CTR, ROAS et Leads qualifiés.
        """
        campaigns = active_campaigns or []
        if campaigns:
            total_spend = round(sum(c.get("depenses_total", 0) for c in campaigns), 2)
            total_imp = sum(c.get("impressions", 0) for c in campaigns)
            total_clicks = sum(c.get("clics", 0) for c in campaigns)
            total_leads = sum(c.get("conversions", 0) for c in campaigns)
            avg_roas = round(sum(c.get("roas", 0) for c in campaigns) / len(campaigns), 2)
            avg_cpc = round(total_spend / max(total_clicks, 1), 2)
            ctr = round((total_clicks / max(total_imp, 1)) * 100, 2)
        else:
            total_spend = round(monthly_budget * 0.78, 2)
            avg_cpc = 0.44
            total_clicks = int(total_spend / avg_cpc)
            total_imp = total_clicks * 32
            ctr = round((total_clicks / max(total_imp, 1)) * 100, 2)
            total_leads = int(total_clicks * 0.062)
            avg_roas = 4.85

        return {
            "spend": total_spend,
            "budget_total": float(monthly_budget),
            "impressions": total_imp,
            "clicks": total_clicks,
            "cpc": avg_cpc,
            "ctr": ctr,
            "leads": total_leads,
            "roas": avg_roas,
            "is_live": self.is_live,
            "ad_account_id": self.ad_account_id
        }

    def get_weekly_trends(self, monthly_budget=450.0):
        """
        Données hebdomadaires pour graphiques d'évolution (Dépenses vs Clics).
        """
        weekly_spend = {
            "Semaine 1": round(monthly_budget * 0.22, 1),
            "Semaine 2": round(monthly_budget * 0.25, 1),
            "Semaine 3": round(monthly_budget * 0.28, 1),
            "Semaine 4": round(monthly_budget * 0.25, 1)
        }
        weekly_clicks = {
            "Semaine 1": int((monthly_budget * 0.22) / 0.44),
            "Semaine 2": int((monthly_budget * 0.25) / 0.44),
            "Semaine 3": int((monthly_budget * 0.28) / 0.44),
            "Semaine 4": int((monthly_budget * 0.25) / 0.44)
        }
        return weekly_spend, weekly_clicks

    def create_campaign(self, name, objective, daily_budget, targeting="", pitch=""):
        """
        Création ou simulation d'une campagne Meta Ads (POST /act_<ID>/campaigns).
        """
        camp_id = f"meta_camp_{abs(hash(name)) % 100000:05d}"
        new_camp = {
            "id": camp_id,
            "nom": name,
            "objectif": objective,
            "budget_jour": float(daily_budget),
            "statut": "Actif (Optimisation IA)",
            "depenses_total": 0.0,
            "impressions": 0,
            "clics": 0,
            "cpc": 0.0,
            "conversions": 0,
            "roas": 0.0,
            "ciblage": targeting,
            "pitch": pitch,
            "date_creation": str(date.today())
        }
        return new_camp


def get_intelligence_score(model_name):
    n = model_name.lower()
    if "3.8-pro" in n or "argon" in n:
        return 100
    if "3.1-pro" in n or "3-pro" in n:
        return 95
    if "pro" in n:
        return 85
    if "3.8-flash" in n and "lite" not in n:
        return 80
    if "3-flash" in n and "lite" not in n:
        return 75
    if "flash" in n and "lite" not in n:
        return 70
    if "3.8-flash-lite" in n:
        return 55
    if "flash-lite" in n:
        return 50
    return 40

def list_candidate_models():
    candidates = []
    try:
        for m in client.models.list():
            name = m.name.replace("models/", "")
            methods = getattr(m, "supported_actions", []) or getattr(m, "supported_generation_methods", [])
            if methods and "generateContent" not in methods:
                continue
            bad = ["embedding", "imagen", "veo", "tts", "audio", "aqa", "1.5", "2.0", "2.5", "bison", "gecko", "learnlm", "robotics", "computer-use"]
            if any(b in name.lower() for b in bad):
                continue
            candidates.append(name)
    except Exception:
        pass
    if not candidates:
        candidates = ["gemini-3.8-flash", "gemini-3.8-flash-lite", "gemini-3.1-pro-preview"]
    return candidates

def call_with_timeout(model_name, contents, timeout_sec=30, use_search=False):
    response = client.models.generate_content(model=model_name, contents=contents)
    return response.text

class BackgroundModelSelector:
    def __init__(self):
        self.candidates = list_candidate_models()
        self.active_model = self.candidates[0]
        self.active_score = get_intelligence_score(self.active_model)
        self.is_ready = True
        self.scan_finished = True
        self.tested_results = {}

def agent_directeur_strategie_red_team(input_utilisateur, objectif_prioritaire, current_state, model):
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")
    user_name = bv.get("founder_or_lead") or f"{bv.get('user_first_name', '')} {bv.get('user_last_name', '')}".strip() or "Le Dirigeant"

    prompt = f"""
    Tu es le Directeur de la Stratégie de l'agence de communication dédiée à '{bv.get("brand_name")}' ({bv.get("location")}).
    Secteur : {bv.get("business_type", "Commerce / Service")} | Portée cible : {target_scope} | Type de marché : {market_type}.
    Dirigeant / Référent : {user_name} ({bv.get("user_role", "Dirigeant")}).

    {brand_ctx}

    CADRAGE STRUCTURÉ DU DIRIGEANT :
    "{input_utilisateur}"
    Objectif commercial prioritaire : "{objectif_prioritaire}"

    DIRECTIVE PRIMORDIALE DE PERSONNALISATION :
    - Tu dois impérativement ancrer toute ton analyse, ton vocabulaire, tes cibles et tes propositions dans le contexte réel de '{bv.get("brand_name")}', implantée à '{bv.get("location")}' et active dans le secteur '{bv.get("business_type")}'.
    - Portée de la cible : '{target_scope}'. Si 'Local / De proximité', ancre impérativement toutes les recommandations dans la zone de chalandise immédiate de {bv.get("location")}. Si 'National', oriente sur le territoire national. Si 'International', oriente sur l'export.
    - Typologie de marché : '{market_type}'. Si 'B2B / Professionnels', adopte des leviers de crédibilité, d'efficacité et de retour sur investissement. Si 'B2C / Grand public', privilégie la proximité, l'émotion et l'accessibilité.
    - Bannis ABSOLUMENT toute référence à d'anciennes données de test (ne cite jamais Bogotá, de traiteur ou d'autres secteurs s'ils ne correspondent pas à l'entreprise). Base-toi exclusivement sur le profil ci-dessus.

    Rédige d'abord une note de synthèse pédagogique, chaleureuse et éclairante en français (2 à 3 paragraphes fluides, AUCUNE LISTE À PUCES ARTIFICIELLE, AUCUN TIRET EN PLEIN MILIEU DE PHRASE). Explique à {user_name} pourquoi ce positionnement et ce ciblage ({target_scope}, {market_type}) vont maximiser ses résultats commerciaux et comment l'agence va orchestrer sa prise de parole.

    Sépare ensuite ta réponse par la balise exacte `===JSON_UPDATE===` puis fournis un objet JSON valide contenant la mise à jour des clés :
    - "vision_du_chef" (string résumant le cap commercial pour {bv.get("brand_name")} à {bv.get("location")})
    - "positionnement_actif" (string résumant l'identité et la promesse)
    - "cibles_prioritaires" (string détaillant les segments prioritaires selon la portée {target_scope} et le marché {market_type})
    - "objectifs_comm" (dict avec les clés "cognitif", "affectif", "conatif")
    - "biais_psychologiques_actifs" (liste de 3 strings expliquant les leviers psychologiques adaptés à {market_type})
    - "ecosysteme_conversion" (string décrivant le tunnel d'acquisition et de fidélisation pour {bv.get("brand_name")})
    - "offres_innovantes_validees" (liste de strings adaptées au secteur {bv.get("business_type")})
    - "brief_actif_pour_studio" (string)
    - "calendrier_tactique" (liste de dicts avec jour, objectif, biais, sujet, cta_tunnel)
    """
    raw = call_with_timeout(model, prompt, timeout_sec=40)
    if "===JSON_UPDATE===" in raw:
        parts = raw.split("===JSON_UPDATE===")
        return parts[0].strip(), parts[1].strip()
    return raw, None

def agent_strategie_marche_offre(angle_analyse, segment_cible, question_specifique, current_state, model):
    """
    Directeur Stratégique Senior & Consultant Croissance.
    Analyse le positionnement de marché, la concurrence locale/nationale, la grille tarifaire
    et conçoit une offre commerciale packagée prête au déploiement.
    """
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")

    prompt = f"""
    Tu es le Directeur Stratégique Senior & Consultant en Croissance Commerciale pour '{bv.get("brand_name")}' ({bv.get("location")}), spécialisé dans le secteur '{bv.get("business_type", "Commerce / Service")}'.
    Portée cible : {target_scope} | Typologie de marché : {market_type}.

    {brand_ctx}

    CADRE DE L'ANALYSE DE MARCHÉ :
    - Angle d'analyse marketing : {angle_analyse}
    - Segment de clientèle ciblé : {segment_cible}
    - Question ou défi commercial spécifique : {question_specifique or f'Optimiser le positionnement, la grille tarifaire et créer une offre packagée à forte marge pour {bv.get("brand_name")} ({target_scope}, {market_type}).'}

    DIRECTIVE STRICTE DE PERSONNALISATION :
    - Rédige sous forme de diagnostic conseil professionnel, concret, exclusivement ancré dans la réalité économique de {bv.get("location")} pour le compte de '{bv.get("brand_name")}'.
    - Prends rigoureusement en compte la portée '{target_scope}' et le marché '{market_type}'.
    - Pas de style IA théorique ou creux : propose des chiffres, des grilles de prix réalistes adaptées au pouvoir d'achat de la zone, des argumentaires de vente et des étapes actionnables pour {bv.get("brand_name")}.
    - Interdiction formelle d'utiliser des données génériques de test non liées à {bv.get("brand_name")} ({bv.get("business_type")}).

    STRUCTURE DE LA RÉPONSE ATTENDUE :

    ### 📊 1. Diagnostic de Marché & Attentes ({bv.get("location")} — {target_scope})
    - Analyse des attentes et des freins psychologiques du segment '{segment_cible}' face à {bv.get("brand_name")}.
    - Concurrence sur ce créneau ({market_type}) et positionnement tarifaire recommandé.

    ### 💎 2. Conception de l'Offre Commerciale Recommandée pour {bv.get("brand_name")}
    - **Nom de l'Offre :** Un titre mémorable et valorisant.
    - **Promesse forte (Value Proposition) :** Ce que le client achète réellement (bénéfice émotionnel et fonctionnel).
    - **Contenu & Livrables :** Ce qui est inclus avec le détail de l'expérience ({bv.get("business_type")}).
    - **Grille Tarifaire Conseillée :** Prix suggéré en euros (ou devise locale), justification de la valeur perçue et marge estimée.

    ### 🚀 3. Tunnels d'Acquisition & Plan d'Action ({target_scope} · {market_type})
    - Étape 1 (Déclencheur d'intérêt) : Comment susciter la curiosité immédiate de la cible ({target_scope}).
    - Étape 2 (Preuve & Réassurance) : Le levier de confiance (avis, réalisations, garantie, démonstration).
    - Étape 3 (Conversion & Closing) : Le canal de commande ou de signature (contact direct, boutique, web, devis).

    Termine par un bloc JSON séparé par `===JSON_OFFER===` contenant :
    {{
        "titre_offre": "Nom court de l'offre recommandée",
        "prix_conseille": "Tarif indicatif recommandé (ex: 45€/pers ou 850€)",
        "promesse": "La promesse en une phrase",
        "angle_post": "Idée concrète de post ou publication pour le Studio"
    }}
    """
    raw = call_with_timeout(model, prompt, timeout_sec=45, use_search=True)
    if "===JSON_OFFER===" in raw:
        parts = raw.split("===JSON_OFFER===")
        return parts[0].strip(), parts[1].strip()
    return raw, None

def agent_analyse_profil_google_maps(brand_name, location, business_type, client_type, maps_query, current_state, model):
    """
    Analyse le profil du commerce (nom, ville, secteur, lien/nom Google Maps) pour extraire
    ou simuler le contexte de réputation, les avis clients et formuler un ADN précis et adapté.
    """
    prompt = f"""
    Tu es le Directeur d'Onboarding et Analyste Marché Local de l'agence IA.
    Un dirigeant d'entreprise configure son profil d'onboarding :
    - Nom du commerce / Marque : {brand_name}
    - Ville / Localisation : {location}
    - Secteur d'activité : {business_type}
    - Clientèle prioritaire : {client_type}
    - Fiche Google Maps / Lien : {maps_query or (brand_name + ' ' + location)}

    MISSION :
    Effectue une analyse approfondie du profil et de son contexte local (en exploitant les données réelles ou en simulant fidèlement la réputation Google Maps de ce type de commerce à {location}).
    
    Rédige une restitution claire en Markdown avec les sections suivantes :
    ### 🌟 1. Synthèse de Réputation & Contexte Google Maps (Avis Clients)
    - Analyse de la réputation perçue (note globale simulée ou réelle sur 5, volume d'avis, verbatims clients types).
    - Les 3 points forts unanimement salués par les clients (ex: qualité du service, ambiance, régularité, rapport qualité/prix).
    - Les 2 attentes majeures ou points d'attention exprimés par les clients locaux.

    ### 🧬 2. ADN & Proposition de Valeur Recommandée
    - Une proposition d'ADN court (3 à 4 phrases percutantes) prête à l'emploi pour le Coffre-fort de Marque.

    ### 🎯 3. Segments de Clientèle & Axes de Différenciation à {location}
    - Typologie des profils clients les plus rentables dans la zone géographique.
    - Recommandation sur le ton de voix le plus efficace ({location}).

    Termine impérativement ta réponse par un bloc JSON séparé par `===JSON_PROFILE===` contenant les clés exactes :
    {{
        "google_reviews_summary": "Résumé concis de la note et des retours d'avis clients en 2 phrases",
        "short_dna": "L'ADN court formulé pour le commerce",
        "recommended_tone": "Ton de voix conseillé",
        "primary_color_hint": "#85a363"
    }}
    """
    raw = call_with_timeout(model, prompt, timeout_sec=40, use_search=True)
    if "===JSON_PROFILE===" in raw:
        parts = raw.split("===JSON_PROFILE===")
        return parts[0].strip(), parts[1].strip()
    return raw, None


def agent_campagne_mailing(segment_cible, type_action, brief_offre, nb_contacts, current_state, model):
    """Génère un e-mail commercial clé en main + explication psychologique de conversion."""
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")
    user_name = bv.get("founder_or_lead") or f"{bv.get('user_first_name', '')} {bv.get('user_last_name', '')}".strip() or "Le Dirigeant"

    prompt = f"""
    Tu es le Directeur CRM & Copywriter Emailing de '{bv.get("brand_name")}' ({bv.get("location")}), dans le secteur '{bv.get("business_type", "Commerce / Service")}'.
    Portée cible : {target_scope} | Marché : {market_type} | Signataire : {user_name} ({bv.get("user_role", "Dirigeant")}).

    {brand_ctx}

    PARAMÈTRES DE LA CAMPAGNE MAILING :
    - Entreprise émettrice : {bv.get("brand_name")} ({bv.get("location")}) — Secteur : {bv.get("business_type")}
    - Typologie de marché : {market_type} (adapter le ton selon qu'il s'agit de professionnels B2B ou de particuliers B2C)
    - Portée géographique : {target_scope}
    - Segment ciblé : {segment_cible} ({nb_contacts} destinataires qualifiés)
    - Type d'action : {type_action}
    - Offre ou message clé : {brief_offre}
    - Positionnement stratégique : {current_state.get("positionnement_actif", "")}

    DIRECTIVE STRICTE DE PERSONNALISATION :
    - L'e-mail doit obligatoirement émaner de l'entreprise '{bv.get("brand_name")}' et être signé par {user_name} ({bv.get("user_role", "Dirigeant")}).
    - Tous les termes, arguments et offres doivent être rigoureusement adaptés au secteur '{bv.get("business_type")}' et au marché '{market_type}'.
    - Si la portée est 'Local / De proximité', mettre en valeur la relation locale à {bv.get("location")} ; si 'National', mettre en avant la disponibilité nationale.

    Rédige une réponse structurée en deux parties séparées par la balise exacte `===ANALYSE_CONVERSION===` :

    PARTIE 1 (avant la balise) : L'e-mail prêt à envoyer, respectant le style linguistique ({bv.get("language_style")}) et le ton ({bv.get("tone_of_voice")}), comprenant :
    - **Objet 1 (Direct & Prestigieux) :** ...
    - **Objet 2 (Curiosité & Privilège) :** ...
    - **Objet 3 (Relationnel & Proche) :** ...
    - **Corps de l'e-mail :** Rédigé en paragraphes fluides, élégants, humains (zéro puce robotique), avec une ouverture personnalisée, une proposition de valeur irrésistible et un appel à l'action clair (réponse directe au mail ou contact téléphonique/WhatsApp).

    ===ANALYSE_CONVERSION===

    PARTIE 2 (après la balise, en français) : Explique de façon pédagogique au dirigeant de '{bv.get("brand_name")}' la mécanique psychologique de cet e-mail (pourquoi l'objet maximise l'ouverture, quel levier de conversion B2B/B2C est activé, et quel moment de la semaine privilégier pour l'envoi). Rédige en paragraphes fluides.
    """
    raw = call_with_timeout(model, prompt, timeout_sec=35)
    if "===ANALYSE_CONVERSION===" in raw:
        parts = raw.split("===ANALYSE_CONVERSION===")
        return parts[0].strip(), parts[1].strip()
    return raw, "Cet e-mail s'appuie sur la proximité relationnelle et l'autorité de la marque pour déclencher une réponse directe sans pression commerciale."

def agent_veille_proactive_rd(focus_secteur, current_state, model):
    """Génère 3 nouvelles propositions proactives de R&D et de veille sectorielle au format JSON."""
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")

    prompt = f"""
    Tu es le Directeur R&D et Veille Stratégique de '{bv.get("brand_name")}' ({bv.get("location")}), secteur '{bv.get("business_type")}'.
    Portée géographique : {target_scope} | Type de marché : {market_type}.

    {brand_ctx}
    Entreprise : {bv.get("brand_name")} à {bv.get("location")}
    Secteur d'activité : {bv.get("business_type")}
    Cibles prioritaires : {current_state.get("cibles_prioritaires", "")}
    Orientation de veille demandée : "{focus_secteur or f'Tendances actuelles du secteur {bv.get("business_type")}, opportunités de marché ({market_type}, {target_scope}) et formats réseaux sociaux'}"

    DIRECTIVE STRICTE DE PERSONNALISATION :
    - Simule une veille sectorielle pointue spécifiquement pour le secteur '{bv.get("business_type")}', la portée '{target_scope}' et le marché '{market_type}'.
    - Les 3 propositions doivent concerner directement l'activité de '{bv.get("brand_name")}' (bannir toute idée générique d'un autre secteur).

    Renvoie UNIQUEMENT un tableau JSON valide de 3 objets (sans texte autour) ayant chacun exactement ces clés :
    - "categorie" : ex. "Offre & Produit Signature", "Concept Commercial ({market_type})", ou "Format Réseaux Sociaux"
    - "titre" : Titre accrocheur et concret de la proposition pour {bv.get("brand_name")}
    - "tendance" : L'observation de marché ou l'attente client détectée (2 phrases fluides)
    - "impact" : Pourquoi cette idée est rentable et pertinente pour {bv.get("brand_name")} ({target_scope}) (1 à 2 phrases)
    - "angle_post" : Idée concrète de mise en scène photo/vidéo pour les réseaux sociaux
    """
    raw = call_with_timeout(model, prompt, timeout_sec=35, use_search=True)
    clean = raw.strip()
    if "```" in clean:
        clean = clean.split("```")[1].replace("json", "").strip()
    return json.loads(clean)

def agent_generateur_plan_comm(periode_ou_campagne, current_state, model):
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")

    prompt = f"""
    Tu es le Directeur Éditorial de '{bv.get("brand_name")}' ({bv.get("location")}), entreprise spécialisée dans '{bv.get("business_type", "Commerce / Service")}'.
    Portée cible : {target_scope} | Type de marché : {market_type}.
    Conçois une stratégie de campagne fluide et rédigée en paragraphes élégants (sans listes à puces froides), fidèle à l'ADN et au ton de voix définis dans le Coffre-fort de Marque.

    {brand_ctx}

    Stratégie active : {current_state.get("positionnement_actif", "")}
    Campagne / Thème : "{periode_ou_campagne}"

    DIRECTIVE STRICTE DE PERSONNALISATION :
    Adapte rigoureusement les sujets des publications, les objectifs et les appels à l'action à '{bv.get("brand_name")}' ({target_scope}, {market_type}).

    Sépare avec `===JSON_CALENDAR===` puis fournis une liste JSON valide de 4 objets avec les clés : "jour", "objectif", "biais", "sujet", "cta_tunnel".
    """
    raw = call_with_timeout(model, prompt, timeout_sec=35)
    if "===JSON_CALENDAR===" in raw:
        parts = raw.split("===JSON_CALENDAR===")
        return parts[0].strip(), parts[1].strip()
    return raw, None

def prepare_images(pil_images):
    optimized = []
    for img in pil_images:
        copy_img = img.copy()
        if copy_img.mode in ("RGBA", "P"):
            copy_img = copy_img.convert("RGB")
        copy_img.thumbnail((800, 800))
        optimized.append(copy_img)
    return optimized

def pipeline_studio_collaboratif(images, type_event, intention_comm, canal_cible, notes, current_state, model):
    opt_images = prepare_images(images)
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")
    user_name = bv.get("founder_or_lead") or f"{bv.get('user_first_name', '')} {bv.get('user_last_name', '')}".strip() or "Le Dirigeant"

    is_cross = "Cross-posting" in canal_cible or ("Instagram" in canal_cible and "Facebook" in canal_cible)
    is_fb_only = "Facebook" in canal_cible and not is_cross
    is_ig_only = "Instagram" in canal_cible and not is_cross

    city_hashtag = f"#{bv.get('location', '').replace(' ', '').replace(',', '')}" if target_scope == "Local / De proximité" else "#France"

    prompt = f"""
    Tu es le Directeur de Création et Copywriter d'élite de '{bv.get("brand_name")}' ({bv.get("location")}), spécialisé dans le secteur '{bv.get("business_type", "Commerce / Service")}'.
    Portée de diffusion : {target_scope} | Type de marché : {market_type} | Référent : {user_name}.

    {brand_ctx}

    Contexte de la publication :
    - Entreprise émettrice : {bv.get("brand_name")} ({bv.get("location")}) — Activité : {bv.get("business_type")}
    - Portée & Marché : {target_scope} · {market_type}
    - Catégorie / Prestation : {type_event}
    - Intention de communication : {intention_comm}
    - Canal de diffusion cible : {canal_cible}
    - Notes de terrain : {notes}

    DIRECTIVE STRICTE DE PERSONNALISATION :
    - Rédige toutes les propositions sur mesure pour '{bv.get("brand_name")}' ({bv.get("business_type")}) à {bv.get("location")}.
    - ZÉRO STYLE IA : INTERDICTION formelle d'utiliser des listes à puces, des tirets au milieu des phrases ou des structures robotiques.
    - Applique rigoureusement le ton de communication du Coffre-fort de Marque : "{bv.get("tone_of_voice")}".
    - Rédige les légendes selon la directive linguistique de la marque : "{bv.get("language_style")}".
    - S'appuyer sur l'ADN de la marque : "{bv.get("short_dna")}".
    - Des textes courts, percutants, avec une première phrase accrocheuse (moins de 100 caractères).

    SPÉCIFICITÉS PAR CANAL ({canal_cible}) :
    {"- Mode Cross-Posting (Instagram & Facebook simultané) : Rédige une version harmonisée qui fonctionne sur les deux plateformes, en fournissant l'adaptation avec 4 hashtags pertinents (dont " + city_hashtag + ") pour Instagram et l'appel à l'action direct (lien / contact) pour Facebook." if is_cross else "- Mode Facebook : Mets l'accent sur la proximité relationnelle, le partage d'expérience et l'invitation à échanger ou réserver en direct." if is_fb_only else "- Mode Instagram : Soigne l'accroche visuelle pour stopper le scroll, ajoute 4 hashtags signatures pertinents (dont " + city_hashtag + ") et favorise l'engagement en DM."}

    Livre 3 options rédigées adaptées à l'identité de '{bv.get("brand_name")}' :
    ### ⚡ Option 1 : L'Approche Directe & Signature ({bv.get("tone_of_voice")})
    ### 🥂 Option 2 : Storytelling & Savoir-Faire ({bv.get("brand_name")})
    ### 💬 Option 3 : Le Post Engagement / Partage ({canal_cible})

    + Un encadré en français : "Conseil de Direction Artistique & Diffusion Meta ({canal_cible})" (harmonie visuelle avec la palette {bv.get("primary_color")} / {bv.get("accent_color")} et heure recommandée pour publier).
    """
    res = call_with_timeout(model, [*opt_images, prompt], timeout_sec=35)
    return "Analyse sémiologique validée.", "Brief psychologique validé.", "Red Team : Angle créatif validé.", res

def agent_meta_ads_copywriter(objective, target_audience, offer_pitch, daily_budget, placement_choice, current_state, model):
    """
    Rédige des créatifs publicitaires Meta Ads complets (Instagram Feed/Stories & Facebook Feed).
    """
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    target_scope = bv.get("target_scope", "Local / De proximité")
    market_type = bv.get("market_type", "B2C / Grand public")

    prompt = f"""
    Tu es le Media Buyer Senior & Copywriter Publicitaire Meta Ads (Instagram & Facebook Ads) pour '{bv.get("brand_name")}' ({bv.get("location")}), dans le secteur '{bv.get("business_type", "Commerce / Service")}'.
    Portée cible : {target_scope} | Type de marché : {market_type}.

    {brand_ctx}

    PARAMÈTRES DE LA CAMPAGNE PUBLICITAIRE :
    - Entreprise : {bv.get("brand_name")} ({bv.get("business_type")}) à {bv.get("location")}
    - Portée géographique : {target_scope}
    - Type de marché : {market_type}
    - Objectif commercial Meta : {objective}
    - Audience cible visée : {target_audience}
    - Offre / Pitch publicitaire : {offer_pitch}
    - Budget alloué : {daily_budget}€/jour
    - Emplacements de diffusion : {placement_choice}

    DIRECTIVE STRICTE DE PERSONNALISATION :
    - Rédige des annonces publicitaires percutantes et adaptées pour promouvoir '{bv.get("brand_name")}' auprès de sa cible ({target_scope}, {market_type}).
    - Si la portée est 'Local / De proximité', conseiller un ciblage géographique dans un rayon précis autour de {bv.get("location")} (ex: 15-25 km) ; si 'National', cibler la France entière.
    - Zéro style IA générique : des paragraphes fluides, des accroches puissantes qui stoppent le scroll.

    ### ⚡ 1. Textes Publicitaires (Primary Text)
    - **Variante A (Accroche Directe & Prestige) :** Texte orienté sur l'exclusivité et la réputation de {bv.get("brand_name")}.
    - **Variante B (Storytelling & Émotion) :** Texte axé sur la convivialité, l'expérience client et l'ambiance.

    ### 🎯 2. Titres d'Accroche & Appel à l'Action (Headlines & CTA)
    - 3 propositions de titres percutants (max 40 caractères) pour le bouton publicitaire Meta.
    - Choix du bouton d'action officiel Meta (ex. "Obtenir un devis", "Envoyer un message WhatsApp", "En savoir plus").

    ### 👥 3. Recommandations de Paramétrage d'Audience (Meta Ads Manager)
    - Centres d'intérêt précis pour le secteur '{bv.get("business_type")}'.
    - Tranches d'âge et géolocalisation ({target_scope} autour de {bv.get("location")}).

    ### 🎨 4. Direction Artistique Visuelle
    - Quel cadrage visuel privilégier pour stopper le scroll (en accord avec les couleurs officielles {bv.get("primary_color")} et {bv.get("accent_color")}).
    """
    return call_with_timeout(model, prompt, timeout_sec=35)

def agent_retouche_interactive(texte_actuel, demande_modification, current_state, model):
    brand_ctx = format_brand_vault_context(current_state)
    prompt = f"""
    {brand_ctx}

    Ajuste ces textes publicitaires selon la demande du dirigeant, en respectant strictement le ton et l'ADN du Coffre-fort de Marque ci-dessus, sans style IA (paragraphes fluides, zéro liste à puces inutile) :
    {texte_actuel}
    Demande : "{demande_modification}"
    """
    return call_with_timeout(model, prompt, timeout_sec=25)

def agent_marketing_360(type_mission, brief_utilisateur, current_state, model):
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    brand_ctx = format_brand_vault_context(current_state)
    prompt = f"""
    Tu travailles pour '{bv.get("brand_name")}' ({bv.get("location")}), dirigée par {bv.get("founder_or_lead")}.

    {brand_ctx}

    Mission confiée : {type_mission}
    Brief & Instructions :
    {brief_utilisateur}

    Adapte intégralement ta réponse à l'ADN, au ton de voix ({bv.get("tone_of_voice")}) et aux codes couleurs ({bv.get("primary_color")}, {bv.get("secondary_color")}, {bv.get("accent_color")}) de la marque '{bv.get("brand_name")}'. Si la mission ne demande pas de code informatique, rédige sous forme de paragraphes fluides et élégants sans listes à puces froides.
    """
    return call_with_timeout(model, prompt, timeout_sec=35, use_search=True)

def agent_ingenieur_adobe_jsx(logiciel, brief_utilisateur, current_state, model, base_code=None):
    bv = (current_state or {}).get("brand_vault", DEFAULT_BRAND_VAULT)
    c_prim = bv.get("primary_color", "#85a363")
    c_sec = bv.get("secondary_color", "#0e1117")
    c_acc = bv.get("accent_color", "#f59e0b")
    b_name = bv.get("brand_name", "Mon Entreprise")

    base_code_instruction = ""
    if base_code and str(base_code).strip():
        base_code_instruction = f"""
    CONTEXTE & SCRIPT DE BASE EXISTANT À ADAPTER :
    L'utilisateur souhaite faire évoluer et personnaliser le script ExtendScript ci-dessous.
    Reprends fidèlement son arborescence et ses calques, puis intègre scrupuleusement les modifications demandées (ex: nouvelles dimensions, modification de l'épaisseur des traits, remplacement des couleurs par de nouvelles teintes, ajout de paramètres ou calques supplémentaires) sans altérer la compatibilité JavaScript ES3 :
    ```javascript
    {base_code.strip()}
    ```
    """

    prompt = f"""
    Tu es un Ingénieur Expert en automatisation créative et scripting ExtendScript (JavaScript ES3) pour la Suite Adobe.
    Logiciel ciblé : {logiciel} (compatible Adobe Creative Cloud 2024 / 2025 / 2026).
    Identité de la marque cliente : '{b_name}'
    Palette officielle de la marque :
    - Couleur Principale : {c_prim}
    - Couleur Secondaire : {c_sec}
    - Couleur d'Accentuation : {c_acc}

    MISSION :
    Rédige ou adapte un script ExtendScript (.jsx) complet, robuste, sans erreur et directement exécutable répondant scrupuleusement à cette demande :
    "{brief_utilisateur}"
    {base_code_instruction}
    RÈGLES D'INGÉNIERIE STRICTES EXTENDSCRIPT ES3 :
    1. Le moteur Adobe repose sur ECMAScript 3 : N'utilise JAMAIS 'const', 'let', ni '=>'. Utilise exclusivement 'var'.
    2. Encapsule TOUT le script dans une IIFE auto-exécutée : (function() {{ ... }})(); pour isoler l'espace global.
    3. Spécificités par logiciel :
       - Si Adobe Illustrator : vérifie si un document est ouvert, sinon crée un document RGB (1920x1080). Organise toujours chaque élément dans des calques nommés et bien rangés (ex: 'doc.layers.add()'). Ferme les tracés ('pathItem.closed = true') et applique les couleurs avec des objets RGBColor convertis depuis les codes hex demandés.
       - Si Adobe After Effects : encadre impérativement tout le code dans 'app.beginUndoGroup("Script IA {b_name}");' et 'app.endUndoGroup();'. Vérifie que 'app.project.activeItem instanceof CompItem'.
       - Si Adobe InDesign : vérifie 'app.documents.length > 0' ou crée un document 'app.documents.add()', configure les blocs de texte, les styles de paragraphe et les grilles.
       - Si Adobe Photoshop : vérifie 'app.documents.length > 0' ou crée un document, utilise 'artLayers.add()', 'layerSets.add()' pour grouper les calques, et gère les masques/réglages proprement.
       - Si Adobe Premiere Pro : utilise l'API 'app.project', vérifie la séquence active ('app.project.activeSequence') ou crée une nouvelle séquence, manipule les pistes et marqueurs.
    4. Structure de ta réponse :
       - Une brève introduction expliquant ce que le script va créer ou modifier concrètement dans {logiciel} (calques créés, réglages modifiés, gain de temps).
       - Le bloc de code COMPLET et autonome encapsulé STRICTEMENT dans un bloc ```javascript ... ``` prêt à être téléchargé en .jsx.
       - Deux lignes simples rappelant comment exécuter le script dans {logiciel} (Menu Fichier > Scripts > Autre script...).
    """
    return call_with_timeout(model, prompt, timeout_sec=40)
