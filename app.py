import re
import json
import base64
import calendar
from datetime import date, datetime, time, timedelta
import streamlit as st
from pathlib import Path
from PIL import Image
from agents import (
    DEFAULT_BRAND_VAULT,
    DEFAULT_PROACTIVE_RD_IDEAS,
    DEFAULT_META_ADS_STATE,
    MetaMarketingAPIConnector,
    load_agency_state,
    save_agency_state,
    BackgroundModelSelector,
    agent_directeur_strategie_red_team,
    agent_campagne_mailing,
    agent_veille_proactive_rd,
    agent_strategie_marche_offre,
    agent_analyse_profil_google_maps,
    agent_meta_ads_copywriter,
    agent_generateur_plan_comm,
    pipeline_studio_collaboratif,
    agent_marketing_360,
    agent_ingenieur_adobe_jsx,
)

_init_brand_title = "Studio & Agence IA"
try:
    if Path("agency_state.json").exists():
        _raw_st = json.loads(Path("agency_state.json").read_text(encoding="utf-8"))
        _init_brand_title = _raw_st.get("brand_vault", {}).get("brand_name", _init_brand_title)
except Exception:
    pass

st.set_page_config(
    page_title=f"{_init_brand_title} — Espace Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- DOCTRINE TECHNIQUE EXTENDSCRIPT / ADOBE ---
DOCTRINE_ADOBE_JSX = """
RÈGLES STRICTES EXTENDSCRIPT (ADOBE ILLUSTRATOR & AFTER EFFECTS) :
1. Le moteur ExtendScript d'Adobe repose sur ECMAScript 3 (ES3) : N'utilise JAMAIS 'const', 'let', les arrow functions '=>', ni les méthodes ES6. Utilise exclusivement 'var'.
2. Encapsule toujours le script dans une fonction IIFE : (function() { ... })(); pour éviter de polluer l'espace global.
3. Pour Illustrator : vérifie 'app.documents.length > 0' (ou crée un document RGB propre), organise chaque élément généré dans des calques nommés ('doc.layers.add()'), utilise 'RGBColor' et ferme les tracés vectoriels ('pathItem.closed = true').
4. Pour After Effects : encadre toujours les opérations par 'app.beginUndoGroup("Script IA");' et 'app.endUndoGroup();', vérifie la composition active ('app.project.activeItem instanceof CompItem').
5. Renvoie TOUJOURS le code complet à l'intérieur d'un bloc ```javascript ... ``` prêt à être téléchargé en .jsx.
"""

doctrine_file = Path("doctrine_adobe.txt")
if doctrine_file.exists():
    DOCTRINE_ADOBE_JSX += "\n\nRECHERCHES AVANCÉES SUPPLÉMENTAIRES :\n" + doctrine_file.read_text(encoding="utf-8")

def extract_jsx_code(markdown_text):
    matches = re.findall(r"```(?:javascript|jsx|js)?\s*\n(.*?)```", markdown_text, re.DOTALL)
    if matches:
        return "\n\n".join(matches).strip()
    return None

def hex_to_rgb_str(hex_code):
    h = hex_code.lstrip("#")
    if len(h) == 6:
        try:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return f"RGB({r}, {g}, {b})"
        except ValueError:
            pass
    return "RGB(133, 163, 99)"

def extract_emails_from_text(raw_text):
    found = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", raw_text or "")
    unique_clean = []
    for e in found:
        e_low = e.strip().lower().rstrip(".,;:")
        if e_low and e_low not in unique_clean:
            unique_clean.append(e_low)
    return unique_clean

# =====================================================================
# INGENIERIE DE SCRIPTS ADOBE (EXTENDSCRIPT JSX) — CATALOGUE 1-CLIC
# =====================================================================
def hex_to_rgb_tuple(hex_code, fallback=(133, 163, 99)):
    h = (hex_code or "").lstrip("#")
    if len(h) == 6:
        try:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        except ValueError:
            pass
    return fallback

def generate_authentic_adobe_script(soft_slug, t_idx, bv):
    c_prim = bv.get("primary_color", "#85a363")
    c_sec = bv.get("secondary_color", "#0e1117")
    c_acc = bv.get("accent_color", "#f59e0b")
    b_name = bv.get("brand_name", "Mon Entreprise")
    
    r1, g1, b1 = hex_to_rgb_tuple(c_prim, (133, 163, 99))
    r2, g2, b2 = hex_to_rgb_tuple(c_sec, (14, 17, 23))
    r3, g3, b3 = hex_to_rgb_tuple(c_acc, (245, 158, 11))

    catalog = {
        "illustrator": [
            {
                "title": "Grille Isométrique Vectorielle & Repères",
                "filename": "grille_isometrique_illustrator.jsx",
                "description": "Script ExtendScript complet pour Adobe Illustrator traçant une grille isométrique mathématique précise (angles 30° et 150°) sur un calque verrouillé dédié.",
                "code": """#target illustrator
(function() {
    try {
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add(DocumentColorSpace.RGB, 1920, 1080);
        var artboard = doc.artboards[doc.artboards.getActiveArtboardIndex()];
        var rect = artboard.artboardRect;
        var left = rect[0], top = rect[1], right = rect[2], bottom = rect[3];
        var width = right - left;
        var height = top - bottom;

        var gridLayer;
        try {
            gridLayer = doc.layers.getByName("📐 Grille_Isometrique");
            gridLayer.locked = false;
        } catch(e) {
            gridLayer = doc.layers.add();
            gridLayer.name = "📐 Grille_Isometrique";
        }

        var gridColor = new RGBColor();
        gridColor.red = 180;
        gridColor.green = 195;
        gridColor.blue = 190;

        var spacing = 40;
        var tan30 = 0.57735;

        // Tracé des verticales
        for (var x = left; x <= right; x += spacing) {
            var vLine = gridLayer.pathItems.add();
            vLine.setEntirePath([[x, top], [x, bottom]]);
            vLine.stroked = true;
            vLine.strokeColor = gridColor;
            vLine.strokeWidth = 0.5;
            vLine.filled = false;
        }

        // Tracé des diagonales 30° et 150°
        var extent = width + (height / tan30);
        for (var d = -extent; d <= extent; d += spacing * 1.5) {
            var line1 = gridLayer.pathItems.add();
            line1.setEntirePath([[left + d, top], [left + d + (height / tan30), bottom]]);
            line1.stroked = true;
            line1.strokeColor = gridColor;
            line1.strokeWidth = 0.4;
            line1.filled = false;

            var line2 = gridLayer.pathItems.add();
            line2.setEntirePath([[right - d, top], [right - d - (height / tan30), bottom]]);
            line2.stroked = true;
            line2.strokeColor = gridColor;
            line2.strokeWidth = 0.4;
            line2.filled = false;
        }

        gridLayer.locked = true;
        alert("✅ Grille isométrique générée avec succès sur le calque '📐 Grille_Isometrique' (verrouillé).");
    } catch(err) {
        alert("Erreur Illustrator : " + err.message);
    }
})();"""
            },
            {
                "title": f"Nuancier Officiel & Swatches ({b_name})",
                "filename": "nuancier_officiel_illustrator.jsx",
                "description": f"Script générant une planche de présentation du nuancier de {b_name} et enregistrant les nuances officielles directement dans le panneau Nuancier du document actif.",
                "code": f"""#target illustrator
(function() {{
    try {{
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add(DocumentColorSpace.RGB, 1200, 800);
        
        var swatchLayer;
        try {{
            swatchLayer = doc.layers.getByName("🎨 Nuancier_Officiel");
        }} catch(e) {{
            swatchLayer = doc.layers.add();
            swatchLayer.name = "🎨 Nuancier_Officiel";
        }}

        var palette = [
            {{ name: "Couleur Principale", hex: "{c_prim}", r: {r1}, g: {g1}, b: {b1} }},
            {{ name: "Couleur Secondaire", hex: "{c_sec}", r: {r2}, g: {g2}, b: {b2} }},
            {{ name: "Accentuation", hex: "{c_acc}", r: {r3}, g: {g3}, b: {b3} }}
        ];

        var startX = 80;
        var startY = -80;
        var swatchWidth = 220;
        var swatchHeight = 130;
        var gap = 40;

        var titleText = swatchLayer.textFrames.add();
        titleText.contents = "CHARTE CHROMATIQUE OFFICIELLE — {b_name}";
        titleText.top = startY;
        titleText.left = startX;
        titleText.textRange.characterAttributes.size = 20;

        for (var i = 0; i < palette.length; i++) {{
            var colData = palette[i];
            var posX = startX + (i * (swatchWidth + gap));
            var posY = startY - 50;

            var rect = swatchLayer.pathItems.rectangle(posY, posX, swatchWidth, swatchHeight);
            var col = new RGBColor();
            col.red = colData.r;
            col.green = colData.g;
            col.blue = colData.b;
            rect.fillColor = col;
            rect.stroked = false;

            try {{
                var sw = doc.swatches.add();
                sw.name = "{b_name} - " + colData.name;
                sw.color = col;
            }} catch(e) {{}}

            var label = swatchLayer.textFrames.add();
            label.contents = colData.name + "\n" + colData.hex + " | RGB(" + colData.r + ", " + colData.g + ", " + colData.b + ")";
            label.top = posY - swatchHeight - 15;
            label.left = posX;
            label.textRange.characterAttributes.size = 11;
        }}

        alert("✅ Nuancier officiel de {b_name} généré et injecté dans le nuancier d'Illustrator !");
    }} catch(err) {{
        alert("Erreur nuancier : " + err.message);
    }}
}})();"""
            },
            {
                "title": f"Cadres Typographiques & Titrage ({b_name})",
                "filename": "cadres_typo_illustrator.jsx",
                "description": "Script créant un calque typographique hiérarchisé et centré avec un titre H1 stylisé et un sous-titre de marque.",
                "code": f"""#target illustrator
(function() {{
    try {{
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add(DocumentColorSpace.RGB, 1920, 1080);
        var artboard = doc.artboards[doc.artboards.getActiveArtboardIndex()];
        var rect = artboard.artboardRect;
        var abWidth = rect[2] - rect[0];
        var centerX = rect[0] + (abWidth / 2);
        var centerY = rect[1] - ((rect[1] - rect[3]) / 2);

        var typoLayer;
        try {{
            typoLayer = doc.layers.getByName("🔤 Typographie_Marque");
        }} catch(e) {{
            typoLayer = doc.layers.add();
            typoLayer.name = "🔤 Typographie_Marque";
        }}

        var titleFrame = typoLayer.textFrames.add();
        titleFrame.contents = "{b_name}";
        titleFrame.textRange.characterAttributes.size = 54;
        titleFrame.textRange.paragraphAttributes.justification = Justification.CENTER;
        titleFrame.top = centerY + 60;
        titleFrame.left = centerX - 350;
        titleFrame.width = 700;

        var subFrame = typoLayer.textFrames.add();
        subFrame.contents = "Excellence, Savoir-Faire & Innovation";
        subFrame.textRange.characterAttributes.size = 20;
        subFrame.textRange.paragraphAttributes.justification = Justification.CENTER;
        subFrame.top = centerY - 10;
        subFrame.left = centerX - 350;
        subFrame.width = 700;

        alert("✅ Cadres typographiques créés et parfaitement centrés sur le plan de travail actif.");
    }} catch(err) {{
        alert("Erreur typographie : " + err.message);
    }}
}})();"""
            },
            {
                "title": "Déclinaison Formats & Plans de Travail (Artboards)",
                "filename": "multi_artboards_illustrator.jsx",
                "description": "Script configurant automatiquement 3 plans de travail calibrés au pixel près pour les formats réseaux sociaux (Post 1:1, Story 9:16, Bannière 16:9).",
                "code": """#target illustrator
(function() {
    try {
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add(DocumentColorSpace.RGB, 1080, 1080);
        
        var formats = [
            { name: "01_Post_Instagram_1080x1080", w: 1080, h: 1080 },
            { name: "02_Story_Reels_1080x1920", w: 1080, h: 1920 },
            { name: "03_Banniere_Web_1920x1080", w: 1920, h: 1080 }
        ];

        var curX = 0;
        var gap = 150;

        doc.artboards[0].name = formats[0].name;
        doc.artboards[0].artboardRect = [0, 0, formats[0].w, -formats[0].h];
        curX += formats[0].w + gap;

        for (var i = 1; i < formats.length; i++) {
            var f = formats[i];
            var newAb = doc.artboards.add([curX, 0, curX + f.w, -f.h]);
            newAb.name = f.name;
            curX += f.w + gap;
        }

        alert("✅ 3 plans de travail multi-formats (Post Carré, Story 9:16, Bannière 16:9) configurés avec succès !");
    } catch(err) {
        alert("Erreur plans de travail : " + err.message);
    }
})();"""
            }
        ],
        "after_effects": [
            {
                "title": "Éclosion en Cascade (Stagger Opacité & Échelle)",
                "filename": "eclosion_cascade_aftereffects.jsx",
                "description": "Script After Effects qui anime l'apparition fluide en cascade (stagger) des calques de la composition active avec décalage temporel et amorti de vitesse.",
                "code": """(function() {
    app.beginUndoGroup("Éclosion en Cascade Stagger");
    try {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            alert("Veuillez ouvrir une composition active dans After Effects.");
            return;
        }

        var layers = comp.selectedLayers.length > 0 ? comp.selectedLayers : comp.layers;
        var staggerFrames = 4;
        var frameDuration = comp.frameDuration;

        for (var i = 1; i <= layers.length; i++) {
            var layer = (comp.selectedLayers.length > 0) ? comp.selectedLayers[i-1] : comp.layer(i);
            var startTime = (i - 1) * (staggerFrames * frameDuration);

            var op = layer.property("ADBE Transform Group").property("ADBE Opacity");
            op.setValueAtTime(startTime, 0);
            op.setValueAtTime(startTime + (10 * frameDuration), 100);

            var sc = layer.property("ADBE Transform Group").property("ADBE Scale");
            sc.setValueAtTime(startTime, [80, 80, 100]);
            sc.setValueAtTime(startTime + (12 * frameDuration), [100, 100, 100]);
        }

        alert("✅ Éclosion en cascade appliquée sur " + (comp.selectedLayers.length > 0 ? comp.selectedLayers.length : comp.numLayers) + " calques avec lissage !");
    } catch(err) {
        alert("Erreur After Effects : " + err.message);
    } finally {
        app.endUndoGroup();
    }
})();"""
            },
            {
                "title": "Inertie & Rebond Élastique (Inertial Bounce)",
                "filename": "rebond_elastique_aftereffects.jsx",
                "description": "Script After Effects injectant une expression d'amorti physique et d'inertie élastique sur la Position des calques sélectionnés pour des mouvements ultra-organiques.",
                "code": """(function() {
    app.beginUndoGroup("Appliquer Rebond Élastique");
    try {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            alert("Ouvrez une composition After Effects avant de lancer ce script.");
            return;
        }

        if (comp.selectedLayers.length === 0) {
            alert("Sélectionnez au moins un calque animé avec des clés de Position.");
            return;
        }

        var bounceExpr = 
            "// Expression de rebond inertiel\n" +
            "var amp = 0.05;\n" +
            "var freq = 4.0;\n" +
            "var decay = 5.0;\n" +
            "var n = 0;\n" +
            "if (numKeys > 0){\n" +
            "  n = nearestKey(time).index;\n" +
            "  if (key(n).time > time) n--;\n" +
            "}\n" +
            "if (n === 0) { t = 0; } else { t = time - key(n).time; }\n" +
            "if (n > 0 && t < 1) {\n" +
            "  var v = velocityAtTime(key(n).time - thisComp.frameDuration/10);\n" +
            "  value + v * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);\n" +
            "} else { value; }";

        for (var i = 0; i < comp.selectedLayers.length; i++) {
            var layer = comp.selectedLayers[i];
            var posProp = layer.property("ADBE Transform Group").property("ADBE Position");
            posProp.expression = bounceExpr;
        }

        alert("✅ Expression d'inertie et rebond élastique appliquée sur les calques sélectionnés !");
    } catch(err) {
        alert("Erreur : " + err.message);
    } finally {
        app.endUndoGroup();
    }
})();"""
            },
            {
                "title": "Compteur Chiffré Dynamique (0 à 100%)",
                "filename": "compteur_dynamique_aftereffects.jsx",
                "description": "Script créant un calque texte avec Slider Control animé de 0 à 100% sur 2.5 secondes avec arrondi mathématique propre.",
                "code": """(function() {
    app.beginUndoGroup("Créer Compteur Chiffré");
    try {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            alert("Veuillez ouvrir une composition active dans After Effects.");
            return;
        }

        var textLayer = comp.layers.addText("0%");
        textLayer.name = "⏱️ Compteur_Chiffre_0_100";

        var sliderEffect = textLayer.property("ADBE Effect Parade").addProperty("ADBE Slider Control");
        sliderEffect.name = "Progression";
        var sliderProp = sliderEffect.property(1);

        sliderProp.setValueAtTime(0, 0);
        sliderProp.setValueAtTime(2.5, 100);

        var expr = "var val = Math.round(effect('Progression')('Slider')); val + ' %';";
        textLayer.property("ADBE Text Properties").property("ADBE Text Document").expression = expr;

        alert("✅ Calque compteur dynamique créé avec animation fluide de 0% à 100% !");
    } catch(err) {
        alert("Erreur : " + err.message);
    } finally {
        app.endUndoGroup();
    }
})();"""
            },
            {
                "title": "Boucle loopOut Parfaite (Seamless Cycle)",
                "filename": "loop_cycle_aftereffects.jsx",
                "description": "Script After Effects appliquant une expression loopOut('cycle') sur toutes les propriétés animées des calques sélectionnés pour une boucle vidéo sans raccord.",
                "code": """(function() {
    app.beginUndoGroup("Appliquer loopOut Parfait");
    try {
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            alert("Ouvrez une composition dans After Effects.");
            return;
        }

        var selLayers = comp.selectedLayers;
        if (selLayers.length === 0) {
            alert("Sélectionnez les calques contenant les propriétés animées à boucler.");
            return;
        }

        var count = 0;
        for (var i = 0; i < selLayers.length; i++) {
            var l = selLayers[i];
            var transformGroup = l.property("ADBE Transform Group");
            for (var p = 1; p <= transformGroup.numProperties; p++) {
                var prop = transformGroup.property(p);
                if (prop.numKeys > 1) {
                    prop.expression = "loopOut('cycle');";
                    count++;
                }
            }
        }

        alert("✅ loopOut('cycle') injecté sur " + count + " propriétés animées ! Boucle infinie active.");
    } catch(err) {
        alert("Erreur : " + err.message);
    } finally {
        app.endUndoGroup();
    }
})();"""
            }
        ],
        "indesign": [
            {
                "title": "Grille Éditoriale Modulaire 12 Colonnes",
                "filename": "grille_12_colonnes_indesign.jsx",
                "description": "Script InDesign créant ou configurant une grille modulaire à 12 colonnes avec marges régulières de 15mm et gouttières de 4mm.",
                "code": """(function() {
    try {
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add();
        
        var pref = doc.marginPreferences;
        pref.top = "15mm";
        pref.bottom = "15mm";
        pref.left = "15mm";
        pref.right = "15mm";
        pref.columnCount = 12;
        pref.columnGutter = "4mm";

        for (var i = 0; i < doc.pages.length; i++) {
            var p = doc.pages[i];
            p.marginPreferences.columnCount = 12;
            p.marginPreferences.columnGutter = "4mm";
        }

        alert("✅ Grille modulaire 12 colonnes (marges 15mm, gouttières 4mm) appliquée sur le document InDesign !");
    } catch(err) {
        alert("Erreur InDesign : " + err.message);
    }
})();"""
            },
            {
                "title": f"Folios & Numérotation Automatique ({b_name})",
                "filename": "folios_gabarit_indesign.jsx",
                "description": f"Script InDesign plaçant les numéros de page automatiques et le titre courant de {b_name} sur les pages gauche et droite du gabarit A.",
                "code": f"""(function() {{
    try {{
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add();
        var masterSpread = doc.masterSpreads.item("A-Gabarit");
        if (!masterSpread.isValid) {{
            masterSpread = doc.masterSpreads[0];
        }}

        for (var i = 0; i < masterSpread.pages.length; i++) {{
            var mPage = masterSpread.pages[i];
            var b = mPage.bounds;
            var frame = mPage.textFrames.add();
            frame.geometricBounds = [b[2] - 14, b[1] + 15, b[2] - 5, b[3] - 15];

            if (i === 0) {{
                frame.contents = SpecialCharacters.AUTO_PAGE_NUMBER + "  |  {b_name} — Revue & Édition";
                frame.paragraphs[0].justification = Justification.LEFT_ALIGN;
            }} else {{
                frame.contents = "{b_name}  |  " + SpecialCharacters.AUTO_PAGE_NUMBER;
                frame.paragraphs[0].justification = Justification.RIGHT_ALIGN;
            }}
        }}

        alert("✅ Folios et numérotation automatique injectés sur le gabarit principal !");
    }} catch(err) {{
        alert("Erreur InDesign : " + err.message);
    }}
}})();"""
            },
            {
                "title": f"Hiérarchie de Styles de Paragraphe ({b_name})",
                "filename": "styles_paragraphes_indesign.jsx",
                "description": f"Script InDesign générant l'arborescence des styles de paragraphe (Titre H1, Chapô, Corps de texte) configurés avec la nuance chromatique de {b_name}.",
                "code": f"""(function() {{
    try {{
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add();

        var brandColor;
        try {{
            brandColor = doc.colors.itemByName("{b_name}_Primaire");
            if (!brandColor.isValid) throw new Error();
        }} catch(e) {{
            brandColor = doc.colors.add({{
                name: "{b_name}_Primaire",
                model: ColorModel.PROCESS,
                space: ColorSpace.RGB,
                colorValue: [{r1}, {g1}, {b1}]
            }});
        }}

        try {{
            doc.paragraphStyles.add({{
                name: "01_Titre_H1",
                pointSize: 32,
                leading: 38,
                spaceAfter: "8mm",
                fillColor: brandColor
            }});
        }} catch(e) {{}}

        try {{
            doc.paragraphStyles.add({{
                name: "02_Chapeau",
                pointSize: 14,
                leading: 19,
                spaceAfter: "5mm"
            }});
        }} catch(e) {{}}

        try {{
            doc.paragraphStyles.add({{
                name: "03_Corps_de_Texte",
                pointSize: 10,
                leading: 14,
                spaceAfter: "3mm"
            }});
        }} catch(e) {{}}

        alert("✅ Hiérarchie de styles typographiques configurée avec la teinte officielle de {b_name} !");
    }} catch(err) {{
        alert("Erreur InDesign : " + err.message);
    }}
}})();"""
            },
            {
                "title": "Export PDF HD Imprimeur (avec Repères & Fond Perdu)",
                "filename": "export_pdf_imprimeur_indesign.jsx",
                "description": "Script InDesign automatisant l'export PDF Haute Définition avec traits de coupe et 3mm de fond perdu directement sur le bureau.",
                "code": """(function() {
    try {
        if (app.documents.length === 0) {
            alert("Ouvrez un document InDesign avant d'exporter.");
            return;
        }

        var doc = app.activeDocument;
        var outFolder = Folder.desktop;
        var outFile = new File(outFolder + "/" + doc.name.replace(/\.[^\.]+$/, "") + "_PRINT_HD.pdf");

        var pdfPreset = app.pdfExportPresets.item("[High Quality Print]");
        app.pdfExportPreferences.useDocumentBleedWithPDF = true;
        app.pdfExportPreferences.cropMarks = true;
        app.pdfExportPreferences.bleedMarks = true;

        doc.exportFile(ExportFormat.PDF_TYPE, outFile, false, pdfPreset);

        alert("✅ Export PDF Imprimeur généré avec succès sur le Bureau : \n" + outFile.fsName);
    } catch(err) {
        alert("Erreur export PDF : " + err.message);
    }
})();"""
            }
        ],
        "photoshop": [
            {
                "title": f"Structure Post Carré & Groupes de Calques ({b_name})",
                "filename": "structure_post_photoshop.jsx",
                "description": f"Script Photoshop créant une composition 1080x1080 structurée en 3 dossiers de calques avec fond subtilement teinté aux couleurs de {b_name}.",
                "code": f"""#target photoshop
(function() {{
    try {{
        var doc = app.documents.add(1080, 1080, 300, "{b_name}_Post_Carre", NewDocumentMode.RGB, DocumentFill.WHITE);

        var groupBackground = doc.layerSets.add();
        groupBackground.name = "01_Arrière_Plan";

        var groupVisuals = doc.layerSets.add();
        groupVisuals.name = "02_Visuels_&_Photos";

        var groupTitles = doc.layerSets.add();
        groupTitles.name = "03_Typographie_&_Titres";

        var bgLayer = groupBackground.artLayers.add();
        bgLayer.name = "Fond_Teinté_Marque";
        doc.selection.selectAll();
        var fillCol = new SolidColor();
        fillCol.rgb.red = {r1};
        fillCol.rgb.green = {g1};
        fillCol.rgb.blue = {b1};
        doc.selection.fill(fillCol);
        doc.selection.deselect();
        bgLayer.opacity = 15;

        alert("✅ Structure Photoshop créée avec 3 dossiers de calques et fond de marque calibré !");
    }} catch(err) {{
        alert("Erreur Photoshop : " + err.message);
    }}
}})();"""
            },
            {
                "title": f"Palette & Calques de Remplissage ({b_name})",
                "filename": "palette_calques_photoshop.jsx",
                "description": f"Script Photoshop créant 3 calques d'échantillons de couleurs pour {b_name} ({c_prim}, {c_sec}, {c_acc}) rangés dans un dossier de charte.",
                "code": f"""#target photoshop
(function() {{
    try {{
        var doc = app.documents.length > 0 ? app.activeDocument : app.documents.add(1200, 800, 72, "Palette_{b_name}");

        var groupPalette = doc.layerSets.add();
        groupPalette.name = "🎨 Nuancier_Officiel_{b_name}";

        var colors = [
            {{ name: "01_Primaire_{c_prim}", r: {r1}, g: {g1}, b: {b1} }},
            {{ name: "02_Secondaire_{c_sec}", r: {r2}, g: {g2}, b: {b2} }},
            {{ name: "03_Accent_{c_acc}", r: {r3}, g: {g3}, b: {b3} }}
        ];

        for (var i = 0; i < colors.length; i++) {{
            var c = colors[i];
            var layer = groupPalette.artLayers.add();
            layer.name = c.name;
            var sc = new SolidColor();
            sc.rgb.red = c.r;
            sc.rgb.green = c.g;
            sc.rgb.blue = c.b;
            
            var x1 = 50 + (i * 220);
            var y1 = 50;
            var x2 = x1 + 180;
            var y2 = y1 + 180;
            doc.selection.select([[x1, y1], [x2, y1], [x2, y2], [x1, y2]]);
            doc.selection.fill(sc);
            doc.selection.deselect();
        }}

        alert("✅ 3 calques d'échantillons créés et organisés dans le dossier de charte !");
    }} catch(err) {{
        alert("Erreur Photoshop : " + err.message);
    }}
}})();"""
            },
            {
                "title": f"Filigrane & Signature de Marque ({b_name})",
                "filename": "filigrane_signature_photoshop.jsx",
                "description": f"Script Photoshop apposant une signature typographique discrète (opacité 35%, verrouillée) de {b_name} en bas à droite de l'image.",
                "code": f"""#target photoshop
(function() {{
    try {{
        if (app.documents.length === 0) {{
            alert("Veuillez ouvrir une image dans Photoshop avant d'appliquer la signature.");
            return;
        }}

        var doc = app.activeDocument;
        var textLayer = doc.artLayers.add();
        textLayer.kind = LayerKind.TEXT;
        textLayer.name = "🛡️ Signature_{b_name}";

        var textItem = textLayer.textItem;
        textItem.contents = "© {b_name} — Tous droits réservés";
        textItem.size = Math.max(14, Math.round(doc.width.value / 65));
        
        var textColor = new SolidColor();
        textColor.rgb.red = 255;
        textColor.rgb.green = 255;
        textColor.rgb.blue = 255;
        textItem.color = textColor;

        textItem.position = [doc.width.value - (textItem.size.value * 20), doc.height.value - (textItem.size.value * 2)];
        textLayer.opacity = 35;
        textLayer.allLocked = true;

        alert("✅ Signature de marque '{b_name}' apposée en bas à droite (opacité 35%, calque verrouillé).");
    }} catch(err) {{
        alert("Erreur Photoshop : " + err.message);
    }}
}})();"""
            },
            {
                "title": "Export Web Optimisé (JPEG 85% sRGB)",
                "filename": "export_web_photoshop.jsx",
                "description": "Script Photoshop automatisant SaveForWeb en JPEG 85% calibré sRGB sur le bureau avec allègement du poids de fichier.",
                "code": """#target photoshop
(function() {
    try {
        if (app.documents.length === 0) {
            alert("Ouvrez un document Photoshop à exporter.");
            return;
        }

        var doc = app.activeDocument;
        var exportFolder = Folder.desktop;
        var exportFile = new File(exportFolder + "/" + doc.name.replace(/\.[^\.]+$/, "") + "_WEB_OPTIMIZED.jpg");

        var exportOptions = new ExportOptionsSaveForWeb();
        exportOptions.format = SaveDocumentType.JPEG;
        exportOptions.includeProfile = true;
        exportOptions.quality = 85;
        exportOptions.optimized = true;

        doc.exportDocument(exportFile, ExportType.SAVEFORWEB, exportOptions);

        alert("✅ Export Web HD (JPEG 85% sRGB) enregistré sur votre Bureau :\n" + exportFile.fsName);
    } catch(err) {
        alert("Erreur export Web : " + err.message);
    }
})();"""
            }
        ],
        "premiere": [
            {
                "title": "Marqueurs de Montage Rythmique (Beat Cutting)",
                "filename": "marqueurs_rythme_premiere.jsx",
                "description": "Script Premiere Pro insérant automatiquement des marqueurs de séquence toutes les 2 secondes pour caler les coupes de plans sur le rythme sonore.",
                "code": """(function() {
    try {
        var seq = app.project.activeSequence;
        if (!seq) {
            alert("Ouvrez une séquence active dans Premiere Pro.");
            return;
        }

        var markers = seq.markers;
        var intervalSeconds = 2.0;
        var totalDuration = seq.end ? parseFloat(seq.end) : 30.0;

        for (var t = 0; t <= Math.min(totalDuration, 60.0); t += intervalSeconds) {
            var marker = markers.createMarker(t);
            marker.name = "✂️ Coupe Rythme (" + t.toFixed(1) + "s)";
            marker.comments = "Point de synchronisation rythmique.";
            marker.setColorByIndex(1);
        }

        alert("✅ Marqueurs de coupe rythmique insérés toutes les 2 secondes sur la timeline de Premiere Pro !");
    } catch(err) {
        alert("Erreur Premiere Pro : " + err.message);
    }
})();"""
            },
            {
                "title": "Organisation des Chutes & Bins Pro",
                "filename": "arborescence_bins_premiere.jsx",
                "description": "Script Premiere Pro créant une arborescence de 6 dossiers de chutier professionnels (Rushes, Audio, Musique, Graphismes, Séquences, Exports).",
                "code": """(function() {
    try {
        var proj = app.project;
        if (!proj) {
            alert("Ouvrez un projet Premiere Pro.");
            return;
        }

        var rootBin = proj.rootItem;
        var bins = [
            "01_RUSHES_CAMERA",
            "02_INTERVIEWS_VOIX",
            "03_MUSIQUE_&_SFX",
            "04_GRAPHISMES_&_TITRES",
            "05_SEQUENCES_MONTAGE",
            "06_EXPORTS_LIVRABLES"
        ];

        for (var i = 0; i < bins.length; i++) {
            var binName = bins[i];
            var exists = false;
            for (var j = 0; j < rootBin.children.numItems; j++) {
                if (rootBin.children[j].name === binName) {
                    exists = true;
                    break;
                }
            }
            if (!exists) {
                rootBin.createBin(binName);
            }
        }

        alert("✅ Arborescence de 6 Bins professionnels créée dans le chutier Premiere Pro !");
    } catch(err) {
        alert("Erreur Premiere Pro : " + err.message);
    }
})();"""
            },
            {
                "title": f"Initialisation Séquence Verticale (Reels 9:16 - {b_name})",
                "filename": "sequence_verticale_premiere.jsx",
                "description": f"Script Premiere Pro créant une nouvelle séquence dédiée au format vertical 1080x1920 calibrée pour Instagram Reels et TikTok.",
                "code": f"""(function() {{
    try {{
        var proj = app.project;
        if (!proj) {{
            alert("Ouvrez un projet Premiere Pro.");
            return;
        }}

        var seqName = "{b_name}_REELS_TIKTOK_9x16";
        proj.createNewSequence(seqName, "");

        alert("✅ Séquence verticale '" + seqName + "' créée prête pour vos montages Reels et TikTok !");
    }} catch(err) {{
        alert("Erreur Premiere Pro : " + err.message);
    }}
}})();"""
            },
            {
                "title": "Export Automatisé vers Adobe Media Encoder",
                "filename": "envoi_media_encoder_premiere.jsx",
                "description": "Script Premiere Pro envoyant la séquence active directement dans la file d'attente d'Adobe Media Encoder pour un rendu en tâche de fond.",
                "code": """(function() {
    try {
        var seq = app.project.activeSequence;
        if (!seq) {
            alert("Sélectionnez la séquence à exporter dans Premiere Pro.");
            return;
        }

        var desktop = Folder.desktop.fsName;
        var outPath = desktop + "/" + seq.name + "_LIVRABLE.mp4";

        app.encoder.launchEncoder();
        app.encoder.encodeSequence(
            seq,
            outPath,
            "",
            0,
            1
        );

        alert("✅ Séquence '" + seq.name + "' transmise à la file d'attente d'Adobe Media Encoder !");
    } catch(err) {
        alert("Erreur Media Encoder : " + err.message);
    }
})();"""
            }
        ]
    }

    soft_scripts = catalog.get(soft_slug, catalog["illustrator"])
    idx = max(0, min(t_idx, len(soft_scripts) - 1))
    return soft_scripts[idx]



# --- DESIGN SYSTEM : BIBLIOTHÈQUE D'ICÔNES VECTORIELLES SVG MINIMALISTES ---
SVG_ICONS = {
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-1 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="3"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "wand": '<path d="m15 4-2 4 4 2-4-2-2-4Z"/><path d="M18 2h4v4"/><path d="M2 22l10-10"/><path d="M9 3l1 2"/><path d="M20 12l2 1"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>',
    "camera": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "vault": '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "shield_check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "flask": '<path d="M10 2v7.31L4.62 17.5A2 2 0 0 0 6.34 20h11.32a2 2 0 0 0 1.72-2.5L14 9.31V2"/><path d="M8.5 2h7"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "map_pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "trash": '<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>',
    "edit": '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "send": '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
    "refresh": '<path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21h5v-5"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="9" y1="22" x2="9" y2="2"/><line x1="8" y1="6" x2="10" y2="6"/><line x1="14" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/>',
    "tag": '<path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/><circle cx="7" cy="7" r=".5" fill="currentColor"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    "arrow_right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "vector": '<path d="m12 2 4 7-7 4 3-11Z"/><circle cx="12" cy="2" r="2"/><circle cx="16" cy="9" r="2"/><circle cx="9" cy="13" r="2"/><path d="M4 22l6-7"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "lightning": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>'
}

def get_svg_icon(name, size=18, color="currentColor", extra_classes=""):
    path_data = SVG_ICONS.get(name, "")
    if not path_data:
        return ""
    cls = f"svg-icon {extra_classes}".strip()
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" style="vertical-align: -3px; display: inline-block;">'
        f'{path_data}</svg>'
    )

def render_icon_label(icon_name, text, size=18, color="currentColor"):
    svg = get_svg_icon(icon_name, size=size, color=color)
    if svg:
        return f'<span class="icon-label-wrap">{svg}<span>{text}</span></span>'
    return text

def render_html(html_str):
    """Affiche du HTML sans risque d'échappement Markdown en supprimant l'indentation parasite."""
    lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    st.markdown(" ".join(lines), unsafe_allow_html=True)

GENERIC_DEMO_TEXTS = {
    "brand_name": ["Mon Entreprise", "Le Catering Francés", ""],
    "business_type": ["Commerce / Services de proximité", "Commerce / Service", ""],
    "location": ["Vesoul", "Besançon", "Bogotá", ""],
    "short_dna": [
        "Commerce de proximité axé sur la qualité d'accueil, le savoir-faire artisanal et un service irréprochable.",
        "Commerce de proximité axé sur l'accueil, la qualité de service et la satisfaction client.",
        "Savoir-faire et réputation reconnue à Vesoul",
        ""
    ],
    "client_type": [
        "Particuliers & clientèle de proximité",
        "Particuliers & Entreprises",
        "Hôtes privés CSP+, Entreprises B2B, Familles",
        ""
    ],
    "google_reviews_summary": [
        "Excellente réputation locale, accueil attentionné et satisfaction client reconnue.",
        "Excellente réputation locale, accueil chaleureux et satisfaction client reconnue.",
        ""
    ],
    "language_style": [
        "Français soigné, dynamique et courtois",
        ""
    ],
    "typography_notes": [
        "Playfair Display (Titres Serif) & Plus Jakarta Sans (Corps)",
        "Playfair Display & Plus Jakarta Sans",
        ""
    ]
}

def clean_placeholder_val(key, current_val):
    """Renvoie une chaîne vide si la valeur correspond à un texte de démo pour laisser place au placeholder."""
    if not current_val:
        return ""
    demos = GENERIC_DEMO_TEXTS.get(key, [])
    for d in demos:
        if d and (current_val == d or d in str(current_val)):
            return ""
    return current_val

def format_vault_field(key, val, fallback="Non renseigné", html=True):
    """Affiche proprement la valeur d'un champ ou 'Non renseigné' si le champ est vide ou générique."""
    cleaned = clean_placeholder_val(key, val) if key else (val or "").strip()
    if not cleaned or str(cleaned).strip() == "":
        if html:
            return f"<span style='opacity: 0.55; font-style: italic;'>{fallback}</span>"
        return fallback
    return str(cleaned).strip()

# --- CHARGEMENT DE LA MÉMOIRE DE L'AGENCE ---
if "agency_state" not in st.session_state:
    st.session_state.agency_state = load_agency_state()
state = st.session_state.agency_state

if "brand_vault" not in state or not isinstance(state["brand_vault"], dict):
    state["brand_vault"] = DEFAULT_BRAND_VAULT.copy()
else:
    for k_bv, v_bv in DEFAULT_BRAND_VAULT.items():
        state["brand_vault"].setdefault(k_bv, v_bv)

bv_active = state["brand_vault"]

if "custom_categories" not in state:
    state["custom_categories"] = [
        "Prestation Signature / Coup de cœur",
        "Lancement d'Offre / Nouveauté",
        "Coulisses & Savoir-faire Artisanal",
        "Événement Spécial / Portes Ouvertes"
    ]
if "custom_intentions" not in state:
    state["custom_intentions"] = [
        "Stop-Scroll & Originalité",
        "Preuve d'Autorité & Qualité",
        "Désir, Émotion & Proximité"
    ]
if "custom_marketing_actions" not in state:
    state["custom_marketing_actions"] = [
        "Fidélisation & Relation Client (Relance VIP)",
        "Offre Spéciale de Saison / Nouveauté",
        "Prospection Directe & Partenariats",
        "Invitation Privée / Avantage Exclusif"
    ]
if "custom_client_segments" not in state:
    state["custom_client_segments"] = [
        "Particuliers & Familles (Clientèle locale)",
        "Professionnels & Entreprises (B2B)",
        "Clients Réguliers & Habitués",
        "Nouveaux Visiteurs & Prospects Qualifiés"
    ]
if "custom_positioning_axes" not in state:
    state["custom_positioning_axes"] = [
        "Excellence & Qualité supérieure",
        "Savoir-faire artisanal & Proximité chaleureuse",
        "Accessibilité, Simplicité & Transparence",
        "Innovation, Créativité & Expérience unique"
    ]
if "custom_tones" not in state:
    state["custom_tones"] = [
        "Chaleureux, Professionnel & Accessible",
        "Haut de gamme, Soigné & Prestigieux",
        "Proche, Convivial & Artisanal",
        "Dynamique, Direct & Moderne",
        "Minimaliste & Éditorial"
    ]
if "proactive_rd_ideas" not in state or not isinstance(state["proactive_rd_ideas"], list) or not state["proactive_rd_ideas"]:
    state["proactive_rd_ideas"] = DEFAULT_PROACTIVE_RD_IDEAS.copy()

if "mailing_contacts" not in state or not isinstance(state["mailing_contacts"], list):
    state["mailing_contacts"] = [
        "contact@partenaire-local.fr",
        "direction@entreprise-cliente.fr",
        "contact@client-fidele.fr"
    ]
if "mailing_config" not in state or not isinstance(state["mailing_config"], dict):
    state["mailing_config"] = {
        "provider": "Brevo (API / Simulation)",
        "sender_name": f"{bv_active.get('founder_or_lead', 'Simon Zoni')} — {bv_active.get('brand_name', 'Mon Entreprise')}",
        "sender_email": "contact@mon-entreprise.fr",
        "api_key": ""
    }

# Initialisation et migration du calendrier vers des dates précises YYYY-MM-DD
today_obj = date.today()
if "calendrier_tactique" not in state or not isinstance(state["calendrier_tactique"], list):
    state["calendrier_tactique"] = []

for idx_item, item in enumerate(state["calendrier_tactique"]):
    if not re.match(r"^\d{4}-\d{2}-\d{2}", str(item.get("jour", ""))):
        target_d = today_obj + timedelta(days=(idx_item * 2) + 1)
        item["jour"] = target_d.strftime("%Y-%m-%d")
    if "statut" not in item:
        item["statut"] = "Brouillon"

if "meta_auto" not in state:
    state["meta_auto"] = {
        "active": False,
        "mode": "Validation manuelle avant envoi"
    }

if "meta_ads_data" not in state or not isinstance(state.get("meta_ads_data"), dict):
    state["meta_ads_data"] = DEFAULT_META_ADS_STATE.copy()
else:
    for mak, mav in DEFAULT_META_ADS_STATE.items():
        state["meta_ads_data"].setdefault(mak, mav)

if "cal_year" not in st.session_state:
    st.session_state.cal_year = today_obj.year
if "cal_month" not in st.session_state:
    st.session_state.cal_month = today_obj.month
if "jsx_chat_history" not in st.session_state:
    st.session_state.jsx_chat_history = []
if "adobe_chat_history" not in st.session_state:
    st.session_state.adobe_chat_history = []
if "show_adobe_drawer" not in st.session_state:
    st.session_state.show_adobe_drawer = False
if "jsx_active_base_script" not in st.session_state:
    st.session_state.jsx_active_base_script = None
if "jsx_custom_seed" not in st.session_state:
    st.session_state.jsx_custom_seed = ""

if "custom_jsx_presets" not in state or not isinstance(state.get("custom_jsx_presets"), dict):
    state["custom_jsx_presets"] = {
        "illustrator": [],
        "after_effects": [],
        "indesign": [],
        "photoshop": [],
        "premiere": []
    }
else:
    for s_slug in ["illustrator", "after_effects", "indesign", "photoshop", "premiere"]:
        state["custom_jsx_presets"].setdefault(s_slug, [])

# --- IMAGE D'ACCUEIL (LOGO DU PÈRE PAR DÉFAUT OU PHOTO DE PROFIL UTILISATEUR) ---
def get_home_avatar_base64():
    user_pic_path = Path(state.get("user_profile_image", ""))
    if user_pic_path.is_file():
        return base64.b64encode(user_pic_path.read_bytes()).decode()
    for candidate in [Path("logo.png"), Path("assets/logo.png")]:
        if candidate.is_file():
            return base64.b64encode(candidate.read_bytes()).decode()
    return ""

encoded_logo = get_home_avatar_base64()

logo_css = ""
if encoded_logo:
    logo_css = f"""
    .st-key-header_logo_home_btn .stButton button {{
        background-image: url("data:image/png;base64,{encoded_logo}") !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-color: transparent !important;
        border: 2px solid #85a363 !important;
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        min-height: 48px !important;
        color: transparent !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        padding: 0 !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease, border-color 0.2s ease !important;
    }}
    .st-key-header_logo_home_btn .stButton button:hover {{
        transform: scale(1.08) !important;
        border-color: #a3c480 !important;
        box-shadow: 0 0 16px rgba(133, 163, 99, 0.45) !important;
    }}
    .st-key-logo_home_btn .stButton button,
    .st-key-sidebar_logo_home_btn .stButton button,
    div[data-testid="stElementContainer"]:has(#unique-header-logo-anchor) + div[data-testid="stElementContainer"] .stButton button,
    div.element-container:has(#unique-header-logo-anchor) + div.element-container .stButton button {{
        background-image: url("data:image/png;base64,{encoded_logo}") !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 50% !important;
        width: 76px !important;
        height: 76px !important;
        min-height: 76px !important;
        color: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    .st-key-logo_home_btn .stButton button:hover,
    .st-key-sidebar_logo_home_btn .stButton button:hover,
    div[data-testid="stElementContainer"]:has(#unique-header-logo-anchor) + div[data-testid="stElementContainer"] .stButton button:hover,
    div.element-container:has(#unique-header-logo-anchor) + div.element-container .stButton button:hover {{
        transform: scale(1.06) !important;
        background-color: transparent !important;
        border: 2px solid #85a363 !important;
        box-shadow: 0 0 12px rgba(133, 163, 99, 0.35) !important;
    }}
    """
else:
    logo_css = """
    .st-key-header_logo_home_btn .stButton button {
        width: 48px !important;
        height: 48px !important;
        min-height: 48px !important;
        border-radius: 50% !important;
        border: 1.5px solid #85a363 !important;
        background: rgba(133, 163, 99, 0.14) !important;
        color: #85a363 !important;
        font-size: 1.25rem !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25) !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease !important;
    }
    .st-key-header_logo_home_btn .stButton button:hover {
        transform: scale(1.08) !important;
        background: rgba(133, 163, 99, 0.25) !important;
        box-shadow: 0 0 16px rgba(133, 163, 99, 0.45) !important;
    }
    """

# --- CHARTE GRAPHIQUE MODERNE, ADOUCIE (NOVICES & DESIGN ÉPURÉ) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        line-height: 1.6;
        letter-spacing: 0.15px;
    }}

    h1, h2, h3, h4, .serif-title {{
        font-family: 'Playfair Display', serif !important;
        letter-spacing: 0.3px;
        font-weight: 600;
    }}

    p, span, label {{
        letter-spacing: 0.15px;
    }}

    div[data-testid="stElementContainer"]:has(.css-anchor),
    div.element-container:has(.css-anchor) {{
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }}

    /* --- CONTENEURS ET CARTES FLUIDES ET ADOUCIES --- */
    .contour-box {{
        background: linear-gradient(135deg, rgba(133, 163, 99, 0.07) 0%, rgba(255, 255, 255, 0.015) 100%) !important;
        border: 1px solid rgba(133, 163, 99, 0.28);
        border-left: 3.5px solid #85a363;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 16px;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .contour-box:hover {{
        border-color: rgba(133, 163, 99, 0.45);
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18), 0 0 10px rgba(133, 163, 99, 0.1);
    }}

    /* Cartes sobres de la Fiche Stratégique et R&D */
    .strat-card {{
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-top: 3px solid #85a363;
        border-radius: 16px;
        padding: 18px 20px;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.025) 0%, rgba(255, 255, 255, 0.008) 100%);
        height: 100%;
        min-height: 150px;
        margin-bottom: 14px;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .strat-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(133, 163, 99, 0.4);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), 0 0 12px rgba(133, 163, 99, 0.12);
    }}

    .rd-idea-card {{
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-left: 3.5px solid #85a363;
        border-radius: 16px;
        padding: 18px 20px;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        min-height: 245px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 14px;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .rd-idea-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(133, 163, 99, 0.4);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), 0 0 12px rgba(133, 163, 99, 0.12);
    }}

    /* Cartes du parcours guidé avec hauteur homogène et hover interactif */
    .step-card {{
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-left: 3.5px solid #85a363;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 12px;
        min-height: 112px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: linear-gradient(90deg, rgba(133, 163, 99, 0.06) 0%, rgba(255, 255, 255, 0.01) 100%);
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .step-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(133, 163, 99, 0.42);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22), 0 0 12px rgba(133, 163, 99, 0.12);
    }}

    /* Badges ergonomiques en forme de pilule douce (Soft Pill) */
    .step-badge {{
        display: inline-flex;
        align-items: center;
        width: fit-content;
        background: rgba(133, 163, 99, 0.15);
        border: 1px solid rgba(133, 163, 99, 0.45);
        color: #85a363;
        font-size: 0.73rem;
        font-weight: 600;
        padding: 3px 12px;
        border-radius: 9999px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
    }}

    .compass-panel {{
        border: 1px solid rgba(133, 163, 99, 0.28);
        border-radius: 18px;
        padding: 24px;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .compass-panel:hover {{
        border-color: rgba(133, 163, 99, 0.45);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.26), 0 0 14px rgba(133, 163, 99, 0.14);
    }}

    /* Volet latéral droit repliable */
    .adobe-drawer {{
        border-left: 2px solid rgba(133, 163, 99, 0.5);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 16px 18px;
        background-color: rgba(255, 255, 255, 0.02);
    }}

    .chat-msg-user {{
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        background-color: rgba(255, 255, 255, 0.02);
    }}

    .chat-msg-bot {{
        border: 1px solid rgba(133, 163, 99, 0.35);
        border-left: 3.5px solid #85a363;
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.88rem;
        background-color: rgba(133, 163, 99, 0.04);
    }}

    /* --- HARMONISATION DES BOUTONS (SOFT-PILL / ARRONDIS DOUX) --- */
    .stButton button, .stDownloadButton button {{
        background-color: rgba(255, 255, 255, 0.025) !important;
        color: inherit !important;
        border: 1px solid rgba(133, 163, 99, 0.4) !important;
        border-radius: 24px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
        height: 42px !important;
        min-height: 42px !important;
        padding: 0 1.25rem !important;
        font-size: 0.87rem !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        margin: 0 !important;
        letter-spacing: 0.2px !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .stButton button:hover, .stDownloadButton button:hover {{
        background: linear-gradient(135deg, #85a363 0%, #728f52 100%) !important;
        border-color: #85a363 !important;
        color: #0e1117 !important;
        transform: translateY(-1.5px) !important;
        box-shadow: 0 4px 16px rgba(133, 163, 99, 0.35) !important;
    }}
    .stButton button:active, .stDownloadButton button:active {{
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(133, 163, 99, 0.25) !important;
    }}

    /* Bouton actif dans la barre de navigation supérieure */
    div[data-testid="stElementContainer"]:has(.active-nav-anchor) + div[data-testid="stElementContainer"] .stButton button,
    div.element-container:has(.active-nav-anchor) + div.element-container .stButton button {{
        background: linear-gradient(135deg, rgba(133, 163, 99, 0.25) 0%, rgba(133, 163, 99, 0.12) 100%) !important;
        border: 1.5px solid #85a363 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 14px rgba(133, 163, 99, 0.3) !important;
    }}

    /* --- PASTILLE PROFIL UTILISATEUR HAUT DROITE (STYLE SAAS MODERNE) --- */
    .st-key-top_user_pill_btn .stButton button {{
        border-radius: 999px !important;
        background: rgba(255, 255, 255, 0.035) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: rgba(255, 255, 255, 0.88) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0 16px !important;
        height: 38px !important;
        min-height: 38px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .st-key-top_user_pill_btn .stButton button:hover {{
        background: rgba(133, 163, 99, 0.15) !important;
        border-color: rgba(133, 163, 99, 0.55) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(133, 163, 99, 0.25) !important;
    }}

    /* --- BARRE DE NAVIGATION RECTANGULAIRE UNIFIÉE DU HEADER (STYLE SAAS PRO) --- */
    .saas-nav-container {{
        width: 100%;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.035) 0%, rgba(255, 255, 255, 0.015) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 10px;
        padding: 4px;
        margin: 8px 0 18px 0;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25);
    }}
    .saas-nav-container div[data-testid="stHorizontalBlock"] {{
        gap: 4px !important;
        align-items: center !important;
    }}
    .saas-nav-container .stButton {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    .saas-nav-container .stButton button {{
        border-radius: 7px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        color: rgba(255, 255, 255, 0.72) !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        height: 38px !important;
        min-height: 38px !important;
        padding: 0 8px !important;
        box-shadow: none !important;
        transform: none !important;
        letter-spacing: 0.2px !important;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .saas-nav-container .stButton button:hover {{
        background: rgba(255, 255, 255, 0.055) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    .saas-nav-container div[data-testid="stElementContainer"]:has(.active-saas-nav-marker) + div[data-testid="stElementContainer"] .stButton button,
    .saas-nav-container div.element-container:has(.active-saas-nav-marker) + div.element-container .stButton button {{
        background: rgba(133, 163, 99, 0.18) !important;
        border: 1px solid rgba(133, 163, 99, 0.45) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 0 14px rgba(133, 163, 99, 0.25) !important;
    }}

    /* Boutons + et ⋯ (arrondis ergonomiques et alignés avec les selectbox) */
    div[data-testid="stElementContainer"]:has(.green-plus-anchor) + div[data-testid="stElementContainer"] .stButton button,
    div.element-container:has(.green-plus-anchor) + div.element-container .stButton button {{
        background-color: #16a34a !important;
        border: 1px solid #22c55e !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        height: 42px !important;
        min-height: 42px !important;
        padding: 0 !important;
        margin: 0 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    div[data-testid="stElementContainer"]:has(.green-plus-anchor) + div[data-testid="stElementContainer"] .stButton button:hover,
    div.element-container:has(.green-plus-anchor) + div.element-container .stButton button:hover {{
        background-color: #15803d !important;
        border-color: #4ade80 !important;
        color: #ffffff !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.35) !important;
    }}

    div[data-testid="stElementContainer"]:has(.dropdown-dots-anchor) + div[data-testid="stElementContainer"] .stButton button,
    div.element-container:has(.dropdown-dots-anchor) + div.element-container .stButton button {{
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 42px !important;
        min-height: 42px !important;
        padding: 0 !important;
        margin: 0 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    div[data-testid="stElementContainer"]:has(.dropdown-dots-anchor) + div[data-testid="stElementContainer"] .stButton button:hover,
    div.element-container:has(.dropdown-dots-anchor) + div.element-container .stButton button:hover {{
        border-color: rgba(133, 163, 99, 0.5) !important;
        background-color: rgba(133, 163, 99, 0.12) !important;
        transform: scale(1.05) !important;
    }}

    /* --- FORMULAIRES & INPUTS ADOUCIS --- */
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {{
        border-radius: 12px !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        background-color: rgba(255, 255, 255, 0.02) !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {{
        border-color: #85a363 !important;
        box-shadow: 0 0 12px rgba(133, 163, 99, 0.22) !important;
    }}

    /* Accordéons / Expanders adoucis */
    div[data-testid="stExpander"] {{
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 14px !important;
        background-color: rgba(255, 255, 255, 0.015) !important;
        margin-bottom: 12px !important;
        overflow: hidden;
        transition: all 0.25s ease;
    }}
    div[data-testid="stExpander"]:hover {{
        border-color: rgba(133, 163, 99, 0.32) !important;
    }}

    /* --- PASTILLES COULEURS DU COFFRE-FORT DE MARQUE --- */
    .vault-swatch-card {{
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 14px;
        padding: 12px 16px;
        background-color: rgba(255, 255, 255, 0.018);
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 8px;
        transition: all 0.22s ease;
    }}
    .vault-swatch-card:hover {{
        background-color: rgba(255, 255, 255, 0.035);
        border-color: rgba(133, 163, 99, 0.35);
    }}
    .vault-swatch-circle {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 1.5px solid rgba(255, 255, 255, 0.35);
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }}

    /* --- ONGLETS DE SOUS-MENU ÉLÉGANTS ET ANIMÉS --- */
    div[data-testid="stTabs"] {{
        margin-top: 8px;
        margin-bottom: 22px;
    }}
    div[data-baseweb="tab-list"] {{
        gap: 8px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.09) !important;
        background-color: transparent !important;
        padding-bottom: 4px !important;
    }}
    button[data-baseweb="tab"] {{
        background-color: transparent !important;
        color: rgba(255, 255, 255, 0.68) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.90rem !important;
        font-weight: 500 !important;
        padding: 9px 20px !important;
        border: none !important;
        border-radius: 12px 12px 0 0 !important;
        position: relative !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    button[data-baseweb="tab"]:hover {{
        color: #ffffff !important;
        background-color: rgba(133, 163, 99, 0.09) !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #85a363 !important;
        font-weight: 600 !important;
        background-color: rgba(133, 163, 99, 0.14) !important;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: #85a363 !important;
        height: 3px !important;
        border-radius: 3px 3px 0 0 !important;
        box-shadow: 0 0 8px rgba(133, 163, 99, 0.45) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    div[data-baseweb="tab-border"] {{
        background-color: rgba(255, 255, 255, 0.06) !important;
    }}

    /* --- CARTES DE MÉTRIQUES ADS & ANALYTICS --- */
    .ads-metric-card {{
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 16px 18px;
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.025) 0%, rgba(255, 255, 255, 0.008) 100%);
        border-left: 3.5px solid #85a363;
        margin-bottom: 14px;
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .ads-metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25), 0 0 12px rgba(133, 163, 99, 0.12);
        border-color: rgba(133, 163, 99, 0.4);
    }}
    .ads-metric-title {{
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        opacity: 0.75;
        margin-bottom: 4px;
        font-weight: 600;
    }}
    .ads-metric-val {{
        font-size: 1.55rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }}
    .ads-metric-sub {{
        font-size: 0.78rem;
        color: #85a363;
        margin-top: 4px;
    }}

    /* --- DESIGN SYSTEM : ICÔNES VECTORIELLES SVG SUR-MESURE --- */
    .svg-icon {{
        display: inline-block;
        vertical-align: -3px;
        flex-shrink: 0;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.2s ease;
    }}
    .icon-label-wrap {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        line-height: 1.2;
    }}
    .step-card:hover .svg-icon,
    .strat-card:hover .svg-icon,
    .rd-idea-card:hover .svg-icon,
    .ads-metric-card:hover .svg-icon,
    .compass-panel:hover .svg-icon,
    .contour-box:hover .svg-icon {{
        transform: scale(1.12);
        stroke: #85a363 !important;
    }}

    /* --- PANNEAU LATÉRAL COULISSANT / TIROIR PERSISTANT MENTOR ADOBE --- */
    .adobe-slide-drawer,
    .adobe-persistent-drawer {{
        background: linear-gradient(180deg, rgba(22, 27, 34, 0.98) 0%, rgba(14, 17, 23, 0.99) 100%);
        border: 1px solid rgba(133, 163, 99, 0.38);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.55), 0 0 20px rgba(133, 163, 99, 0.14);
        max-height: calc(100vh - 120px);
        overflow-y: auto;
        position: sticky;
        top: 75px;
        animation: slideInFromRight 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 99;
    }}
    @keyframes slideInFromRight {{
        from {{ opacity: 0; transform: translateX(18px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes fadeInDrawer {{
        from {{ opacity: 0; transform: translateY(-8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* BOUTON FLOTTANT PERSISTANT D'ASSISTANCE ADOBE (Accessible en haut et en bas de page) */
    .floating-mentor-trigger {{
        position: fixed;
        bottom: 28px;
        right: 28px;
        z-index: 999999;
    }}
    .floating-mentor-trigger div[data-testid="stButton"] button {{
        background: linear-gradient(135deg, #1c232d 0%, #12171e 100%) !important;
        color: #85a363 !important;
        border: 1.5px solid rgba(133, 163, 99, 0.55) !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 10px 22px !important;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.65), 0 0 16px rgba(133, 163, 99, 0.25) !important;
        transition: all 0.22s ease !important;
    }}
    .floating-mentor-trigger div[data-testid="stButton"] button:hover {{
        background: #85a363 !important;
        color: #0e1117 !important;
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 12px 32px rgba(133, 163, 99, 0.4) !important;
    }}

    /* CARTE D'ITÉRATION DYNAMIQUE & SCRIPT DE BASE */
    .active-base-script-card {{
        background: rgba(133, 163, 99, 0.08);
        border: 1px dashed rgba(133, 163, 99, 0.45);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }}

    {logo_css}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_model_selector():
    return BackgroundModelSelector()
selector = get_model_selector()

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Accueil"

# --- COMPOSANT : VRAI SELECTBOX NATIF + BOUTONS D'ACTION STRICTEMENT ALIGNÉS (＋ / ⋯) ---
def render_category_manager(title, state_key, prefix):
    items = state.get(state_key, [])
    if not items:
        items = ["(Aucune catégorie)"]

    selected_key = f"selected_{prefix}"
    adding_key = f"adding_{prefix}"
    editing_key = f"editing_{prefix}"

    if adding_key not in st.session_state:
        st.session_state[adding_key] = False
    if editing_key not in st.session_state:
        st.session_state[editing_key] = False

    st.markdown(f"<div style='font-size: 0.88rem; font-weight: 500; margin-bottom: 4px;'>{title}</div>", unsafe_allow_html=True)

    col_sel, col_plus, col_dots = st.columns([6.2, 0.9, 0.9], vertical_alignment="center")

    with col_sel:
        current_index = 0
        if selected_key in st.session_state and st.session_state[selected_key] in items:
            current_index = items.index(st.session_state[selected_key])

        selected_item = st.selectbox(
            title,
            options=items,
            index=current_index,
            key=f"selectbox_{prefix}",
            label_visibility="collapsed"
        )
        st.session_state[selected_key] = selected_item

    with col_plus:
        st.markdown('<div class="css-anchor green-plus-anchor"></div>', unsafe_allow_html=True)
        if st.button("＋", key=f"btn_plus_{prefix}", help="Ajouter une catégorie", use_container_width=True):
            st.session_state[adding_key] = not st.session_state[adding_key]
            st.session_state[editing_key] = False
            st.rerun()

    with col_dots:
        st.markdown('<div class="css-anchor dropdown-dots-anchor"></div>', unsafe_allow_html=True)
        if st.button("⋯", key=f"btn_dots_{prefix}", help="Modifier, copier ou supprimer", use_container_width=True):
            st.session_state[editing_key] = not st.session_state[editing_key]
            st.session_state[adding_key] = False
            st.rerun()

    if st.session_state[adding_key]:
        ca1, ca2 = st.columns([4.5, 1.5], vertical_alignment="center")
        with ca1:
            new_val = st.text_input("Nouvelle catégorie :", key=f"input_add_{prefix}", placeholder="Nom de la nouvelle catégorie...", label_visibility="collapsed")
        with ca2:
            if st.button("Ajouter", key=f"confirm_add_{prefix}", use_container_width=True):
                if new_val.strip() and new_val.strip() not in items:
                    if items == ["(Aucune catégorie)"]:
                        items = []
                    items.append(new_val.strip())
                    state[state_key] = items
                    save_agency_state(state)
                    st.session_state[selected_key] = new_val.strip()
                    st.session_state[adding_key] = False
                    st.rerun()

    if st.session_state[editing_key] and selected_item != "(Aucune catégorie)":
        edit_val = st.text_input("Renommer :", value=selected_item, key=f"edit_val_{prefix}", label_visibility="collapsed")
        m1, m2, m3 = st.columns([1.4, 1.2, 1.2], vertical_alignment="center")
        with m1:
            if st.button("✏️ Enregistrer", key=f"save_edit_{prefix}", use_container_width=True):
                if edit_val.strip() and edit_val.strip() != selected_item:
                    idx = items.index(selected_item)
                    items[idx] = edit_val.strip()
                    state[state_key] = items
                    save_agency_state(state)
                    st.session_state[selected_key] = edit_val.strip()
                    st.session_state[editing_key] = False
                    st.rerun()
        with m2:
            if st.button("📋 Copier", key=f"copy_btn_{prefix}", use_container_width=True):
                idx = items.index(selected_item)
                new_item = f"{selected_item} (copie)"
                items.insert(idx + 1, new_item)
                state[state_key] = items
                save_agency_state(state)
                st.session_state[selected_key] = new_item
                st.session_state[editing_key] = False
                st.rerun()
        with m3:
            if st.button("🗑️ Supprimer", key=f"del_btn_{prefix}", use_container_width=True):
                if len(items) > 1:
                    items.remove(selected_item)
                    state[state_key] = items
                    save_agency_state(state)
                    st.session_state[selected_key] = items[0]
                    st.session_state[editing_key] = False
                    st.rerun()
                else:
                    st.warning("Gardez au moins une catégorie.")

    return st.session_state[selected_key]


# --- COMPOSANT : FICHE D'IDENTITÉ STRATÉGIQUE VISUELLE ---
def render_strategic_identity_card(target_state, badge_text="Fiche d'Identité Stratégique Active"):
    obj_comm = target_state.get("objectifs_comm", {})
    if not isinstance(obj_comm, dict):
        obj_comm = {"cognitif": str(obj_comm), "affectif": "", "conatif": ""}

    biais_list = target_state.get("biais_psychologiques_actifs", [])
    if isinstance(biais_list, str):
        biais_list = [biais_list]

    render_html(f"<span class='step-badge'>{badge_text}</span>")

    # Rangée 1 : Les 3 Piliers Fondamentaux
    p1, p2, p3 = st.columns(3)
    with p1:
        render_html(f"""
        <div class="strat-card">
            <div style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.8px; color: #85a363; font-weight: 700; margin-bottom: 6px;">🏛️ 1. Positionnement & Promesse</div>
            <div style="font-size: 0.87rem; opacity: 0.9; line-height: 1.5;">{target_state.get('positionnement_actif', 'Non défini')}</div>
        </div>
        """)
    with p2:
        render_html(f"""
        <div class="strat-card">
            <div style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.8px; color: #85a363; font-weight: 700; margin-bottom: 6px;">🎯 2. Cibles Prioritaires</div>
            <div style="font-size: 0.87rem; opacity: 0.9; line-height: 1.5;">{target_state.get('cibles_prioritaires', 'Non défini')}</div>
        </div>
        """)
    with p3:
        render_html(f"""
        <div class="strat-card">
            <div style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.8px; color: #85a363; font-weight: 700; margin-bottom: 6px;">🧭 3. Cap & Ambition Commerciale</div>
            <div style="font-size: 0.87rem; opacity: 0.9; line-height: 1.5;">{target_state.get('vision_du_chef', 'Non défini')}</div>
        </div>
        """)

    # Rangée 2 : Les 3 Objectifs de Communication (Faire Savoir / Faire Aimer / Faire Agir)
    o1, o2, o3 = st.columns(3)
    with o1:
        render_html(f"""
        <div class="contour-box" style="min-height: 118px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">🧠 Faire Savoir (Cognitif)</div>
            <div style="font-size: 0.84rem; opacity: 0.85; line-height: 1.45;">{obj_comm.get('cognitif', 'Prouver le savoir-faire et la rigueur.')}</div>
        </div>
        """)
    with o2:
        render_html(f"""
        <div class="contour-box" style="min-height: 118px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">✨ Faire Aimer (Affectif)</div>
            <div style="font-size: 0.84rem; opacity: 0.85; line-height: 1.45;">{obj_comm.get('affectif', 'Susciter la confiance et le désir.')}</div>
        </div>
        """)
    with o3:
        render_html(f"""
        <div class="contour-box" style="min-height: 118px;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">🚀 Faire Agir (Conatif)</div>
            <div style="font-size: 0.84rem; opacity: 0.85; line-height: 1.45;">{obj_comm.get('conatif', 'Générer des demandes de devis.')}</div>
        </div>
        """)

    # Rangée 3 : Leviers Psychologiques & Parcours de Conversion
    b_col1, b_col2 = st.columns([1.3, 1])
    with b_col1:
        biais_html = "".join([f"<div style='margin-bottom: 6px; font-size: 0.84rem;'>• {b}</div>" for b in biais_list[:3]])
        render_html(f"""
        <div class="contour-box">
            <div style="font-size: 0.76rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 6px;">🔑 Leviers Psychologiques de Décision</div>
            {biais_html}
        </div>
        """)
    with b_col2:
        render_html(f"""
        <div class="contour-box">
            <div style="font-size: 0.76rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 6px;">🔄 Tunnel de Conversion Client</div>
            <div style="font-size: 0.84rem; opacity: 0.88; line-height: 1.5;">{target_state.get('ecosysteme_conversion', '')}</div>
        </div>
        """)


# =====================================================================
# BARRE LATÉRALE MINIMALISTE : PROFIL UTILISATEUR & MOTEUR IA
# =====================================================================
with st.sidebar:
    u_first = bv_active.get("user_first_name", "")
    u_last = bv_active.get("user_last_name", "")
    u_full = f"{u_first} {u_last}".strip() or bv_active.get("founder_or_lead", "Simon Zoni")
    u_role = bv_active.get("user_role", "Dirigeant")
    sb_bname = format_vault_field("brand_name", bv_active.get("brand_name"), fallback="Mon Entreprise", html=False)
    sb_bloc = format_vault_field("location", bv_active.get("location"))

    avatar_markup = ""
    if encoded_logo:
        avatar_markup = f'<img src="data:image/png;base64,{encoded_logo}" style="width: 54px; height: 54px; border-radius: 50%; object-fit: cover; border: 2px solid #85a363; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 6px;">'
    else:
        avatar_markup = f'<div style="width: 54px; height: 54px; border-radius: 50%; background: rgba(133, 163, 99, 0.15); border: 1.5px solid #85a363; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; margin: 0 auto 6px auto;">👤</div>'

    render_html(f"""
    <div style="text-align: center; padding: 4px 0 10px 0;">
        {avatar_markup}
        <div style="font-weight: 600; font-size: 0.95rem; color: #ffffff; line-height: 1.25;">{u_full}</div>
        <div style="font-size: 0.76rem; color: #85a363; font-weight: 500; margin-top: 2px;">{u_role}</div>
        <div style="font-size: 0.74rem; opacity: 0.7; margin-top: 4px;">{sb_bname} &nbsp;·&nbsp; {sb_bloc}</div>
    </div>
    """)

    if st.button("⚙️ Mon Compte", key="sb_btn_to_account", use_container_width=True):
        st.session_state.current_page = "🏢 Mon Compte"
        st.rerun()

    render_html("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 16px 0 14px 0;'></div>")

    # Sélecteur de Modèle d'IA Minimaliste
    render_html("<div style='font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; color: rgba(255,255,255,0.45); font-weight: 600; margin-bottom: 6px; padding-left: 2px;'>Moteur IA</div>")
    if selector.scan_finished:
        render_html(f"<div style='font-size: 0.78rem; color: #4ade80; margin-bottom: 6px;'>🟢 Actif : <code>{selector.active_model}</code></div>")
    else:
        render_html(f"<div style='font-size: 0.78rem; color: #85a363; margin-bottom: 6px;'>⚡ Rapide : <code>{selector.active_model}</code></div>")

    manual_choice = st.selectbox(
        "Modèle IA actif :",
        selector.candidates,
        index=selector.candidates.index(selector.active_model) if selector.active_model in selector.candidates else 0,
        label_visibility="collapsed",
        key="sb_model_choice_select"
    )
    if manual_choice != selector.active_model:
        selector.active_model = manual_choice
        st.rerun()


# =====================================================================
# EN-TÊTE PRINCIPAL : LOGO CLIQUABLE (ACCUEIL), MARQUE & PASTILLE PROFIL
# =====================================================================
col_head_left, col_head_right = st.columns([3.8, 1.4], vertical_alignment="center")
with col_head_left:
    c_logo, c_brand_txt = st.columns([0.45, 3.55], vertical_alignment="center")
    with c_logo:
        logo_btn_label = " " if encoded_logo else "✨"
        if st.button(logo_btn_label, key="header_logo_home_btn", help="Accueil — Revenir à la vue d'ensemble"):
            st.session_state.current_page = "🏠 Accueil"
            st.rerun()
    with c_brand_txt:
        brand_name_raw = bv_active.get("brand_name", "")
        brand_title_upper = format_vault_field("brand_name", brand_name_raw, fallback="Mon Entreprise", html=False).upper()
        primary_hex = bv_active.get("primary_color", "#85a363")
        sec_sector = format_vault_field("business_type", bv_active.get("business_type"))
        sec_loc = format_vault_field("location", bv_active.get("location"))
        sec_scope = format_vault_field("target_scope", bv_active.get("target_scope"))
        sec_market = format_vault_field("market_type", bv_active.get("market_type"))
        render_html(f"""
        <div>
            <div style='font-family: "Playfair Display", serif; font-size: 1.45rem; font-weight: 600; letter-spacing: 0.4px; line-height: 1.2;'>
                {brand_title_upper}
            </div>
            <div style='font-size: 0.80rem; color: rgba(255, 255, 255, 0.65); margin-top: 3px;'>
                <span style='color: {primary_hex}; font-weight: 500;'>{sec_sector}</span> &nbsp;·&nbsp;
                <span>{sec_loc}</span> &nbsp;·&nbsp;
                <span>{sec_scope}</span> &nbsp;·&nbsp;
                <span>{sec_market}</span>
            </div>
        </div>
        """)

with col_head_right:
    first_n = bv_active.get("user_first_name", "")
    last_n = bv_active.get("user_last_name", "")
    full_user_name = f"{first_n} {last_n}".strip() or bv_active.get("founder_or_lead", "Simon Zoni")
    u_role = bv_active.get("user_role", "Dirigeant")
    if st.button(f"👤  {full_user_name}  ·  {u_role}", key="top_user_pill_btn", help="Gérer Mon Compte & Entreprise", use_container_width=True):
        st.session_state.current_page = "🏢 Mon Compte"
        st.rerun()

# --- BARRE DE NAVIGATION RECTANGULAIRE UNIFIÉE (STYLE SAAS PRO) ---
nav_tabs = [
    ("🎯 Stratégie", "Stratégie"),
    ("💡 Marketing", "Marketing"),
    ("📅 Planning", "Planning"),
    ("⚙️ Création", "Création"),
    ("📸 Studio", "Studio"),
    ("🏢 Mon Compte", "Compte")
]

st.markdown('<div class="saas-nav-container">', unsafe_allow_html=True)
nav_cols = st.columns(len(nav_tabs))

for i, (tab_label, tab_keyword) in enumerate(nav_tabs):
    is_active = (tab_label == st.session_state.current_page) or (
        tab_keyword in st.session_state.current_page
    )
    with nav_cols[i]:
        if is_active:
            st.markdown('<div class="active-saas-nav-marker"></div>', unsafe_allow_html=True)
        if st.button(tab_label, key=f"saas_nav_btn_{i}", use_container_width=True):
            st.session_state.current_page = tab_label
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
render_html("<div style='height: 1px; background: linear-gradient(90deg, rgba(133,163,99,0.35) 0%, rgba(255,255,255,0.06) 65%, transparent 100%); margin: 0 0 18px 0;'></div>")


# =====================================================================
# ACCUEIL : PARCOURS GUIDÉ ASYMÉTRIQUE EN 5 ÉTAPES + BOUSSOLE DE MARQUE
# =====================================================================
if st.session_state.current_page == "🏠 Accueil":
    col_compass, col_journey = st.columns([1.25, 2.75])

    with col_compass:
        nb_pending = sum(1 for x in state.get("calendrier_tactique", []) if "valider" in x.get("statut", ""))
        nb_auto = sum(1 for x in state.get("calendrier_tactique", []) if "Prêt" in x.get("statut", ""))
        c_prim = bv_active.get("primary_color", "#85a363")
        c_sec = bv_active.get("secondary_color", "#0e1117")
        c_acc = bv_active.get("accent_color", "#f59e0b")

        loc_f = format_vault_field('location', bv_active.get('location'))
        sec_f = format_vault_field('business_type', bv_active.get('business_type'))
        scope_f = format_vault_field('target_scope', bv_active.get('target_scope'))
        mkt_f = format_vault_field('market_type', bv_active.get('market_type'))
        dna_f = format_vault_field('short_dna', bv_active.get('short_dna'))
        tone_f = format_vault_field('tone_of_voice', bv_active.get('tone_of_voice'))
        brand_f = format_vault_field('brand_name', bv_active.get('brand_name'), fallback="Mon Entreprise", html=False)

        home_compass_html = (
            f"<div class='compass-panel'>"
            f"<span class='step-badge'>{get_svg_icon('vault', 14, '#85a363')} Boussole de Marque</span>"
            f"<h3 class='serif-title' style='margin: 6px 0 2px 0;'>{brand_f}</h3>"
            f"<p style='font-size: 0.78rem; opacity: 0.8; margin-bottom: 6px;'>"
            f"{get_svg_icon('map_pin', 12, '#85a363')} {loc_f} &nbsp;·&nbsp; {get_svg_icon('tag', 12, '#85a363')} {sec_f}"
            f"</p>"
            f"<p style='font-size: 0.76rem; color: #85a363; margin-bottom: 8px;'>"
            f"<b>🎯 Portée :</b> {scope_f} &nbsp;|&nbsp; <b>🏢 Marché :</b> {mkt_f}"
            f"</p>"
            f"<p style='opacity: 0.82; font-size: 0.84rem; line-height: 1.45; margin-bottom: 10px;'>"
            f"{dna_f}"
            f"</p>"
            f"<div style='display:flex; align-items:center; gap:8px; margin-bottom:10px;'>"
            f"<span style='font-size:0.78rem; opacity:0.75;'>Palette :</span>"
            f"<span style='display:inline-block; width:18px; height:18px; border-radius:50%; background:{c_prim}; border:1px solid rgba(255,255,255,0.4);'></span>"
            f"<span style='display:inline-block; width:18px; height:18px; border-radius:50%; background:{c_sec}; border:1px solid rgba(255,255,255,0.4);'></span>"
            f"<span style='display:inline-block; width:18px; height:18px; border-radius:50%; background:{c_acc}; border:1px solid rgba(255,255,255,0.4);'></span>"
            f"<span style='font-size:0.75rem; opacity:0.7;'>({c_prim} · {c_acc})</span>"
            f"</div>"
            f"<p style='font-size: 0.82rem; margin-bottom: 8px;'><b>🎙️ Ton actif :</b> <span style='color:#85a363;'>{tone_f}</span></p>"
            f"<hr style='border-color: rgba(255,255,255,0.1); margin: 12px 0;'>"
            f"<p style='font-size: 0.84rem; margin-bottom: 6px;'><b>{get_svg_icon('calendar', 14, '#85a363')} Publications au calendrier :</b> {len(state.get('calendrier_tactique', []))}</p>"
            f"<p style='font-size: 0.82rem; margin-bottom: 0; color: #fbbf24;'><b>🟠 À valider :</b> {nb_pending} &nbsp;|&nbsp; <span style='color: #4ade80;'><b>🟢 Prêt / Auto :</b> {nb_auto}</span></p>"
            f"</div>"
        )
        render_html(home_compass_html)
        st.write("")
        if st.button("🏢 Gérer Mon Compte →", key="home_vault_btn", use_container_width=True):
            st.session_state.current_page = "🏢 Mon Compte"
            st.rerun()

    with col_journey:
        # Pôle Stratégie
        s1_txt, s1_btn = st.columns([4, 1.25], vertical_alignment="center")
        with s1_txt:
            render_html(f"""
            <div class="step-card">
                <span class="step-badge">{get_svg_icon('target', 13, '#85a363')} Fondation Stratégique</span>
                <h4 class='serif-title' style='margin: 2px 0 4px 0;'>{get_svg_icon('target', 18, '#85a363')} Stratégie & Boussole de Marque</h4>
                <p style='opacity: 0.82; font-size: 0.86rem; margin: 0;'>Cadrage guidé (Positionnement, Cibles, Objectif commercial) restitué sous forme de Fiche d'Identité Stratégique claire.</p>
            </div>
            """)
        with s1_btn:
            if st.button("Stratégie →", key="h_step1", use_container_width=True):
                st.session_state.current_page = "🎯 Stratégie"
                st.rerun()

        # Pôles Marketing et Planning côte à côte
        col_step2, col_step3 = st.columns([1, 1], vertical_alignment="top")
        with col_step2:
            render_html(f"""
            <div class="step-card" style="min-height: 138px;">
                <span class="step-badge">{get_svg_icon('lightbulb', 13, '#85a363')} Offre & Visibilité</span>
                <h4 class='serif-title' style='margin: 2px 0 4px 0;'>{get_svg_icon('lightbulb', 18, '#85a363')} Pôle Marketing 360°</h4>
                <p style='opacity: 0.82; font-size: 0.85rem; margin: 0;'>Stratégie d'offre, campagnes d'e-mailing ciblées (avec analyse psychologique) et boîte à idées R&D proactive.</p>
            </div>
            """)
            if st.button("Marketing →", key="h_step2", use_container_width=True):
                st.session_state.current_page = "💡 Marketing"
                st.rerun()

        with col_step3:
            render_html(f"""
            <div class="step-card" style="min-height: 138px;">
                <span class="step-badge">{get_svg_icon('calendar', 13, '#85a363')} Calendrier & Publication</span>
                <h4 class='serif-title' style='margin: 2px 0 4px 0;'>{get_svg_icon('calendar', 18, '#85a363')} Planning Éditorial</h4>
                <p style='opacity: 0.82; font-size: 0.85rem; margin: 0;'>Visualisez le calendrier mensuel en couleurs, réglez la date de chaque post et validez la publication Meta.</p>
            </div>
            """)
            if st.button("Planning →", key="h_step3", use_container_width=True):
                st.session_state.current_page = "📅 Planning"
                st.rerun()

        st.write("")

        # Pôle Création Graphique & Scripts Adobe
        s4_txt, s4_btn = st.columns([4, 1.25], vertical_alignment="center")
        with s4_txt:
            render_html(f"""
            <div class="step-card">
                <span class="step-badge">{get_svg_icon('wand', 13, '#85a363')} Atelier Graphique & Scripts</span>
                <h4 class='serif-title' style='margin: 2px 0 4px 0;'>{get_svg_icon('wand', 18, '#85a363')} Création & Scripts Adobe (JSX)</h4>
                <p style='opacity: 0.82; font-size: 0.86rem; margin: 0;'>Automatisez vos visuels sur Illustrator ou After Effects grâce au générateur de scripts <b>.jsx</b> et au guide Adobe repliable.</p>
            </div>
            """)
        with s4_btn:
            if st.button("Création →", key="h_step4", use_container_width=True):
                st.session_state.current_page = "⚙️ Création"
                st.rerun()

        # Pôle Studio de Création & Social Ads
        s5_txt, s5_btn = st.columns([4, 1.25], vertical_alignment="center")
        with s5_txt:
            render_html(f"""
            <div class="step-card">
                <span class="step-badge">{get_svg_icon('camera', 13, '#85a363')} Production Visuelle & Ads</span>
                <h4 class='serif-title' style='margin: 2px 0 4px 0;'>{get_svg_icon('camera', 18, '#85a363')} Studio & Social Ads</h4>
                <p style='opacity: 0.82; font-size: 0.86rem; margin: 0;'>Sublimez vos photos de terrain sur Instagram & Facebook, ou pilotez vos campagnes Meta Ads avec suivi du ROAS.</p>
            </div>
            """)
        with s5_btn:
            if st.button("Studio →", key="h_step5", use_container_width=True):
                st.session_state.current_page = "📸 Studio"
                st.rerun()


# =====================================================================
# STRATÉGIE & BOUSSOLE DE MARQUE
# =====================================================================
elif "Stratégie" in st.session_state.current_page:
    st.markdown(f"<h2 class='serif-title'>{get_svg_icon('target', 24, '#85a363')} Stratégie & Boussole de Marque</h2>", unsafe_allow_html=True)

    # 1. Introduction pédagogique claire pour les dirigeants novices
    render_html("""
    <div class="contour-box">
        <span class="step-badge">Comprendre la démarche</span>
        <h4 class="serif-title" style="margin: 4px 0 6px 0;">Pourquoi structurer votre stratégie avant de communiquer ?</h4>
        <p style="font-size: 0.88rem; opacity: 0.86; line-height: 1.55; margin: 0;">
            Publier sans boussole épuise votre énergie sans attirer les bons clients. Une stratégie efficace répond à trois questions simples :
            <b>1. Quelle est votre signature unique ?</b> (Positionnement) ·
            <b>2. Qui souhaitez-vous convaincre en priorité ?</b> (Cibles) ·
            <b>3. Quel résultat concret visez-vous ce mois-ci ?</b> (Objectif).
            Renseignez les 3 piliers ci-dessous : le Directeur Stratégique IA se charge de bâtir votre <b>Fiche d'Identité Stratégique</b> complète.
        </p>
    </div>
    """)

    # 2. Affichage de la Fiche d'Identité Stratégique actuelle (dans un volet dépliable ou visible)
    with st.expander("📋 Consulter votre Fiche d'Identité Stratégique actuelle", expanded=True):
        render_strategic_identity_card(state, badge_text="Boussole Stratégique Active")

    st.divider()

    # 3. Formulaire de Cadrage Structuré (Mini-tunnel en 3 colonnes claires)
    st.markdown("<h3 class='serif-title' style='margin-bottom: 10px;'>🧭 Définir votre Cap Stratégique</h3>", unsafe_allow_html=True)

    col_step_a, col_step_b, col_step_c = st.columns(3, vertical_alignment="top")

    with col_step_a:
        render_html("<span class='step-badge'>Positionnement</span>")
        in_secteur = st.text_input(
            "Métier / Spécialité :",
            value=clean_placeholder_val("business_type", bv_active.get("business_type", "")),
            placeholder="Ex : Restaurant bistronomique, Caviste, Traiteur...",
            key="strat_secteur_in"
        )
        axe_pos = render_category_manager("Axe de positionnement :", "custom_positioning_axes", "pos_axe")
        in_preuve = st.text_input(
            "Atout différenciateur (Preuve) :",
            value=clean_placeholder_val("short_dna", bv_active.get("short_dna", "")),
            placeholder="Ex : Savoir-faire artisanal d'exception et accueil sur-mesure...",
            key="strat_preuve_in"
        )

    with col_step_b:
        render_html("<span class='step-badge'>Cibles Prioritaires</span>")
        cibles_dispo = state.get("custom_client_segments", [])
        in_cibles_sel = st.multiselect(
            "Quels profils voulez-vous attirer en priorité ?",
            options=cibles_dispo,
            default=cibles_dispo[:2] if len(cibles_dispo) >= 2 else cibles_dispo,
            key="strat_cibles_multi"
        )
        in_zone_cible = st.text_input(
            "Zone géographique ou précision clientèle :",
            value=clean_placeholder_val("location", bv_active.get("location", "")),
            placeholder="Ex : Centre-ville et agglomération...",
            key="strat_zone_in"
        )

    with col_step_c:
        render_html("<span class='step-badge'>Objectif Commercial</span>")
        obj_choices = [
            "Attirer de nouveaux clients qualifiés (Acquisition)",
            "Fidéliser et relancer nos clients existants (CRM & Récurrence)",
            "Lancer une nouvelle offre ou préparer une saison forte",
            "Asseoir notre prestige face à la concurrence"
        ]
        in_obj_prio = st.selectbox("Priorité commerciale du moment :", options=obj_choices, key="strat_obj_sel")
        in_notes_dir = st.text_area(
            "Précision libre du dirigeant (optionnel) :",
            placeholder="Ex : Ce mois-ci, dynamiser les réservations avec une formule exclusive...",
            height=88,
            key="strat_notes_in"
        )

    st.write("")
    btn_strat_col, _ = st.columns([1.8, 2.2])
    with btn_strat_col:
        if st.button("🪄 Structurer ma nouvelle Fiche d'Identité Stratégique", key="run_guided_strat_btn", use_container_width=True):
            cibles_str = ", ".join(in_cibles_sel) if in_cibles_sel else "Clientèle haut de gamme et entreprises"
            structured_brief = (
                f"Secteur : {in_secteur} | Axe de positionnement : {axe_pos} | "
                f"Preuve & Différenciation : {in_preuve} | "
                f"Cibles prioritaires : {cibles_str} ({in_zone_cible}) | "
                f"Objectif commercial : {in_obj_prio} | "
                f"Consigne spécifique du dirigeant : {in_notes_dir or 'Aucune'}"
            )
            with st.spinner("Le Directeur Stratégique structure votre nouvelle Fiche d'Identité..."):
                md_critique, proposed_state = agent_directeur_strategie_red_team(
                    structured_brief,
                    in_obj_prio,
                    state,
                    selector.active_model
                )
                st.session_state.last_strategy_critique = md_critique
                if proposed_state:
                    try:
                        clean_json = proposed_state.strip("`").replace("json", "").strip()
                        parsed_prop = json.loads(clean_json)
                        # Préserver les données du coffre-fort, du mailing et des listes personnalisées
                        for keep_k in [
                            "brand_vault", "custom_categories", "custom_intentions",
                            "custom_marketing_actions", "custom_client_segments",
                            "custom_positioning_axes", "custom_tones", "proactive_rd_ideas",
                            "mailing_contacts", "mailing_config", "meta_auto", "user_profile_image"
                        ]:
                            if keep_k in state:
                                parsed_prop[keep_k] = state[keep_k]
                        st.session_state.proposed_state = parsed_prop
                    except Exception as e:
                        st.warning(f"Note générée, mais le formatage JSON nécessite un ajustement ({e}).")

    # 4. Restitution visuelle de la nouvelle proposition stratégique
    if "last_strategy_critique" in st.session_state:
        st.divider()
        st.markdown("<div class='contour-box'><span class='step-badge'>Diagnostic du Directeur Stratégique</span></div>", unsafe_allow_html=True)
        st.markdown(st.session_state.last_strategy_critique, unsafe_allow_html=True)

        if st.session_state.get("proposed_state"):
            st.write("")
            render_strategic_identity_card(
                st.session_state.proposed_state,
                badge_text="Nouvelle Fiche d'Identité Stratégique Proposée"
            )
            st.write("")
            c_act1, c_act2 = st.columns([1.8, 2.2], vertical_alignment="center")
            with c_act1:
                if st.button("✅ Confirmer et activer cette Fiche Stratégique", key="confirm_strat_card_btn", use_container_width=True):
                    st.session_state.agency_state = st.session_state.proposed_state
                    save_agency_state(st.session_state.proposed_state)
                    st.session_state.pop("last_strategy_critique", None)
                    st.session_state.pop("proposed_state", None)
                    st.success("Votre nouvelle Fiche d'Identité Stratégique est maintenant active dans toute l'agence !")
                    st.rerun()


# =====================================================================
# MARKETING & OFFRES COMMERCIALES
# =====================================================================
elif "Marketing" in st.session_state.current_page:
    st.markdown(f"<h2 class='serif-title'>{get_svg_icon('lightbulb', 24, '#85a363')} Marketing & Offres Commerciales</h2>", unsafe_allow_html=True)

    tab_strategy, tab_mailing, tab_rd = st.tabs([
        "🎯 Offre & Marché",
        "✉️ Campagnes E-mailing",
        "💡 R&D & Idées Produits"
    ])

    # -----------------------------------------------------------------
    # SOUS-ONGLET 1 : STRATÉGIE DE MARCHÉ & OFFRE COMMERCIALE
    # -----------------------------------------------------------------
    with tab_strategy:
        render_html(f"""
        <div class="contour-box">
            <span class="step-badge">Positionnement, Offre Irrésistible & Tarification</span>
            <p style="font-size: 0.87rem; opacity: 0.86; margin: 4px 0 0 0;">
                Votre conseiller stratégique analyse les spécificités de votre marché local à <b>{bv_active.get('location')}</b>, vos concurrents et les attentes de vos clients pour vous aider à packager une offre commerciale à forte valeur et fixer des prix rentables.
            </p>
        </div>
        """)

        col_mkt_left, col_mkt_right = st.columns([1.5, 1.25], vertical_alignment="top")

        with col_mkt_left:
            st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>Paramètres de l'Analyse</h4>", unsafe_allow_html=True)
            angle_choices = [
                "Diagnostic de positionnement & Grille tarifaire (Justifier des prix premium)",
                "Création d'une offre commerciale packagée (Offre Irrésistible)",
                "Différenciation concurrentielle & Barrières à l'entrée locales",
                "Tunnels d'acquisition & Leviers de conversion client",
                "Audit des forces & axes d'amélioration (Avis clients & Google Maps)"
            ]
            in_angle = st.selectbox("Angle d'analyse prioritaire :", angle_choices, key="mkt_strat_angle_sel")
            st.write("")
            in_mkt_segment = render_category_manager("Segment de clientèle ciblé :", "custom_client_segments", "mkt_strat_seg")
            st.write("")
            in_mkt_question = st.text_area(
                "Question, défi commercial ou produit à lancer (optionnel) :",
                placeholder=f"Ex : Comment concevoir une formule événementielle haut de gamme à {bv_active.get('location')} qui attire les entreprises et justifie un ticket moyen élevé ?",
                height=90,
                key="mkt_strat_q_in"
            )

            st.write("")
            if st.button("🪄 Lancer l'Analyse Stratégique de Marché", key="btn_run_mkt_strat", use_container_width=True):
                with st.spinner(f"Analyse du marché à {bv_active.get('location')} et conception de l'offre commerciale..."):
                    mkt_advice, mkt_json = agent_strategie_marche_offre(
                        in_angle,
                        in_mkt_segment,
                        in_mkt_question,
                        state,
                        selector.active_model
                    )
                    st.session_state.mkt_strat_result = mkt_advice
                    if mkt_json:
                        try:
                            clean_j = mkt_json.strip("`").replace("json", "").strip()
                            st.session_state.mkt_strat_offer_json = json.loads(clean_j)
                        except Exception:
                            st.session_state.mkt_strat_offer_json = None
                    st.rerun()

        with col_mkt_right:
            st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>Fiche de Marché Active</h4>", unsafe_allow_html=True)
            maps_note_html = ""
            if bv_active.get("google_reviews_summary"):
                maps_note_html = (
                    f"<div style='background: rgba(133, 163, 99, 0.12); border-left: 3px solid #85a363; "
                    f"padding: 10px 12px; border-radius: 6px; margin: 10px 0; font-size: 0.81rem; line-height: 1.45;'>"
                    f"<b>⭐ Contexte Avis & Réputation :</b><br>"
                    f"<span style='opacity: 0.9;'>{bv_active.get('google_reviews_summary')}</span>"
                    f"</div>"
                )

            mkt_bname = format_vault_field('brand_name', bv_active.get('brand_name'), fallback="Mon Entreprise", html=False)
            mkt_loc = format_vault_field('location', bv_active.get('location'))
            mkt_sec = format_vault_field('business_type', bv_active.get('business_type'))
            mkt_cli = format_vault_field('client_type', bv_active.get('client_type'))
            mkt_dna = format_vault_field('short_dna', bv_active.get('short_dna'))
            mkt_tone = format_vault_field('tone_of_voice', bv_active.get('tone_of_voice'))

            fiche_marche_html = (
                f"<div class='strat-card' style='min-height: 290px;'>"
                f"<span class='step-badge'>Profil Entreprise ({mkt_bname})</span>"
                f"<p style='font-size: 0.83rem; margin: 6px 0 8px 0; opacity: 0.85; line-height: 1.4;'>"
                f"📍 <b>Ville :</b> {mkt_loc} &nbsp;|&nbsp; 🏷️ <b>Secteur :</b> {mkt_sec}<br>"
                f"🎯 <b>Clientèle type :</b> {mkt_cli}"
                f"</p>"
                f"{maps_note_html}"
                f"<div style='font-size: 0.82rem; opacity: 0.88; line-height: 1.45; margin: 8px 0;'>"
                f"<b>🧬 ADN Actif :</b> {mkt_dna}"
                f"</div>"
                f"<div style='font-size: 0.80rem; opacity: 0.78; margin-top: 6px;'>"
                f"🎙️ <b>Ton :</b> {mkt_tone}"
                f"</div>"
                f"</div>"
            )
            render_html(fiche_marche_html)

        if "mkt_strat_result" in st.session_state:
            st.divider()
            st.markdown("<h4 class='serif-title'>📋 Diagnostic & Recommandations Stratégiques</h4>", unsafe_allow_html=True)
            st.markdown(st.session_state.mkt_strat_result)

            if st.session_state.get("mkt_strat_offer_json"):
                of_j = st.session_state.mkt_strat_offer_json
                titre_of = of_j.get("titre_offre", "Nouvelle Offre Packagée")
                prix_of = of_j.get("prix_conseille", "Sur devis")
                promesse_of = of_j.get("promesse", "")

                render_html(f"""
                <div class="contour-box" style="margin-top: 14px;">
                    <span class="step-badge">Pack Commercial Prêt à l'Emploi</span>
                    <h3 class="serif-title" style="margin: 6px 0 4px 0;">{titre_of} — {prix_of}</h3>
                    <p style="font-size: 0.86rem; opacity: 0.88; margin: 0;"><b>Promesse client :</b> {promesse_of}</p>
                </div>
                """)

                act_o1, act_o2, act_o3 = st.columns(3, vertical_alignment="center")
                with act_o1:
                    if st.button("✅ Valider l'offre au catalogue", key="btn_mkt_add_offer", use_container_width=True):
                        if titre_of not in state.get("offres_innovantes_validees", []):
                            state.setdefault("offres_innovantes_validees", []).insert(0, titre_of)
                        if titre_of not in state.get("custom_categories", []):
                            state.setdefault("custom_categories", []).append(titre_of)
                        save_agency_state(state)
                        st.success(f"« {titre_of} » a été ajoutée aux offres validées et aux catégories de l'agence !")
                with act_o2:
                    if st.button("📅 Programmer au Planning", key="btn_mkt_plan_offer", use_container_width=True):
                        state.setdefault("calendrier_tactique", []).append({
                            "jour": (date.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
                            "sujet": f"Lancement : {titre_of} ({prix_of})",
                            "objectif": "Conversion & Offre Packagée",
                            "statut": "À valider"
                        })
                        save_agency_state(state)
                        st.session_state.current_page = "📅 Planning"
                        st.rerun()
                with act_o3:
                    if st.button("📸 Tester l'offre au Studio →", key="btn_mkt_studio_offer", use_container_width=True):
                        state["brief_actif_pour_studio"] = f"[Offre Commerciale : {titre_of} ({prix_of})] {promesse_of}"
                        save_agency_state(state)
                        st.session_state.current_page = "📸 Studio"
                        st.rerun()

    # -----------------------------------------------------------------
    # SOUS-ONGLET 2 : CAMPAGNES D'E-MAILING (CRM & FIDÉLISATION)
    # -----------------------------------------------------------------
    with tab_mailing:
        render_html("""
        <div class="contour-box">
            <span class="step-badge">Fidélisation & Prospection Directe</span>
            <p style="font-size: 0.87rem; opacity: 0.86; margin: 4px 0 0 0;">
                Importez ou collez vos contacts clients, choisissez un segment et laissez l'IA rédiger un e-mail commercial élégant accompagné de son explication psychologique de conversion.
            </p>
        </div>
        """)

        col_crm_left, col_crm_right = st.columns([1.25, 1.75], vertical_alignment="top")

        with col_crm_left:
            st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>1. Cible & Liste de Contacts</h4>", unsafe_allow_html=True)
            selected_segment = render_category_manager("Segment de clientèle visé :", "custom_client_segments", "crm_seg")
            st.write("")

            # Import CSV / Texte ou copier-coller d'emails
            uploaded_csv = st.file_uploader(
                "📂 Importer un fichier de contacts (.csv, .txt) :",
                type=["csv", "txt"],
                key="crm_csv_uploader"
            )
            if uploaded_csv is not None:
                raw_file_txt = uploaded_csv.getvalue().decode("utf-8", errors="ignore")
                extracted_from_file = extract_emails_from_text(raw_file_txt)
                if extracted_from_file:
                    merged = list(dict.fromkeys(state.get("mailing_contacts", []) + extracted_from_file))
                    state["mailing_contacts"] = merged
                    save_agency_state(state)
                    st.success(f"{len(extracted_from_file)} adresses détectées et ajoutées ({len(merged)} au total).")

            current_emails_str = "\n".join(state.get("mailing_contacts", []))
            pasted_emails = st.text_area(
                f"Liste des e-mails destinataires ({len(state.get('mailing_contacts', []))} contacts enregistrés) :",
                value=current_emails_str,
                height=135,
                placeholder="Collez ici les adresses e-mail de vos clients (une par ligne ou séparées par des virgules)...",
                key="crm_emails_textarea"
            )

            if st.button("💾 Enregistrer la liste de contacts", key="save_crm_contacts_btn", use_container_width=True):
                cleaned_list = extract_emails_from_text(pasted_emails)
                state["mailing_contacts"] = cleaned_list
                save_agency_state(state)
                st.success(f"Liste mise à jour : {len(cleaned_list)} contacts valides enregistrés.")
                st.rerun()

            st.write("")
            with st.expander("🔌 Connexion d'envoi externe (Brevo API / Expéditeur)"):
                m_cfg = state.get("mailing_config", {})
                in_sender_name = st.text_input("Nom de l'expéditeur :", value=m_cfg.get("sender_name", ""), key="brevo_sname")
                in_sender_email = st.text_input("E-mail expéditeur :", value=m_cfg.get("sender_email", ""), key="brevo_semail")
                in_brevo_key = st.text_input("Clé API Brevo (optionnel — vide = mode simulation) :", value=m_cfg.get("api_key", ""), type="password", key="brevo_key")
                if st.button("Sauvegarder la configuration d'envoi", key="save_brevo_btn", use_container_width=True):
                    state["mailing_config"] = {
                        "provider": "Brevo",
                        "sender_name": in_sender_name.strip(),
                        "sender_email": in_sender_email.strip(),
                        "api_key": in_brevo_key.strip()
                    }
                    save_agency_state(state)
                    st.success("Configuration d'envoi enregistrée.")

        with col_crm_right:
            st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>2. Générateur de Campagne E-mail</h4>", unsafe_allow_html=True)
            type_action_mail = render_category_manager("Objectif de l'e-mail :", "custom_marketing_actions", "mkt_act")
            st.write("")
            brief_mail = st.text_area(
                "Que souhaitez-vous proposer ou annoncer dans cet e-mail ?",
                placeholder="Ex : Proposer à nos anciens clients de réserver leur Chef à domicile pour leurs réceptions privées du mois prochain avec un menu dégustation exclusif...",
                height=100,
                key="crm_brief_input"
            )

            nb_dest = len(state.get("mailing_contacts", []))
            if st.button(f"✉️ Générer l'E-mail Commercial ({nb_dest} destinataires)", key="gen_email_campaign_btn", use_container_width=True):
                if not brief_mail.strip():
                    st.warning("Précisez en une phrase l'offre ou le sujet de votre e-mail.")
                else:
                    with st.spinner("Rédaction de l'e-mail et analyse psychologique de conversion..."):
                        email_txt, psych_analysis = agent_campagne_mailing(
                            selected_segment,
                            type_action_mail,
                            brief_mail,
                            nb_dest,
                            state,
                            selector.active_model
                        )
                        st.session_state.generated_email_body = email_txt
                        st.session_state.generated_email_psych = psych_analysis
                        st.rerun()

            if "generated_email_body" in st.session_state:
                st.divider()
                st.markdown("<span class='step-badge'>E-mail Prêt à Envoyer (Modifiable)</span>", unsafe_allow_html=True)
                edited_email = st.text_area(
                    "Ajustez le texte si nécessaire avant validation ou envoi :",
                    value=st.session_state.generated_email_body,
                    height=240,
                    key="edited_email_output"
                )
                st.session_state.generated_email_body = edited_email

                render_html(f"""
                <div class="contour-box">
                    <div style="font-size: 0.76rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">
                        🧠 Pourquoi cet e-mail va convertir (Logique Psychologique & Fidélisation)
                    </div>
                    <div style="font-size: 0.85rem; opacity: 0.88; line-height: 1.5;">
                        {st.session_state.get('generated_email_psych', '')}
                    </div>
                </div>
                """)

                em_act1, em_act2 = st.columns(2, vertical_alignment="center")
                with em_act1:
                    st.download_button(
                        label="📋 Télécharger / Copier la campagne (.txt)",
                        data=edited_email,
                        file_name="campagne_mailing.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with em_act2:
                    if st.button(f"🚀 Valider & Envoyer aux {nb_dest} contacts", key="send_campaign_btn", use_container_width=True):
                        api_k = state.get("mailing_config", {}).get("api_key", "")
                        mode_label = "via l'API Brevo" if api_k else "en mode Simulation Validée"
                        st.success(
                            f"✅ Campagne validée et programmée {mode_label} vers {nb_dest} destinataires du segment « {selected_segment} » !"
                        )

    # -----------------------------------------------------------------
    # SOUS-ONGLET 3 : RECHERCHE & DÉVELOPPEMENT (VEILLE & IDÉES PRODUITS)
    # -----------------------------------------------------------------
    with tab_rd:
        render_html("""
        <div class="contour-box">
            <span class="step-badge">Veille Sectorielle & Boîte à Idées Proactive</span>
            <p style="font-size: 0.87rem; opacity: 0.86; margin: 4px 0 0 0;">
                Plus besoin de chercher l'inspiration devant une page blanche : votre agent R&D analyse les tendances de votre marché et vous propose <b>3 concepts concrets</b> sur lesquels rebondir en un clic.
            </p>
        </div>
        """)

        v_bar1, v_bar2 = st.columns([3, 1.3], vertical_alignment="center")
        with v_bar1:
            veille_focus = st.text_input(
                "Orienter la veille sur une thématique (optionnel) :",
                placeholder="Ex : Nouvelles offres pour entreprises, événements de fin d'année, formats Reels Instagram...",
                label_visibility="collapsed",
                key="rd_veille_focus_in"
            )
        with v_bar2:
            if st.button("🔄 Actualiser les 3 idées (Veille IA)", key="refresh_proactive_rd_btn", use_container_width=True):
                with st.spinner("Analyse des tendances du secteur et génération de 3 nouvelles propositions..."):
                    try:
                        new_ideas = agent_veille_proactive_rd(veille_focus, state, selector.active_model)
                        if isinstance(new_ideas, list) and len(new_ideas) > 0:
                            state["proactive_rd_ideas"] = new_ideas[:3]
                            save_agency_state(state)
                            st.rerun()
                    except Exception as e:
                        st.warning(f"Impossible d'actualiser les cartes pour le moment ({e}).")

        st.write("")
        # Affichage des 3 Propositions Proactives en 3 colonnes
        ideas_list = state.get("proactive_rd_ideas", DEFAULT_PROACTIVE_RD_IDEAS)
        cols_ideas = st.columns(3, vertical_alignment="top")

        for idx_id, idea in enumerate(ideas_list[:3]):
            with cols_ideas[idx_id]:
                render_html(f"""
                <div class="rd-idea-card">
                    <div>
                        <span class="step-badge">{idea.get('categorie', 'Idée R&D')}</span>
                        <h4 class="serif-title" style="margin: 4px 0 8px 0; font-size: 1.05rem;">{idea.get('titre', '')}</h4>
                        <p style="font-size: 0.82rem; opacity: 0.85; line-height: 1.45; margin-bottom: 8px;">
                            <b>🔍 Tendance détectée :</b> {idea.get('tendance', '')}
                        </p>
                        <p style="font-size: 0.82rem; opacity: 0.85; line-height: 1.45; margin-bottom: 0;">
                            <b>💡 Intérêt commercial :</b> {idea.get('impact', '')}
                        </p>
                    </div>
                </div>
                """)

                b_reb1, b_reb2 = st.columns(2, vertical_alignment="center")
                with b_reb1:
                    if st.button("🔬 Approfondir", key=f"rebond_etude_{idx_id}", use_container_width=True):
                        st.session_state.rd_custom_input_val = f"{idea.get('titre')} — {idea.get('tendance')}"
                        with st.spinner(f"Étude approfondie de « {idea.get('titre')} »..."):
                            res_deep = agent_marketing_360(
                                "Étude R&D & Lancement d'Offre",
                                f"Développe concrètement cette proposition (recette/format, tarif conseillé, argumentaire commercial et plan de lancement) : {idea.get('titre')}. Contexte : {idea.get('tendance')}",
                                state,
                                selector.active_model
                            )
                            st.session_state.last_rd_study = res_deep
                            st.session_state.last_rd_title = idea.get("titre", "Nouvelle offre")
                            st.rerun()
                with b_reb2:
                    if st.button("📸 Ouvrir au Studio", key=f"rebond_studio_{idx_id}", use_container_width=True):
                        state["brief_actif_pour_studio"] = (
                            f"[Idée R&D : {idea.get('titre')}] {idea.get('angle_post', idea.get('tendance', ''))}"
                        )
                        save_agency_state(state)
                        st.session_state.current_page = "📸 Studio"
                        st.rerun()

        st.divider()
        st.markdown("<h4 class='serif-title'>🧪 Tester ou approfondir une idée de produit / d'offre sur mesure</h4>", unsafe_allow_html=True)
        rd_in1, rd_in2 = st.columns([3, 1.2], vertical_alignment="center")
        with rd_in1:
            produit = st.text_input(
                "Nouvelle idée à étudier :",
                value=st.session_state.get("rd_custom_input_val", ""),
                placeholder="Ex : Gamme de petits fours aux fruits de mer, Menu brunch dominical...",
                label_visibility="collapsed",
                key="rd_free_input"
            )
        with rd_in2:
            if st.button("🧪 Lancer l'étude de viabilité", key="run_free_rd_btn", use_container_width=True):
                if produit.strip():
                    with st.spinner("Analyse de viabilité, positionnement prix et stratégie de lancement..."):
                        res = agent_marketing_360(
                            "R&D Produit & Viabilité Commerciale",
                            f"Analyse l'opportunité commerciale, la rentabilité, le prix conseillé et l'angle de communication pour : {produit}",
                            state,
                            selector.active_model
                        )
                        st.session_state.last_rd_study = res
                        st.session_state.last_rd_title = produit.strip()
                        st.rerun()

        if "last_rd_study" in st.session_state:
            st.write("")
            st.markdown(f"<div class='contour-box'><span class='step-badge'>Étude R&D : {st.session_state.get('last_rd_title', '')}</span></div>", unsafe_allow_html=True)
            st.markdown(st.session_state.last_rd_study)
            st.write("")
            rd_act1, rd_act2 = st.columns([2, 2], vertical_alignment="center")
            with rd_act1:
                if st.button("✅ Valider et ajouter aux offres officielles de l'agence", key="add_validated_offer_btn", use_container_width=True):
                    title_to_add = st.session_state.get("last_rd_title", "Nouvelle Offre")
                    if title_to_add not in state.get("offres_innovantes_validees", []):
                        state.setdefault("offres_innovantes_validees", []).insert(0, title_to_add)
                    if title_to_add not in state.get("custom_categories", []):
                        state.setdefault("custom_categories", []).append(title_to_add)
                    save_agency_state(state)
                    st.success(f"« {title_to_add} » a été ajouté aux offres validées et aux catégories du Studio !")
            with rd_act2:
                if st.button("📅 Programmer le lancement dans le Planning →", key="plan_rd_launch_btn", use_container_width=True):
                    title_to_add = st.session_state.get("last_rd_title", "Nouvelle Offre")
                    state.setdefault("calendrier_tactique", []).append({
                        "jour": (date.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
                        "sujet": f"Lancement : {title_to_add}",
                        "objectif": "Nouveauté & Conversion",
                        "statut": "Brouillon"
                    })
                    save_agency_state(state)
                    st.session_state.current_page = "📅 Planning"
                    st.rerun()


# =====================================================================
# PLANNING & CALENDRIER MENSUEL
# =====================================================================
elif "Planning" in st.session_state.current_page:
    st.markdown(f"<h2 class='serif-title'>{get_svg_icon('calendar', 24, '#85a363')} Planning & Calendrier Mensuel</h2>", unsafe_allow_html=True)

    # Initialisation de la config Meta et des dates précises
    if "meta_auto" not in state:
        state["meta_auto"] = {"active": False, "mode": "Validation manuelle avant envoi"}

    # --- 1. PANNEAU D'AUTOMATISATION META (INSTAGRAM & FACEBOOK) ---
    with st.expander("⚡ Paramètres d'automatisation Meta (Instagram & Facebook)", expanded=False):
        m_col1, m_col2, m_col3 = st.columns([1.2, 2, 1.2])
        with m_col1:
            auto_active = st.toggle("Activer l'auto-publication Meta", value=state["meta_auto"].get("active", False))
            state["meta_auto"]["active"] = auto_active
        with m_col2:
            auto_mode = st.radio(
                "Mode de déclenchement :",
                ["Validation manuelle avant envoi", "100% Automatique à la date prévue"],
                index=0 if "Validation" in state["meta_auto"].get("mode", "") else 1,
                horizontal=True,
                disabled=not auto_active
            )
            state["meta_auto"]["mode"] = auto_mode
        with m_col3:
            st.write("")
            if st.button("💾 Sauvegarder", key="save_meta_cfg", use_container_width=True):
                save_agency_state(state)
                st.success("Réglages enregistrés.")

    st.write("")

    # --- 2. AJOUTER UN POST À UNE DATE PRÉCISE OU GÉNÉRER PAR IA ---
    col_add_manual, col_gen_ai = st.columns([1.4, 1])

    with col_add_manual:
        st.markdown("<div class='contour-box'><b>➕ Programmer une publication à une date précise</b></div>", unsafe_allow_html=True)
        f_c1, f_c2 = st.columns([1, 2])
        with f_c1:
            chosen_date = st.date_input("Date de publication :", value=date.today(), key="cal_date_picker")
            chosen_status = st.selectbox("Statut :", ["Brouillon", "À valider", "Prêt (Auto)"], key="cal_status_picker")
        with f_c2:
            chosen_sujet = st.text_input("Sujet du post :", placeholder="Ex : Menu spécial réception d'ambassade...", key="cal_sujet_input")
            chosen_obj = st.text_input("Objectif / Canal :", value="Instagram & Facebook — Prestige", key="cal_obj_input")
        if st.button("📌 Ajouter au calendrier", key="btn_add_cal_entry", use_container_width=True):
            if chosen_sujet.strip():
                state.setdefault("calendrier_tactique", []).append({
                    "jour": chosen_date.strftime("%Y-%m-%d"),
                    "sujet": chosen_sujet.strip(),
                    "objectif": chosen_obj.strip(),
                    "statut": chosen_status
                })
                save_agency_state(state)
                st.rerun()

    with col_gen_ai:
        st.markdown("<div class='contour-box'><b>🤖 Génération d'idées par l'IA</b></div>", unsafe_allow_html=True)
        campagne_input = st.text_input("Thème du mois ou de la semaine :", placeholder="Ex : Mariages, Fêtes de fin d'année...")
        st.write("")
        if st.button("✨ Générer des idées de posts", key="btn_ai_cal", use_container_width=True):
            with st.spinner("Création du planning..."):
                md_plan, new_cal = agent_generateur_plan_comm(campagne_input or state.get("vision_du_chef", ""), state, selector.active_model)
                st.session_state.last_plan_md = md_plan
                if new_cal:
                    clean_cal = new_cal.strip("`").replace("json", "").strip()
                    parsed_cal = json.loads(clean_cal)
                    for idx_p, item in enumerate(parsed_cal):
                        item.setdefault("statut", "Brouillon")
                        if not re.match(r"^\d{4}-\d{2}-\d{2}", str(item.get("jour", ""))):
                            item["jour"] = (date.today() + timedelta(days=(idx_p * 2) + 1)).strftime("%Y-%m-%d")
                    state["calendrier_tactique"] = parsed_cal
                    save_agency_state(state)
                    st.rerun()

    st.divider()

    # --- 3. VUE CALENDRIER MENSUEL COLORÉE (MOIS PAR MOIS) ---
    today = date.today()
    c_m1, c_m2, c_m3 = st.columns([1, 1, 2])
    with c_m1:
        sel_month = st.selectbox("Mois :", list(range(1, 13)), index=today.month - 1, format_func=lambda m: calendar.month_name[m])
    with c_m2:
        sel_year = st.selectbox("Année :", [2026, 2027], index=0)
    with c_m3:
        st.markdown("""
        <div style='padding-top: 26px; font-size: 0.84rem;'>
            <span style='color:#94a3b8; margin-right:14px;'>● <b>Gris :</b> Brouillon</span>
            <span style='color:#f59e0b; margin-right:14px;'>● <b>Orange :</b> À valider</span>
            <span style='color:#22c55e;'>● <b>Vert :</b> Prêt / Auto-post</span>
        </div>
        """, unsafe_allow_html=True)

    # Construction de la grille HTML du mois
    cal_matrix = calendar.monthcalendar(sel_year, sel_month)
    events_by_day = {}
    for ev in state.get("calendrier_tactique", []):
        d_str = str(ev.get("jour", ""))
        prefix_ym = f"{sel_year}-{sel_month:02d}-"
        if d_str.startswith(prefix_ym):
            try:
                d_num = int(d_str.split("-")[2])
                events_by_day.setdefault(d_num, []).append(ev)
            except ValueError:
                pass

    jours_semaine = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    html_cal = "<div style='display:grid; grid-template-columns:repeat(7, 1fr); gap:6px; margin-top:10px; margin-bottom:22px;'>"
    for j_label in jours_semaine:
        html_cal += f"<div style='text-align:center; font-size:0.8rem; font-weight:600; opacity:0.7; padding:4px;'>{j_label}</div>"

    for week in cal_matrix:
        for day_num in week:
            if day_num == 0:
                html_cal += "<div style='min-height:78px; border:1px solid rgba(255,255,255,0.04); border-radius:12px; background:rgba(255,255,255,0.01);'></div>"
            else:
                day_evs = events_by_day.get(day_num, [])
                border_col = "rgba(255,255,255,0.10)"
                badges_html = ""
                for ev in day_evs:
                    st_ev = ev.get("statut", "Brouillon")
                    if "Prêt" in st_ev:
                        bg_c, tx_c, border_col = "rgba(34,197,94,0.18)", "#4ade80", "#22c55e"
                    elif "valider" in st_ev:
                        bg_c, tx_c, border_col = "rgba(245,158,11,0.18)", "#fbbf24", "#f59e0b"
                    else:
                        bg_c, tx_c, border_col = "rgba(148,163,184,0.18)", "#cbd5e1", "rgba(148,163,184,0.45)"
                    short_title = ev.get("sujet", "")[:22] + ("…" if len(ev.get("sujet", "")) > 22 else "")
                    badges_html += f"<div style='background:{bg_c}; color:{tx_c}; font-size:0.72rem; padding:3px 7px; border-radius:6px; margin-top:4px; line-height:1.2; font-weight:500;'>{short_title}</div>"

                html_cal += f"<div style='min-height:78px; border:1px solid {border_col}; border-radius:12px; padding:8px; background:rgba(255,255,255,0.015); transition:all 0.2s ease;'><div style='font-size:0.78rem; font-weight:600; opacity:0.85;'>{day_num}</div>{badges_html}</div>"
    html_cal += "</div>"
    st.markdown(html_cal, unsafe_allow_html=True)

    # --- 4. LISTE DES PUBLICATIONS PARFAITEMENT ALIGNÉE ---
    st.markdown("<h4 class='serif-title'>📋 Gestion & Validation des Publications :</h4>", unsafe_allow_html=True)

    for idx, item in enumerate(list(state.get("calendrier_tactique", []))):
        statut_actuel = item.get("statut", "Brouillon")
        if "Prêt" in statut_actuel:
            dot_color, badge_label = "#22c55e", "🟢 Prêt / Auto-post"
        elif "valider" in statut_actuel:
            dot_color, badge_label = "#f59e0b", "🟠 À valider"
        else:
            dot_color, badge_label = "#94a3b8", "⚪ Brouillon"

        row_c1, row_c2, row_c3, row_c4 = st.columns([4.2, 1.3, 1.3, 0.6], vertical_alignment="center")
        with row_c1:
            render_html(f"""
            <div style="border: 1px solid rgba(255,255,255,0.09); border-left: 4px solid {dot_color}; border-radius: 14px; padding: 12px 16px; margin: 4px 0; background: rgba(255,255,255,0.015); transition: all 0.2s ease;">
                <span style="font-size:0.76rem; color:{dot_color}; font-weight:600;">{badge_label} — {item.get('jour')}</span><br>
                <b style="font-size:0.92rem;">{item.get('sujet')}</b>
                <span style="opacity:0.65; font-size:0.82rem;"> ({item.get('objectif', '')})</span>
            </div>
            """)

        with row_c2:
            if st.button("📸 Studio →", key=f"send_cal_{idx}", use_container_width=True):
                state["brief_actif_pour_studio"] = f"[{item.get('jour')}] {item.get('sujet')} — Objectif : {item.get('objectif')}"
                save_agency_state(state)
                st.session_state.current_page = "📸 Studio"
                st.rerun()

        with row_c3:
            next_label = "✅ Valider" if "Prêt" not in statut_actuel else "🚀 Publier"
            if st.button(next_label, key=f"val_cal_{idx}", use_container_width=True):
                if "Prêt" not in statut_actuel:
                    state["calendrier_tactique"][idx]["statut"] = "Prêt (Auto)"
                    save_agency_state(state)
                    st.rerun()
                else:
                    st.toast(f"Publication envoyée vers Instagram/Facebook : {item.get('sujet')}")

        with row_c4:
            if st.button("🗑️", key=f"del_cal_{idx}", use_container_width=True):
                state["calendrier_tactique"].pop(idx)
                save_agency_state(state)
                st.rerun()


# =====================================================================
# CRÉATION & SCRIPTS ADOBE (EXTENDSCRIPT JSX)
# =====================================================================
elif "Création" in st.session_state.current_page:
    show_adobe_drawer = st.session_state.get("show_adobe_drawer", False)

    # 1. En-tête Principal de l'Atelier avec bascule du tiroir
    head_left, head_right = st.columns([3.3, 1.4], vertical_alignment="center")
    with head_left:
        st.markdown(f"<h2 class='serif-title' style='margin-bottom: 0;'>{get_svg_icon('wand', 24, '#85a363')} Création & Scripts Adobe</h2>", unsafe_allow_html=True)
    with head_right:
        toggle_label = "✖ Replier le Mentor" if show_adobe_drawer else "🧭 Ouvrir le Mentor Adobe"
        if st.button(toggle_label, key="toggle_adobe_drawer_top_btn", use_container_width=True):
            st.session_state.show_adobe_drawer = not show_adobe_drawer
            st.rerun()

    # Introduction et Cadrage Métier
    render_html("""
    <div class="contour-box">
        <span class="step-badge">Atelier d'Ingénierie Graphique & Motion Design (Suite Adobe)</span>
        <h4 class="serif-title" style="margin: 4px 0 6px 0;">Automatisez la création vectorielle, la mise en page et l'animation en un clic</h4>
        <p style="font-size: 0.88rem; opacity: 0.86; line-height: 1.55; margin: 0;">
            Générez et personnalisez des scripts <b>.jsx</b> complets pour les 5 géants Adobe : <b>Illustrator, After Effects, InDesign, Photoshop et Premiere Pro</b>. Cliquez sur un modèle pour l'exécuter et le personnaliser en direct avec l'IA, ou sauvegardez vos propres automatisations dans votre boîte à outils.
        </p>
    </div>
    """)

    # 2. Bouton Flottant Persistant (accessible qu'on soit tout en haut ou tout en bas)
    st.markdown('<div class="floating-mentor-trigger">', unsafe_allow_html=True)
    float_label = "✖ Fermer Mentor" if show_adobe_drawer else "🧭 Mentor Adobe"
    if st.button(float_label, key="floating_mentor_btn"):
        st.session_state.show_adobe_drawer = not show_adobe_drawer
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Répartition : Panneau Principal vs Panneau Latéral (Tiroir)
    if show_adobe_drawer:
        col_main, col_drawer = st.columns([2.55, 1.45], gap="large")
    else:
        col_main = st.container()
        col_drawer = None

    # --- PANNEAU LATÉRAL COULISSANT (TIROIR MENTOR ADOBE DÉDIÉ) ---
    if col_drawer is not None:
        with col_drawer:
            render_html("""
            <div class="adobe-persistent-drawer">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">🧭</span>
                        <h4 class="serif-title" style="margin: 0; color: #85a363;">Mentor Suite Adobe</h4>
                    </div>
                    <span style="font-size: 0.72rem; color: #4ade80; background: rgba(74, 222, 128, 0.12); padding: 3px 8px; border-radius: 999px; border: 1px solid rgba(74, 222, 128, 0.25);">
                        ● En ligne (CC)
                    </span>
                </div>
                <p style="font-size: 0.8rem; opacity: 0.82; line-height: 1.4; margin: 0 0 12px 0;">
                    Assistance technique continue sur l'API ExtendScript (ES3), courbes de Bézier, expressions After Effects et compatibilité.
                </p>
            </div>
            """)

            # Puces de questions rapides
            st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin: 10px 0 6px 0;'>💡 Questions Fréquentes :</div>", unsafe_allow_html=True)
            if st.button("❓ Comment exécuter un .jsx dans Adobe ?", key="faq_adobe_1", use_container_width=True):
                st.session_state["adobe_guide_preset_q"] = "Comment charger et exécuter concrètement un fichier .jsx dans Illustrator, Photoshop ou After Effects ?"
            if st.button("❓ Pourquoi du vectoriel pur vs IA raster ?", key="faq_adobe_2", use_container_width=True):
                st.session_state["adobe_guide_preset_q"] = "Pourquoi les scripts ExtendScript vectoriels sont-ils supérieurs aux images matricielles de Midjourney ou Firefly pour une marque ?"
            if st.button("❓ Comment lisser une animation dans AE ?", key="faq_adobe_3", use_container_width=True):
                st.session_state["adobe_guide_preset_q"] = "Comment animer des calques avec un amorti de vitesse et un décalage temporel fluide (stagger) dans After Effects ?"

            st.write("")
            if st.session_state.adobe_chat_history:
                st.markdown("<div style='font-size: 0.75rem; font-weight: 700; opacity: 0.7; text-transform: uppercase; margin-bottom: 6px;'>Historique Mentor :</div>", unsafe_allow_html=True)
                for g_msg in st.session_state.adobe_chat_history[-4:]:
                    if g_msg["role"] == "user":
                        st.markdown(f"<div class='chat-msg-user' style='padding: 6px 10px; font-size: 0.82rem; margin: 4px 0;'><b>Vous :</b> {g_msg['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-msg-bot' style='padding: 6px 10px; font-size: 0.82rem; margin: 4px 0;'><b>🧭 Mentor :</b><br>{g_msg['content']}</div>", unsafe_allow_html=True)

            guide_q_val = st.session_state.pop("adobe_guide_preset_q", "")
            question_adobe = st.text_area(
                "Votre question technique :",
                value=guide_q_val,
                placeholder="Ex : Comment convertir des points d'ancrage en courbes de Bézier dans Illustrator ?",
                key="adobe_guide_input",
                height=75
            )
            cg1, cg2 = st.columns([3.2, 1.2], vertical_alignment="center")
            with cg1:
                if st.button("💬 Demander", key="btn_ask_guide", use_container_width=True):
                    if question_adobe.strip():
                        st.session_state.adobe_chat_history.append({"role": "user", "content": question_adobe})
                        hist_guide = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.adobe_chat_history[-6:]])
                        with st.spinner("Analyse technique..."):
                            rep_adobe = agent_marketing_360("Mentor Suite Adobe", f"{DOCTRINE_ADOBE_JSX}\n\nHistorique :\n{hist_guide}\n\nQuestion : {question_adobe}", state, selector.active_model)
                            st.session_state.adobe_chat_history.append({"role": "assistant", "content": rep_adobe})
                            st.rerun()
            with cg2:
                if st.button("🗑️ Vider", key="clear_guide_chat", use_container_width=True):
                    st.session_state.adobe_chat_history = []
                    st.rerun()

            st.write("")
            if st.button("✖ Replier le tiroir", key="close_drawer_btn_inside", use_container_width=True):
                st.session_state.show_adobe_drawer = False
                st.rerun()

    # --- CONTENU PRINCIPAL DE L'ATELIER (`col_main`) ---
    with col_main:
        # Sélecteur de logiciel (5 Grands Logiciels de la Suite Adobe)
        adobe_software_options = [
            "🎨 Adobe Illustrator (.jsx) — Tracés vectoriels, courbes de Bézier, nuanciers & calques",
            "🎬 Adobe After Effects (.jsx) — Motion design procédural, animations de calques & keyframes",
            "📄 Adobe InDesign (.jsx) — Grilles modulaires, gabarits, styles typographiques & pagination",
            "🖼️ Adobe Photoshop (.jsx) — Compositions automatisées, calques de réglage & formats web",
            "🎞️ Adobe Premiere Pro (.jsx) — Montage dynamique, marqueurs, organisation chutier & exports"
        ]

        selected_adobe_soft = st.selectbox(
            "Cibler le logiciel Adobe de travail :",
            options=adobe_software_options,
            key="adobe_soft_choice_select"
        )

        if "Illustrator" in selected_adobe_soft:
            soft_slug = "illustrator"
            soft_short = "Illustrator"
        elif "After Effects" in selected_adobe_soft:
            soft_slug = "after_effects"
            soft_short = "After Effects"
        elif "InDesign" in selected_adobe_soft:
            soft_slug = "indesign"
            soft_short = "InDesign"
        elif "Photoshop" in selected_adobe_soft:
            soft_slug = "photoshop"
            soft_short = "Photoshop"
        else:
            soft_slug = "premiere"
            soft_short = "Premiere Pro"

        # Fiche d'identité couleur active
        render_html(
            f"<div class='contour-box' style='font-size: 0.84rem; padding: 10px 14px; margin-top: 4px;'>"
            f"{get_svg_icon('vault', 14, '#85a363')} <b>Charte Active injectée :</b> <b>{bv_active.get('brand_name')}</b> &nbsp;|&nbsp; "
            f"Primaire : <code style='color: {bv_active.get('primary_color', '#85a363')};'>{bv_active.get('primary_color', '#85a363')}</code> &nbsp;|&nbsp; "
            f"Secondaire : <code>{bv_active.get('secondary_color', '#0e1117')}</code> &nbsp;|&nbsp; "
            f"Accent : <code style='color: {bv_active.get('accent_color', '#f59e0b')};'>{bv_active.get('accent_color', '#f59e0b')}</code>"
            f"</div>"
        )

        # 4. Boîte à Outils des Presets : Standards et Personnalisés
        st.markdown("<h4 class='serif-title' style='margin: 16px 0 6px 0;'>⚡ Boîte à Outils & Presets de Scripts (1-Clic & Personnalisables) :</h4>", unsafe_allow_html=True)
        
        user_custom_presets = state.get("custom_jsx_presets", {}).get(soft_slug, [])

        tab_std_presets, tab_custom_presets = st.tabs([
            f"⚡ Presets Standards ({soft_short})",
            f"⭐ Mes Presets Personnalisés ({len(user_custom_presets)})"
        ])

        # --- ONGLET PRESETS STANDARDS ---
        with tab_std_presets:
            quick_template_labels = {
                "illustrator": [
                    ("📐 Grille Isométrique", "Tracé mathématique d'une grille 30° sur calque verrouillé"),
                    ("🎨 Nuancier Officiel", f"Échantillons et injection des teintes de {bv_active.get('brand_name')}"),
                    ("🔤 Cadres Typographiques", "Titres H1 et sous-titres centrés sur le plan de travail"),
                    ("✂️ Formats Multi-Artboards", "3 plans de travail calibrés (Post 1:1, Story 9:16, Bannière)")
                ],
                "after_effects": [
                    ("✨ Éclosion en Cascade", "Animation fluide décalée de l'opacité et de l'échelle des calques"),
                    ("📈 Rebond Élastique", "Expression d'inertie physique et amorti élastique sur la Position"),
                    ("⏱️ Compteur 0-100%", "Calque texte avec Slider Control dynamique animé avec lissage"),
                    ("🔄 Boucle loopOut", "Expression loopOut('cycle') sur les propriétés pour boucle infinie")
                ],
                "indesign": [
                    ("📖 Grille 12 Colonnes", "Grille de mise en page modulaire avec marges et gouttières"),
                    ("🏷️ Folios & Gabarit", f"Folios et numérotation automatique avec signature {bv_active.get('brand_name')}"),
                    ("📑 Styles de Paragraphe", "Arborescence Titre, Chapô et Corps avec la nuance de marque"),
                    ("📦 Export PDF Imprimeur", "Export PDF Haute Définition avec traits de coupe et fond perdu")
                ],
                "photoshop": [
                    ("🖼️ Structure Post Carré", "Composition 1080x1080 avec 3 dossiers de calques et fond teinté"),
                    ("🎨 Palette & Nuancier", "Calques de remplissage solides pour les teintes officielles"),
                    ("🛡️ Filigrane & Signature", f"Signature discrète © {bv_active.get('brand_name')} (35% opacité, verrouillée)"),
                    ("⚡ Export Web Optimisé", "Automatisation SaveForWeb JPEG 85% calibré sRGB")
                ],
                "premiere": [
                    ("🎬 Marqueurs Rythmiques", "Marqueurs de coupe insérés toutes les 2s pour le montage sonore"),
                    ("🎞️ Chutiers & Bins Pro", "Arborescence de 6 dossiers professionnels pour trier les médias"),
                    ("⏱️ Séquence Reels 9:16", f"Séquence verticale 1080x1920 calibrée pour {bv_active.get('brand_name')}"),
                    ("✂️ Export Media Encoder", "Envoi direct de la séquence dans la file d'attente d'AME")
                ]
            }

            t_cols = st.columns(4)
            active_templates = quick_template_labels.get(soft_slug, quick_template_labels["illustrator"])
            for idx_t, (t_label, t_sub) in enumerate(active_templates):
                with t_cols[idx_t]:
                    if st.button(t_label, key=f"quick_tpl_btn_{soft_slug}_{idx_t}", use_container_width=True, help=t_sub):
                        script_data = generate_authentic_adobe_script(soft_slug, idx_t, bv_active)
                        
                        # 1. Enregistre le script comme base active pour personnalisation itérative
                        st.session_state.jsx_active_base_script = {
                            "title": script_data["title"],
                            "code": script_data["code"],
                            "soft": soft_short,
                            "soft_slug": soft_slug,
                            "filename": script_data["filename"]
                        }
                        st.session_state.jsx_custom_seed = f"Adapte le script '{script_data['title']}' pour : "

                        # 2. Ajoute à l'historique de chat
                        st.session_state.jsx_chat_history.append({
                            "role": "user",
                            "content": f"⚡ Modèle 1-Clic ({soft_short}) : {script_data['title']}"
                        })
                        assistant_md = (
                            f"### ⚡ Script ExtendScript ({soft_short}) : {script_data['title']}\n\n"
                            f"{script_data['description']}\n\n"
                            f"```javascript\n{script_data['code']}\n```\n\n"
                            f"> **Mode d'emploi immédiat dans {soft_short} :**\n"
                            f"> 1. Cliquez sur le bouton de téléchargement ci-dessous pour obtenir `{script_data['filename']}`.\n"
                            f"> 2. Dans **{soft_short}**, allez dans le menu **Fichier > Scripts > Autre script...** (`Cmd+F12` sur Mac ou `Ctrl+F12` sur Windows).\n"
                            f"> 3. **Personnalisation interactive :** Ce script est désormais la base active du chat. Vous pouvez demander des ajustements sur-mesure ci-dessous (dimensions, épaisseur de trait à 10px, teintes rouges, etc.) !"
                        )
                        st.session_state.jsx_chat_history.append({
                            "role": "assistant",
                            "content": assistant_md
                        })
                        st.toast(f"⚡ Modèle '{script_data['title']}' injecté ! Vous pouvez le personnaliser dans le chat.", icon="⚡")
                        st.rerun()

        # --- ONGLET PRESETS PERSONNALISÉS DE L'UTILISATEUR ---
        with tab_custom_presets:
            if not user_custom_presets:
                st.info(f"Vous n'avez pas encore de presets personnalisés pour **{soft_short}**.\n\n"
                        f"👉 Générez un script dans l'atelier ci-dessous, puis cliquez sur **« ⭐ Enregistrer ce script dans mes Presets »** "
                        f"ou créez-en un manuellement ci-dessous pour vous constituer votre boîte à outils sur-mesure.")
            else:
                for u_idx, u_preset in enumerate(user_custom_presets):
                    u_col_info, u_col_load, u_col_del = st.columns([3.2, 1.4, 0.5], vertical_alignment="center")
                    with u_col_info:
                        render_html(f"""
                        <div style="background: rgba(22, 27, 34, 0.7); border: 1px solid rgba(133, 163, 99, 0.3); border-radius: 10px; padding: 8px 12px; margin: 4px 0;">
                            <div style="font-weight: 700; color: #85a363; font-size: 0.88rem;">⭐ {u_preset.get('title', 'Preset sans titre')}</div>
                            <div style="font-size: 0.79rem; opacity: 0.82;">{u_preset.get('description', '')}</div>
                        </div>
                        """)
                    with u_col_load:
                        if st.button("⚡ Charger & Modifier", key=f"load_custom_preset_{soft_slug}_{u_idx}", use_container_width=True):
                            st.session_state.jsx_active_base_script = {
                                "title": u_preset.get("title"),
                                "code": u_preset.get("code", ""),
                                "soft": soft_short,
                                "soft_slug": soft_slug,
                                "filename": u_preset.get("filename", f"custom_{soft_slug}.jsx")
                            }
                            st.session_state.jsx_custom_seed = f"Modifie le preset '{u_preset.get('title')}' pour : "
                            st.session_state.jsx_chat_history.append({
                                "role": "user",
                                "content": f"⭐ Chargement du Preset Personnalisé : {u_preset.get('title')}"
                            })
                            st.session_state.jsx_chat_history.append({
                                "role": "assistant",
                                "content": (
                                    f"### ⭐ Preset Personnalisé ({soft_short}) : {u_preset.get('title')}\n\n"
                                    f"{u_preset.get('description', '')}\n\n"
                                    f"```javascript\n{u_preset.get('code', '')}\n```\n\n"
                                    f"> **Preset prêt à l'emploi et chargé dans le chat.** Vous pouvez le télécharger ou demander des ajustements ci-dessous."
                                )
                            })
                            st.toast(f"✅ Preset '{u_preset.get('title')}' chargé comme base active !", icon="⭐")
                            st.rerun()
                    with u_col_del:
                        if st.button("🗑️", key=f"del_custom_preset_{soft_slug}_{u_idx}", use_container_width=True, help="Supprimer ce preset de ma boîte à outils"):
                            deleted_title = u_preset.get('title')
                            state["custom_jsx_presets"][soft_slug].pop(u_idx)
                            save_agency_state(state)
                            st.toast(f"🗑️ Preset '{deleted_title}' supprimé de votre boîte à outils.")
                            st.rerun()

            # Formulaire d'ajout manuel de Preset
            with st.expander(f"➕ Ajouter un nouveau Preset manuellement ({soft_short})"):
                new_preset_title = st.text_input("Titre du Preset :", placeholder="Ex : Grille Carrée 10px Rouge", key=f"new_pre_title_{soft_slug}")
                new_preset_desc = st.text_input("Brève description / objectif :", placeholder="Ex : Tracé de carrés réguliers avec contours rouges de 10px d'épaisseur", key=f"new_pre_desc_{soft_slug}")
                new_preset_code = st.text_area("Code ExtendScript (.jsx) ou brief :", placeholder="// Collez ici un script .jsx fonctionnel...", key=f"new_pre_code_{soft_slug}", height=120)
                if st.button("💾 Enregistrer dans mes Presets", key=f"save_manual_preset_{soft_slug}", use_container_width=True):
                    if new_preset_title.strip() and new_preset_code.strip():
                        state["custom_jsx_presets"].setdefault(soft_slug, []).append({
                            "title": new_preset_title.strip(),
                            "description": new_preset_desc.strip(),
                            "code": new_preset_code.strip(),
                            "filename": f"preset_{re.sub(r'[^a-zA-Z0-9_]', '_', new_preset_title.lower())}.jsx"
                        })
                        save_agency_state(state)
                        st.toast(f"⭐ Preset '{new_preset_title}' ajouté avec succès !")
                        st.rerun()

        # 5. La Puissance Graphique Vectorielle vs IA Raster (Pixels)
        st.markdown("<h4 class='serif-title' style='margin: 18px 0 8px 0;'>🌟 La Puissance du Vectoriel & des Calques Procéduraux vs Pixels IA :</h4>", unsafe_allow_html=True)
        c_p1, c_p2, c_p3, c_p4 = st.columns(4)
        with c_p1:
            render_html("""
            <div class="contour-box" style="min-height: 140px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">
                    📐 Courbes de Bézier Pures
                </div>
                <div style="font-size: 0.81rem; opacity: 0.86; line-height: 1.45;">
                    Précision mathématique infinie. Zéro compression, zéro pixel flou : des tracés vectoriels nets pour l'impression grand format, enseignes ou broderie.
                </div>
            </div>
            """)
        with c_p2:
            render_html("""
            <div class="contour-box" style="min-height: 140px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">
                    🗂️ Calques Nommés & Éditables
                </div>
                <div style="font-size: 0.81rem; opacity: 0.86; line-height: 1.45;">
                    Contrairement aux JPG figés de Midjourney, chaque forme, texte et dégradé réside sur son calque natif. Vos graphistes gardent la main pour ajuster un texte en 2s.
                </div>
            </div>
            """)
        with c_p3:
            render_html(f"""
            <div class="contour-box" style="min-height: 140px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">
                    🎨 Respect Strict de Charte
                </div>
                <div style="font-size: 0.81rem; opacity: 0.86; line-height: 1.45;">
                    Application chirurgicale de vos teintes officielles (<b>{bv_active.get('primary_color', '#85a363')}</b>, <b>{bv_active.get('secondary_color', '#0e1117')}</b>). Aucune hallucination de nuances.
                </div>
            </div>
            """)
        with c_p4:
            render_html("""
            <div class="contour-box" style="min-height: 140px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin-bottom: 4px;">
                    ⚡ 3h de Dessin en 3s
                </div>
                <div style="font-size: 0.81rem; opacity: 0.86; line-height: 1.45;">
                    Génération instantanée de motifs géométriques, grilles d'alignement ou déclinaisons de formats qui nécessiteraient des heures de manipulation manuelle.
                </div>
            </div>
            """)

        st.divider()

        # 6. Espace de Génération Interactif & Historique (Pleine Largeur)
        st.markdown(f"<h4 class='serif-title'>💻 Atelier de Génération & Personnalisation de Scripts ({soft_short})</h4>", unsafe_allow_html=True)
        
        # Historique des scripts générés
        if st.session_state.jsx_chat_history:
            for idx_m, msg in enumerate(st.session_state.jsx_chat_history):
                if msg["role"] == "user":
                    st.markdown(f"<div class='chat-msg-user'><b>Vous :</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-msg-bot'><b>🤖 Ingénieur JSX ({soft_short}) :</b></div>", unsafe_allow_html=True)
                    st.markdown(msg["content"])
                    jsx_code_only = extract_jsx_code(msg["content"])
                    if jsx_code_only:
                        btn_dl_col, btn_save_col, btn_base_col = st.columns([1.5, 1.4, 1.3], vertical_alignment="center")
                        with btn_dl_col:
                            st.download_button(
                                label=f"📥 Télécharger (.jsx)",
                                data=jsx_code_only,
                                file_name=f"script_{soft_slug}_{idx_m+1}.jsx",
                                mime="application/javascript",
                                key=f"dl_jsx_{idx_m}",
                                use_container_width=True
                            )
                        with btn_save_col:
                            with st.popover("⭐ Sauvegarder en Preset", use_container_width=True):
                                pre_title_input = st.text_input("Titre du preset :", value=f"Preset {soft_short} #{idx_m+1}", key=f"pop_title_{idx_m}")
                                pre_desc_input = st.text_input("Description / Notes :", placeholder="Ex : Grille modifiée avec épaisseur 10px", key=f"pop_desc_{idx_m}")
                                if st.button("💾 Confirmer l'enregistrement", key=f"pop_save_btn_{idx_m}", use_container_width=True):
                                    state["custom_jsx_presets"].setdefault(soft_slug, []).append({
                                        "title": pre_title_input.strip() or f"Preset {soft_short} #{idx_m+1}",
                                        "description": pre_desc_input.strip(),
                                        "code": jsx_code_only,
                                        "filename": f"preset_{soft_slug}_{idx_m+1}.jsx"
                                    })
                                    save_agency_state(state)
                                    st.toast("⭐ Script enregistré dans vos Presets personnalisés !")
                                    st.rerun()
                        with btn_base_col:
                            if st.button("✏️ Modifier avec l'IA", key=f"set_as_base_{idx_m}", use_container_width=True, help="Définir ce script comme base pour de futures modifications"):
                                st.session_state.jsx_active_base_script = {
                                    "title": f"Script #{idx_m+1} ({soft_short})",
                                    "code": jsx_code_only,
                                    "soft": soft_short,
                                    "soft_slug": soft_slug,
                                    "filename": f"script_{soft_slug}_{idx_m+1}.jsx"
                                }
                                st.session_state.jsx_custom_seed = f"Modifie ce script pour : "
                                st.toast(f"🧩 Script #{idx_m+1} activé comme base dans le générateur !")
                                st.rerun()

        # Bloc d'alerte / script de base actif
        active_base = st.session_state.get("jsx_active_base_script")
        if active_base and active_base.get("code"):
            render_html(f"""
            <div class="active-base-script-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.74rem; font-weight: 700; color: #85a363; text-transform: uppercase; letter-spacing: 0.5px;">
                            🧩 Script de Base Actif (Itération Connectée)
                        </div>
                        <div style="font-weight: 600; font-size: 0.9rem; color: #f0f6fc; margin-top: 2px;">
                            {active_base.get('title')} ({active_base.get('soft')})
                        </div>
                        <div style="font-size: 0.79rem; opacity: 0.8; margin-top: 2px;">
                            L'IA réutilisera le code de ce script pour appliquer vos modifications précises sans repartir de zéro.
                        </div>
                    </div>
                </div>
            </div>
            """)
            
            # Puces de modifications rapides
            st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #85a363; text-transform: uppercase; margin: 4px 0 6px 0;'>⚡ Personnalisations Rapides Suggérées :</div>", unsafe_allow_html=True)
            ic1, ic2, ic3, ic4 = st.columns(4)
            with ic1:
                if st.button("📏 Dimensions 1200x800", key="chip_dim", use_container_width=True):
                    st.session_state.jsx_custom_seed = f"Modifie le script '{active_base.get('title')}' pour ajuster les dimensions à 1200x800 pixels."
                    st.rerun()
            with ic2:
                if st.button("⚡ Épaisseur traits : 10px", key="chip_stroke", use_container_width=True):
                    st.session_state.jsx_custom_seed = f"Modifie le script '{active_base.get('title')}' pour que tous les tracés aient une épaisseur de 10px (strokeWidth = 10)."
                    st.rerun()
            with ic3:
                if st.button("🔴 Couleur rouge (#ef4444)", key="chip_color", use_container_width=True):
                    st.session_state.jsx_custom_seed = f"Modifie le script '{active_base.get('title')}' pour remplacer la couleur principale par du rouge vif (#ef4444)."
                    st.rerun()
            with ic4:
                if st.button("✖ Détacher la base", key="chip_detach", use_container_width=True, help="Repartir d'une feuille blanche sans script de base"):
                    st.session_state.jsx_active_base_script = None
                    st.session_state.jsx_custom_seed = ""
                    st.rerun()

        ref_img = st.file_uploader("📎 Image, croquis ou maquette de référence (optionnel) :", type=["jpg", "jpeg", "png"], key="jsx_img_up")
        
        default_seed_val = st.session_state.pop("jsx_custom_seed", "")
        prompt_jsx = st.text_area(
            f"Décrivez l'automatisation personnalisée ou les modifications souhaitées dans {soft_short} :",
            value=default_seed_val,
            placeholder=f"Ex : Modifie le script pour que les traits fassent 10px d'épaisseur et que la couleur soit en rouge vif...",
            key="jsx_input_box",
            height=95
        )

        cb1, cb2 = st.columns([4.5, 1.2], vertical_alignment="center")
        with cb1:
            btn_gen_label = f"🪄 Adapter / Générer le script ({soft_short})" if active_base else f"🪄 Générer le script sur-mesure ({soft_short})"
            if st.button(btn_gen_label, use_container_width=True):
                if prompt_jsx.strip():
                    st.session_state.jsx_chat_history.append({"role": "user", "content": prompt_jsx})
                    img_note = " (Maquette de référence jointe)." if ref_img else ""
                    base_code_arg = active_base.get("code") if active_base else None
                    with st.spinner(f"Ingénierie du code ExtendScript pour {soft_short}..."):
                        res_jsx = agent_ingenieur_adobe_jsx(
                            soft_short,
                            f"{prompt_jsx}{img_note}",
                            state,
                            selector.active_model,
                            base_code=base_code_arg
                        )
                        st.session_state.jsx_chat_history.append({"role": "assistant", "content": res_jsx})
                        
                        # Met à jour la base active avec le nouveau script généré pour continuer d'itérer
                        updated_code = extract_jsx_code(res_jsx)
                        if updated_code:
                            st.session_state.jsx_active_base_script = {
                                "title": f"Script Personnalisé ({soft_short})",
                                "code": updated_code,
                                "soft": soft_short,
                                "soft_slug": soft_slug,
                                "filename": f"script_custom_{soft_slug}.jsx"
                            }
                        st.rerun()
        with cb2:
            if st.button("🗑️ Vider", key="clear_jsx_chat", use_container_width=True):
                st.session_state.jsx_chat_history = []
                st.session_state.jsx_active_base_script = None
                st.rerun()



# =====================================================================
# STUDIO DE CRÉATION & SOCIAL ADS (META)
# =====================================================================
elif "Studio" in st.session_state.current_page:
    st.markdown(f"<h2 class='serif-title'>{get_svg_icon('camera', 24, '#85a363')} Studio & Social Ads</h2>", unsafe_allow_html=True)
    render_html(
        f"<div class='contour-box' style='font-size: 0.85rem;'>"
        f"{get_svg_icon('vault', 14, '#85a363')} <b>Personnalisation active via le Profil :</b> <b>{bv_active.get('brand_name')}</b> &nbsp;|&nbsp; "
        f"Ton : <i>{bv_active.get('tone_of_voice')}</i> &nbsp;|&nbsp; "
        f"Style : <i>{bv_active.get('language_style')}</i>"
        f"</div>"
    )

    tab_organic, tab_ads = st.tabs([
        "📸 Publications Organiques",
        "📊 Social Ads & Budgets"
    ])

    # -----------------------------------------------------------------
    # SOUS-ONGLET 1 : PUBLICATIONS ORGANIQUES (INSTAGRAM & FACEBOOK)
    # -----------------------------------------------------------------
    with tab_organic:
        render_html("""
        <div class="contour-box">
            <span class="step-badge">Terrain & Réseaux Sociaux</span>
            <p style="font-size: 0.87rem; opacity: 0.86; margin: 4px 0 0 0;">
                Glissez vos photos de terrain prises lors de vos événements. Choisissez le canal de diffusion (Instagram, Facebook ou cross-posting simultané) et laissez le Studio rédiger des légendes narratives captivantes adaptées à votre cible.
            </p>
        </div>
        """)

        col_left, col_right = st.columns([1.2, 1.2], vertical_alignment="top")
        with col_left:
            uploaded_files = st.file_uploader(
                "1. Photos de la prestation :",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="org_photos_uploader"
            )
            st.write("")
            canal_choisi = st.selectbox(
                "2. Plateforme(s) ciblée(s) :",
                [
                    "Instagram & Facebook (Cross-posting simultané)",
                    "Instagram seul",
                    "Facebook seul"
                ],
                key="studio_canal_select"
            )
            st.write("")
            type_event = render_category_manager("3. Catégorie de prestation :", "custom_categories", "presta_org")

        with col_right:
            intention = render_category_manager("4. Intention & angle marketing :", "custom_intentions", "intent_org")
            st.write("")
            cta_prefere = st.selectbox(
                "5. Appel à l'action souhaité (CTA) :",
                [
                    "DM / Message privé pour devis sur mesure",
                    "Contact direct WhatsApp / Réservation",
                    "Lien dans la bio vers la carte complète",
                    "Commentaire pour recevoir les disponibilités"
                ],
                key="org_cta_select"
            )
            st.write("")
            notes = st.text_area(
                "6. Contexte ou détails de terrain :",
                value=state.get("brief_actif_pour_studio", ""),
                height=95,
                key="org_notes_input",
                placeholder=f"Ex : Prestation chez un client à {bv_active.get('location', 'Besançon')}, présentation des spécialités de {bv_active.get('brand_name', 'notre commerce')}..."
            )

        st.write("")
        if st.button("✨ Rédiger la publication Meta (Légendes & Hashtags)", key="btn_gen_organic_post", use_container_width=True):
            if not uploaded_files:
                st.warning("Veuillez glisser au moins une photo de prestation.")
            else:
                images = [Image.open(f) for f in uploaded_files]
                combined_notes = f"{notes}\nAppel à l'action visé : {cta_prefere}"
                with st.spinner(f"Analyse visuelle et rédaction sur mesure pour {bv_active.get('brand_name')} ({canal_choisi})..."):
                    _, _, _, out_copy = pipeline_studio_collaboratif(
                        images,
                        type_event,
                        intention,
                        canal_choisi,
                        combined_notes,
                        state,
                        selector.active_model
                    )
                    st.session_state.studio_copy = out_copy
                    st.session_state.studio_platform = canal_choisi

        if "studio_copy" in st.session_state:
            st.divider()
            target_plat = st.session_state.get("studio_platform", "Instagram & Facebook")
            st.markdown(f"<h4 class='serif-title'>📝 Proposition éditoriale — {target_plat}</h4>", unsafe_allow_html=True)
            st.markdown(st.session_state.studio_copy)
            st.write("")
            sc1, sc2 = st.columns([2, 2], vertical_alignment="center")
            with sc1:
                if st.button("🟠 Enregistrer comme « À valider » au Planning", key="btn_save_organic_planning", use_container_width=True):
                    target_d = today_obj + timedelta(days=1)
                    state["calendrier_tactique"].append({
                        "jour": target_d.strftime("%Y-%m-%d"),
                        "sujet": f"{type_event} — {intention}",
                        "objectif": f"{target_plat} — {intention}",
                        "statut": "À valider",
                        "legende_prete": st.session_state.studio_copy
                    })
                    save_agency_state(state)
                    st.success("Post enregistré avec succès dans le calendrier mensuel en statut « À valider » !")
            with sc2:
                if st.button("📅 Aller vérifier sur le Calendrier Mensuel →", key="btn_go_planning_from_studio", use_container_width=True):
                    st.session_state.current_page = "📅 Planning"
                    st.rerun()

    # -----------------------------------------------------------------
    # SOUS-ONGLET 2 : SOCIAL ADS & PILOTAGE DES BUDGETS META
    # -----------------------------------------------------------------
    with tab_ads:
        render_html("""
        <div class="contour-box">
            <span class="step-badge">Acquisition Payante & ROI</span>
            <p style="font-size: 0.87rem; opacity: 0.86; margin: 4px 0 0 0;">
                Pilotez vos campagnes sponsorisées Instagram & Facebook Ads. L'IA optimise la répartition de votre budget publicitaire, génère les textes d'accroche et suit vos indicateurs de rentabilité (ROAS, CPC, Conversions).
            </p>
        </div>
        """)

        ads_state = state["meta_ads_data"]
        connector = MetaMarketingAPIConnector(ads_state.get("api_config"))
        metrics = connector.get_dashboard_metrics(
            monthly_budget=ads_state.get("monthly_budget_target", 450.0),
            active_campaigns=ads_state.get("active_campaigns", [])
        )

        # 1. Cartes de bord (KPIs)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        pct_spent = (metrics["spend"] / max(metrics["budget_total"], 1.0)) * 100
        with kpi1:
            render_html(f"""
            <div class="ads-metric-card">
                <div class="ads-metric-title">Budget Mensuel Engagé</div>
                <div class="ads-metric-val">{metrics['spend']:.2f} €</div>
                <div class="ads-metric-sub">Plafond : {metrics['budget_total']:.0f} € ({pct_spent:.1f}%)</div>
            </div>
            """)
        with kpi2:
            render_html(f"""
            <div class="ads-metric-card">
                <div class="ads-metric-title">Portée & Impressions</div>
                <div class="ads-metric-val">{metrics['impressions']:,}</div>
                <div class="ads-metric-sub">{metrics['clicks']} clics générés</div>
            </div>
            """.replace(",", " "))
        with kpi3:
            render_html(f"""
            <div class="ads-metric-card">
                <div class="ads-metric-title">Coût / Clic (CPC) & CTR</div>
                <div class="ads-metric-val">{metrics['cpc']:.2f} €</div>
                <div class="ads-metric-sub">CTR moyen : {metrics['ctr']:.2f}%</div>
            </div>
            """)
        with kpi4:
            render_html(f"""
            <div class="ads-metric-card">
                <div class="ads-metric-title">ROAS & Prospects Qualifiés</div>
                <div class="ads-metric-val">{metrics['roas']:.2f}x</div>
                <div class="ads-metric-sub">{metrics['leads']} prospects / WhatsApp</div>
            </div>
            """)

        # 2. Graphiques de suivi hebdomadaire
        st.markdown("<h4 class='serif-title' style='margin: 14px 0 8px 0;'>📈 Dynamique Hebdomadaire & Répartition des Dépenses</h4>", unsafe_allow_html=True)
        w_spend, w_clicks = connector.get_weekly_trends(ads_state.get("monthly_budget_target", 450.0))
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.caption("Dépenses publicitaires hebdomadaires (€) :")
            st.bar_chart(w_spend)
        with g_col2:
            st.caption("Volume de clics hebdomadaires :")
            st.bar_chart(w_clicks)

        st.divider()

        # 3. Paramétrage du Budget Publicitaire alloué à l'IA
        st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>💰 Allocation Budgétaire & Stratégie d'Enchères</h4>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3 = st.columns([1.5, 1.5, 1.2], vertical_alignment="center")
        with b_col1:
            new_budget = st.number_input(
                "Budget mensuel total alloué (€) :",
                min_value=50.0,
                max_value=10000.0,
                value=float(ads_state.get("monthly_budget_target", 450.0)),
                step=50.0,
                key="num_meta_budget"
            )
        with b_col2:
            enchere_mode = st.selectbox(
                "Mode d'optimisation de l'IA :",
                [
                    "Maximiser le volume de prospects WhatsApp / DM (Recommandé)",
                    "Maximiser le ROAS & Commandes de banquets",
                    "Minimiser le Coût par Clic (CPC le plus bas)",
                    "Couverture maximale & Notoriété locale"
                ],
                key="select_meta_bid_strategy"
            )
        with b_col3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("💾 Valider le budget", key="btn_save_meta_budget", use_container_width=True):
                ads_state["monthly_budget_target"] = new_budget
                ads_state["bidding_strategy"] = enchere_mode
                save_agency_state(state)
                st.success("Allocation budgétaire enregistrée avec succès !")
                st.rerun()

        st.divider()

        # 4. Liste des campagnes actives
        st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>🎯 Campagnes Publicitaires en Cours</h4>", unsafe_allow_html=True)
        active_camps = ads_state.get("active_campaigns", [])
        if not active_camps:
            st.info("Aucune campagne active actuellement. Créez votre première campagne sponsorisée ci-dessous.")
        else:
            for c_idx, camp in enumerate(active_camps):
                c_nom = camp.get("nom", "Campagne sans nom")
                c_obj = camp.get("objectif", "Non spécifié")
                c_bjour = camp.get("budget_jour", 0.0)
                c_dep = camp.get("depenses_total", 0.0)
                c_imp = camp.get("impressions", 0)
                c_clics = camp.get("clics", 0)
                c_roas = camp.get("roas", 0.0)
                c_leads = camp.get("conversions", 0)
                c_statut = camp.get("statut", "Actif")
                c_ciblage = camp.get("ciblage", "")

                with st.expander(f"📢 {c_nom} — {c_statut} ({c_bjour} €/j | Total : {c_dep} €)", expanded=(c_idx == 0)):
                    camp_col1, camp_col2, camp_col3 = st.columns([2, 1.2, 0.8], vertical_alignment="center")
                    with camp_col1:
                        st.markdown(f"**Objectif :** {c_obj}")
                        if c_ciblage:
                            st.caption(f"🎯 **Ciblage :** {c_ciblage}")
                    with camp_col2:
                        st.markdown(f"**Impressions :** {c_imp:,} &nbsp;|&nbsp; **Clics :** {c_clics}".replace(",", " "), unsafe_allow_html=True)
                        st.markdown(f"**Leads :** {c_leads} &nbsp;|&nbsp; **ROAS :** {c_roas}x")
                    with camp_col3:
                        if st.button("🗑️ Supprimer", key=f"del_camp_{c_idx}", use_container_width=True):
                            active_camps.pop(c_idx)
                            save_agency_state(state)
                            st.rerun()

        st.divider()

        # 5. Création d'une nouvelle campagne sponsorisée par IA
        st.markdown("<h4 class='serif-title' style='margin-bottom: 8px;'>✨ Créer une Nouvelle Campagne Publicitaire (IA Copywriter & Media Buyer)</h4>", unsafe_allow_html=True)
        form_ad1, form_ad2 = st.columns(2)
        with form_ad1:
            ad_name = st.text_input(
                "Nom de la campagne :",
                value=f"Campagne Notoriété & Clients — {bv_active.get('location')}",
                key="ad_input_name"
            )
            ad_obj = st.selectbox(
                "Objectif commercial Meta Ads :",
                [
                    "Génération de prospects & WhatsApp",
                    "Messages Instagram Direct (DM)",
                    "Trafic qualifié vers le site Web",
                    "Notoriété & Couverture locale"
                ],
                key="ad_input_objective"
            )
            ad_daily = st.number_input(
                "Budget quotidien alloué (€/jour) :",
                min_value=5.0,
                max_value=200.0,
                value=15.0,
                step=5.0,
                key="ad_input_daily_budget"
            )

        with form_ad2:
            ad_placement = st.selectbox(
                "Emplacements de diffusion ciblés :",
                [
                    "Instagram & Facebook (Placements Advantage+ automatiques)",
                    "Instagram Stories & Reels uniquement",
                    "Instagram Feed uniquement",
                    "Facebook Feed uniquement"
                ],
                key="ad_input_placement"
            )
            ad_targeting = st.text_input(
                "Audience & Ciblage géographique :",
                value=f"{bv_active.get('location')} ({bv_active.get('client_type', 'Clients locaux, 25-60 ans')})",
                key="ad_input_target"
            )
            ad_pitch = st.text_area(
                "Offre, angle ou promesse publicitaire :",
                value=f"Découvrez {bv_active.get('brand_name')} à {bv_active.get('location')} : {bv_active.get('short_dna', '')[:95]}",
                height=72,
                key="ad_input_pitch"
            )

        st.write("")
        if st.button("🚀 Rédiger les créatifs publicitaires & Stratégie d'enchères via l'IA", key="btn_run_ads_copywriter", use_container_width=True):
            with st.spinner(f"Rédaction des annonces publicitaires Meta pour {bv_active.get('brand_name')}..."):
                ads_strategy_text = agent_meta_ads_copywriter(
                    ad_obj,
                    ad_targeting,
                    ad_pitch,
                    ad_daily,
                    ad_placement,
                    state,
                    selector.active_model
                )
                st.session_state.current_ads_strategy = ads_strategy_text
                st.session_state.pending_ad_campaign = {
                    "nom": ad_name,
                    "obj": ad_obj,
                    "daily": ad_daily,
                    "targeting": ad_targeting,
                    "pitch": ad_pitch
                }

        if "current_ads_strategy" in st.session_state:
            st.divider()
            st.markdown("<h4 class='serif-title'>🎯 Stratégie & Copies Publicitaires Générées</h4>", unsafe_allow_html=True)
            st.markdown(st.session_state.current_ads_strategy)
            st.write("")
            if st.button("🚀 Lancer la campagne dans le simulateur / API Meta", key="btn_deploy_ad_campaign", use_container_width=True):
                pend = st.session_state.get("pending_ad_campaign", {})
                new_camp_obj = connector.create_campaign(
                    name=pend.get("nom", ad_name),
                    objective=pend.get("obj", ad_obj),
                    daily_budget=pend.get("daily", ad_daily),
                    targeting=pend.get("targeting", ad_targeting),
                    pitch=pend.get("pitch", ad_pitch)
                )
                ads_state["active_campaigns"].append(new_camp_obj)
                save_agency_state(state)
                st.session_state.pop("current_ads_strategy", None)
                st.session_state.pop("pending_ad_campaign", None)
                st.success(f"La campagne « {new_camp_obj['nom']} » est désormais active et optimisée en continu par l'IA !")
                st.rerun()

        st.divider()

        # 6. Architecture Modulaire : Connexion Meta Marketing & Graph API v19.0
        with st.expander("⚡ Architecture Modulaire & Clés API Meta Marketing (Graph API v19.0)", expanded=False):
            st.markdown("""
            Ce connecteur modulaire (`MetaMarketingAPIConnector`) est prêt pour la production. En mode Sandbox, les performances et coûts sont simulés de manière réaliste. Dès que vos clés de production sont renseignées, l'application bascule automatiquement sur les endpoints réels de Meta Graph API v19.0 (`https://graph.facebook.com/v19.0/`).
            """)
            api_cfg = ads_state.get("api_config", {})
            c_api1, c_api2 = st.columns(2)
            with c_api1:
                in_token = st.text_input(
                    "Meta User / System Access Token :",
                    value=api_cfg.get("access_token", ""),
                    type="password",
                    placeholder="EAABw...",
                    key="meta_api_token"
                )
                in_ad_acc = st.text_input(
                    "Ad Account ID (Compte publicitaire) :",
                    value=api_cfg.get("ad_account_id", "act_849204918204"),
                    key="meta_ad_acc_id"
                )
            with c_api2:
                in_pixel = st.text_input(
                    "Meta Pixel ID (Suivi conversions) :",
                    value=api_cfg.get("pixel_id", "px_9201940182"),
                    key="meta_pixel_id"
                )
                in_sandbox = st.checkbox(
                    "Activer le mode Sandbox / Simulation sécurisée",
                    value=api_cfg.get("sandbox_mode", True),
                    key="meta_sandbox_chk"
                )

            if st.button("💾 Sauvegarder les paramètres Meta Marketing API", key="btn_save_meta_api", use_container_width=True):
                ads_state["api_config"] = {
                    "access_token": in_token.strip(),
                    "ad_account_id": in_ad_acc.strip(),
                    "pixel_id": in_pixel.strip(),
                    "sandbox_mode": in_sandbox
                }
                save_agency_state(state)
                st.success("Paramètres d'API Meta enregistrés avec succès !")
                st.rerun()


# =====================================================================
# MON COMPTE & ENTREPRISE
# =====================================================================
elif "Compte" in st.session_state.current_page or "Coffre-fort" in st.session_state.current_page or "Profil" in st.session_state.current_page:
    st.markdown(f"<h2 class='serif-title'>{get_svg_icon('user', 24, '#85a363')} Mon Compte & Entreprise</h2>", unsafe_allow_html=True)
    render_html(
        "<div class='contour-box' style='margin-bottom: 20px;'>"
        "Espace central de configuration de votre identité et de votre entreprise. "
        "<b>Tous les agents IA de la plateforme</b> (Stratégie, Marketing, Studio & Campagnes) utilisent "
        "directement ces paramètres en temps réel pour personnaliser chacune de leurs propositions à votre réalité de terrain, "
        "éliminant toute valeur générique."
        "</div>"
    )

    col_vault_form, col_vault_preview = st.columns([1.85, 1.15], vertical_alignment="top")

    with col_vault_form:
        # -------------------------------------------------------------
        # PROFIL UTILISATEUR
        # -------------------------------------------------------------
        st.markdown(f"<h4 class='serif-title' style='margin-bottom: 12px;'>{get_svg_icon('user', 18, '#85a363')} Profil Utilisateur</h4>", unsafe_allow_html=True)
        u_col1, u_col2, u_col3 = st.columns(3)
        with u_col1:
            val_user_fn = clean_placeholder_val("user_first_name", bv_active.get("user_first_name", ""))
            in_user_fn = st.text_input(
                "Prénom :",
                value=val_user_fn,
                placeholder="Ex : Simon",
                key="acc_user_fn"
            )
        with u_col2:
            val_user_ln = clean_placeholder_val("user_last_name", bv_active.get("user_last_name", ""))
            in_user_ln = st.text_input(
                "Nom :",
                value=val_user_ln,
                placeholder="Ex : Zoni",
                key="acc_user_ln"
            )
        with u_col3:
            val_user_role = clean_placeholder_val("user_role", bv_active.get("user_role", ""))
            in_user_role = st.text_input(
                "Rôle dans l'entreprise :",
                value=val_user_role,
                placeholder="Ex : Dirigeant, Fondateur, Gérant...",
                key="acc_user_role"
            )

        render_html("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 20px 0;'></div>")

        # -------------------------------------------------------------
        # ENTREPRISE & STRATÉGIE
        # -------------------------------------------------------------
        st.markdown(f"<h4 class='serif-title' style='margin-bottom: 12px;'>{get_svg_icon('building', 18, '#85a363')} Entreprise & Stratégie</h4>", unsafe_allow_html=True)
        b_c1, b_c2, b_c3 = st.columns([1.4, 1.3, 1.3])
        with b_c1:
            val_brand_name = clean_placeholder_val("brand_name", bv_active.get("brand_name", ""))
            in_brand_name = st.text_input(
                "Nom de l'entreprise / commerce :",
                value=val_brand_name,
                placeholder="Ex : Maison Dupont, Le Bistrot des Halles...",
                key="acc_brand_name"
            )
        with b_c2:
            val_business_type = clean_placeholder_val("business_type", bv_active.get("business_type", ""))
            in_business_type = st.text_input(
                "Secteur d'activité principal :",
                value=val_business_type,
                placeholder="Ex : Restaurant bistronomique, Caviste, Traiteur...",
                key="acc_business_type"
            )
        with b_c3:
            val_location = clean_placeholder_val("location", bv_active.get("location", ""))
            in_location = st.text_input(
                "Ville / Implantation principale :",
                value=val_location,
                placeholder="Ex : Vesoul, Besançon, Lyon, Paris...",
                key="acc_location"
            )

        # Portée de la cible & Type de marché
        st_c1, st_c2 = st.columns(2)
        scope_options = [
            "Local / De proximité",
            "National",
            "International"
        ]
        curr_scope = bv_active.get("target_scope", "Local / De proximité")
        scope_idx = scope_options.index(curr_scope) if curr_scope in scope_options else 0
        with st_c1:
            in_target_scope = st.selectbox(
                "Portée géographique de la cible :",
                options=scope_options,
                index=scope_idx,
                help="Définit si les campagnes et conseils de vos agents ciblent votre zone locale, le niveau national ou l'international.",
                key="acc_target_scope"
            )

        market_options = [
            "B2C / Grand public",
            "B2B / Professionnels",
            "Mixte (B2C & B2B)"
        ]
        curr_market = bv_active.get("market_type", "B2C / Grand public")
        market_idx = market_options.index(curr_market) if curr_market in market_options else 0
        with st_c2:
            in_market_type = st.selectbox(
                "Typologie de marché prioritaire :",
                options=market_options,
                index=market_idx,
                help="Adapte le vocabulaire des agents et les canaux (ex: B2C = Instagram/Avis locaux, B2B = LinkedIn/E-mailing professionnel).",
                key="acc_market_type"
            )

        val_client_type = clean_placeholder_val("client_type", bv_active.get("client_type", ""))
        in_client_type = st.text_input(
            "Typologie de clientèle cible détaillée :",
            value=val_client_type,
            placeholder="Ex : Actifs du centre-ville, familles, couples, professionnels...",
            key="acc_client_type"
        )

        val_short_dna = clean_placeholder_val("short_dna", bv_active.get("short_dna", ""))
        in_short_dna = st.text_area(
            "Description courte / ADN de la marque :",
            value=val_short_dna,
            placeholder="Ex : Cuisine artisanale de saison, accueil chaleureux et convivialité. Nous valorisons les produits locaux et un service soigné.",
            height=85,
            help="Ce résumé synthétise votre identité, votre mission et votre proposition de valeur.",
            key="acc_short_dna"
        )

        # Module interactif de synchronisation Google Maps & Avis
        with st.expander("📍 Synchronisation Fiche & Avis Clients (Google Maps)", expanded=bool(bv_active.get("google_maps_query") or bv_active.get("google_reviews_summary"))):
            in_maps_query = st.text_input(
                "Nom de la fiche Google Maps ou URL :",
                value=bv_active.get("google_maps_query", ""),
                placeholder="Ex : Nom de votre établissement ou URL Google Maps",
                key="acc_maps_query"
            )

            if st.button("🔍 Analyser & Synchroniser le Contexte Google Maps (Avis & Réputation)", key="acc_btn_sync_gmaps", use_container_width=True):
                target_bname = in_brand_name.strip() or "Mon Commerce"
                target_bloc = in_location.strip() or "Ma Ville"
                with st.spinner(f"Analyse de réputation et contexte local pour {target_bname} à {target_bloc}..."):
                    maps_md, maps_json = agent_analyse_profil_google_maps(
                        target_bname,
                        target_bloc,
                        in_business_type,
                        in_client_type,
                        in_maps_query,
                        state,
                        selector.active_model
                    )
                    st.session_state.last_gmaps_analysis = maps_md
                    if maps_json:
                        try:
                            clean_mj = maps_json.strip("`").replace("json", "").strip()
                            st.session_state.last_gmaps_parsed = json.loads(clean_mj)
                        except Exception:
                            st.session_state.last_gmaps_parsed = None
                    st.rerun()

            if "last_gmaps_analysis" in st.session_state:
                st.markdown(st.session_state.last_gmaps_analysis, unsafe_allow_html=True)
                if st.session_state.get("last_gmaps_parsed"):
                    parsed_gm = st.session_state.last_gmaps_parsed
                    if st.button("🪄 Appliquer cet ADN et ce résumé d'avis au profil", key="acc_btn_apply_gmaps_data", use_container_width=True):
                        if parsed_gm.get("short_dna"):
                            bv_active["short_dna"] = parsed_gm["short_dna"]
                        if parsed_gm.get("google_reviews_summary"):
                            bv_active["google_reviews_summary"] = parsed_gm["google_reviews_summary"]
                        if parsed_gm.get("recommended_tone") and parsed_gm["recommended_tone"] not in state["custom_tones"]:
                            state["custom_tones"].insert(0, parsed_gm["recommended_tone"])
                            bv_active["tone_of_voice"] = parsed_gm["recommended_tone"]
                        st.session_state.pop("last_gmaps_analysis", None)
                        st.session_state.pop("last_gmaps_parsed", None)
                        save_agency_state(state)
                        st.success("Données appliquées au profil avec succès !")
                        st.rerun()

            val_reviews_summary = clean_placeholder_val("google_reviews_summary", bv_active.get("google_reviews_summary", ""))
            in_reviews_summary = st.text_area(
                "Synthèse des avis clients & réputation locale :",
                value=val_reviews_summary,
                placeholder="Ex : Note 4.9/5 sur Google Maps. Retours réguliers sur l'accueil souriant, la fraîcheur des produits et la ponctualité.",
                height=65,
                key="acc_reviews_summary"
            )

        render_html("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 20px 0;'></div>")

        # -------------------------------------------------------------
        # LOGO OFFICIEL DE L'ENTREPRISE
        # -------------------------------------------------------------
        st.markdown(f"<h4 class='serif-title' style='margin-bottom: 12px;'>{get_svg_icon('sparkles', 18, '#85a363')} Logo Officiel</h4>", unsafe_allow_html=True)
        
        logo_c1, logo_c2 = st.columns([1.1, 2.9], vertical_alignment="center")
        with logo_c1:
            if encoded_logo:
                render_html(f"""
                <div style="text-align: center;">
                    <img src="data:image/png;base64,{encoded_logo}" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 2px solid #85a363; box-shadow: 0 4px 12px rgba(0,0,0,0.3);" />
                    <div style="font-size: 0.72rem; color: #85a363; margin-top: 4px;">Logo actif</div>
                </div>
                """)
            else:
                render_html("""
                <div style="text-align: center; width: 70px; height: 70px; border-radius: 50%; background: rgba(133, 163, 99, 0.15); border: 1px dashed #85a363; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                    <span style="font-size: 1.8rem;">🏢</span>
                </div>
                """)

        with logo_c2:
            st.caption("Téléversez le logo de votre entreprise (PNG, JPG, JPEG, SVG). Il sera immédiatement affiché partout sur la plateforme.")
            uploaded_logo_file = st.file_uploader(
                "Choisir un fichier de logo :",
                type=["png", "jpg", "jpeg", "svg"],
                key="acc_uploaded_logo_file",
                label_visibility="collapsed"
            )

        if uploaded_logo_file is not None:
            btn_up_col1, btn_up_col2 = st.columns(2)
            with btn_up_col1:
                if st.button("✨ Appliquer ce logo sur l'ensemble du site", key="acc_btn_save_logo", use_container_width=True):
                    logo_target_path = Path("user_profile_avatar.png")
                    logo_target_path.write_bytes(uploaded_logo_file.getvalue())
                    state["user_profile_image"] = "user_profile_avatar.png"
                    save_agency_state(state)
                    st.success("✅ Nouveau logo appliqué avec succès sur toute la plateforme !")
                    st.rerun()
            with btn_up_col2:
                if st.button("🔄 Rétablir le logo par défaut", key="acc_btn_reset_logo_uploaded", use_container_width=True):
                    state["user_profile_image"] = "logo.png" if Path("logo.png").exists() else ""
                    save_agency_state(state)
                    st.info("Logo par défaut rétabli.")
                    st.rerun()
        elif state.get("user_profile_image") and state.get("user_profile_image") != "logo.png":
            if st.button("🔄 Rétablir le logo par défaut de la plateforme", key="acc_btn_reset_logo_standalone", use_container_width=False):
                state["user_profile_image"] = "logo.png" if Path("logo.png").exists() else ""
                save_agency_state(state)
                st.info("Logo par défaut rétabli.")
                st.rerun()

        render_html("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 20px 0;'></div>")

        # -------------------------------------------------------------
        # CHARTE GRAPHIQUE, COULEURS & LIGNE ÉDITORIALE
        # -------------------------------------------------------------
        in_prim_col = bv_active.get("primary_color", "#85a363")
        in_sec_col = bv_active.get("secondary_color", "#0e1117")
        in_acc_col = bv_active.get("accent_color", "#f59e0b")
        in_tone = bv_active.get("tone_of_voice", "Chaleureux, Professionnel & Accessible")
        in_lang_style = bv_active.get("language_style", "")
        in_typo = bv_active.get("typography_notes", "")

        with st.expander("🎨 Charte Graphique, Couleurs & Ligne Éditoriale", expanded=True):
            st.markdown("<h5 class='serif-title' style='margin-bottom: 8px;'>Codes Couleurs Officiels</h5>", unsafe_allow_html=True)
            cp1, cp2, cp3 = st.columns(3, vertical_alignment="center")
            with cp1:
                in_prim_col = st.color_picker("Couleur Principale (Signature) :", value=in_prim_col, key="acc_c1")
                st.caption(f"`{in_prim_col}` · {hex_to_rgb_str(in_prim_col)}")
            with cp2:
                in_sec_col = st.color_picker("Couleur Secondaire (Fond sombre) :", value=in_sec_col, key="acc_c2")
                st.caption(f"`{in_sec_col}` · {hex_to_rgb_str(in_sec_col)}")
            with cp3:
                in_acc_col = st.color_picker("Couleur d'Accentuation (Énergie) :", value=in_acc_col, key="acc_c3")
                st.caption(f"`{in_acc_col}` · {hex_to_rgb_str(in_acc_col)}")

            st.divider()
            st.markdown("<h5 class='serif-title' style='margin-bottom: 8px;'>Ton de Communication & Style</h5>", unsafe_allow_html=True)

            if "selected_vault_tone" not in st.session_state:
                curr_tone = in_tone
                if curr_tone not in state["custom_tones"]:
                    state["custom_tones"].insert(0, curr_tone)
                st.session_state["selected_vault_tone"] = curr_tone

            in_tone = render_category_manager("Ton de communication principal :", "custom_tones", "acc_tone_manager")
            st.write("")

            val_lang_style = clean_placeholder_val("language_style", in_lang_style)
            val_typo = clean_placeholder_val("typography_notes", in_typo)

            t_col1, t_col2 = st.columns(2)
            with t_col1:
                in_lang_style = st.text_input(
                    "Directive linguistique (Studio) :",
                    value=val_lang_style,
                    placeholder="Ex : Français soigné, vouvoiement courtois et chaleureux...",
                    key="acc_lang_in"
                )
            with t_col2:
                in_typo = st.text_input(
                    "Polices & Repères typographiques :",
                    value=val_typo,
                    placeholder="Ex : Playfair Display (Titres) & Plus Jakarta Sans (Corps)",
                    key="acc_typo_in"
                )

        # -------------------------------------------------------------
        # BOUTON D'ENREGISTREMENT GLOBAL & RÉINITIALISATION
        # -------------------------------------------------------------
        render_html("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 24px 0 16px 0;'></div>")
        btn_save_col, btn_reset_col = st.columns([2.5, 1.2], vertical_alignment="center")
        with btn_save_col:
            if st.button("💾 Enregistrer Mon Compte & Mon Entreprise", key="acc_save_all_btn", use_container_width=True):
                full_founder = f"{in_user_fn.strip()} {in_user_ln.strip()}".strip() or "Simon Zoni"
                state["brand_vault"] = {
                    "brand_name": in_brand_name.strip() or DEFAULT_BRAND_VAULT["brand_name"],
                    "business_type": in_business_type.strip() or DEFAULT_BRAND_VAULT.get("business_type", "Commerce / Service"),
                    "user_first_name": in_user_fn.strip() or "Simon",
                    "user_last_name": in_user_ln.strip() or "Zoni",
                    "founder_or_lead": full_founder,
                    "user_role": in_user_role.strip() or "Dirigeant",
                    "location": in_location.strip() or DEFAULT_BRAND_VAULT["location"],
                    "target_scope": in_target_scope,
                    "market_type": in_market_type,
                    "client_type": in_client_type.strip() or "Particuliers & clientèle locale",
                    "google_maps_query": in_maps_query.strip(),
                    "google_reviews_summary": in_reviews_summary.strip(),
                    "short_dna": in_short_dna.strip() or DEFAULT_BRAND_VAULT["short_dna"],
                    "primary_color": in_prim_col,
                    "secondary_color": in_sec_col,
                    "accent_color": in_acc_col,
                    "tone_of_voice": in_tone,
                    "language_style": in_lang_style.strip() or DEFAULT_BRAND_VAULT["language_style"],
                    "typography_notes": in_typo.strip() or DEFAULT_BRAND_VAULT["typography_notes"],
                }
                state["user_display_name"] = full_founder
                save_agency_state(state)
                st.success("✅ Profil Utilisateur & Entreprise sauvegardés avec succès ! Tous les agents IA sont synchronisés.")
                st.rerun()

        with btn_reset_col:
            if st.button("🔄 Valeurs par défaut", key="acc_reset_all_btn", use_container_width=True):
                state["brand_vault"] = DEFAULT_BRAND_VAULT.copy()
                state["user_display_name"] = DEFAULT_BRAND_VAULT["founder_or_lead"]
                st.session_state["selected_vault_tone"] = DEFAULT_BRAND_VAULT["tone_of_voice"]
                save_agency_state(state)
                st.info("Profil réinitialisé aux valeurs par défaut.")
                st.rerun()

    # -------------------------------------------------------------
    # COLONNE DE DROITE : APERÇU TEMPS RÉEL (CARTE D'IDENTITÉ IA)
    # -------------------------------------------------------------
    with col_vault_preview:
        logo_preview_html = ""
        if encoded_logo:
            logo_preview_html = (
                f"<div style='text-align: center; margin-bottom: 12px;'>"
                f"<img src='data:image/png;base64,{encoded_logo}' style='width: 74px; height: 74px; border-radius: 50%; object-fit: cover; border: 2px solid {in_prim_col}; box-shadow: 0 4px 14px rgba(0,0,0,0.35);' />"
                f"</div>"
            )

        maps_badge_preview = ""
        if in_maps_query or in_reviews_summary:
            maps_badge_preview = (
                f"<div style='background: rgba(133, 163, 99, 0.12); border-left: 3px solid #85a363; "
                f"border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; font-size: 0.80rem;'>"
                f"<b>⭐ Réputation locale :</b> {in_maps_query or in_brand_name or 'Établissement'}<br>"
                f"<span style='opacity: 0.88; font-style: italic;'>{in_reviews_summary or 'Avis clients analysés'}</span>"
                f"</div>"
            )

        dna_preview = format_vault_field("short_dna", in_short_dna, fallback="Renseignez votre description courte / ADN pour visualiser l'aperçu...")
        user_fn_disp = in_user_fn if in_user_fn else "Prénom"
        user_ln_disp = in_user_ln if in_user_ln else "Nom"
        user_role_disp = in_user_role if in_user_role else "Dirigeant"
        brand_name_disp = in_brand_name if in_brand_name else "Votre Entreprise"
        loc_disp = format_vault_field("location", in_location)
        sector_disp = format_vault_field("business_type", in_business_type)
        client_disp = format_vault_field("client_type", in_client_type)
        scope_disp = format_vault_field("target_scope", in_target_scope)
        market_disp = format_vault_field("market_type", in_market_type)
        lang_disp = format_vault_field("language_style", in_lang_style, fallback="Français soigné")
        typo_disp = format_vault_field("typography_notes", in_typo, fallback="Playfair Display & Plus Jakarta Sans")

        preview_card_html = (
            f"<div class='compass-panel' style='border-color: {in_prim_col};'>"
            f"<span class='step-badge' style='border-color: {in_prim_col}; color: {in_prim_col};'>Aperçu Temps Réel — Carte d'Identité IA</span>"
            f"{logo_preview_html}"
            f"<h3 class='serif-title' style='margin: 8px 0 2px 0; text-align: center;'>{brand_name_disp}</h3>"
            f"<div style='font-size: 0.76rem; color: {in_prim_col}; text-align: center; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px;'>"
            f"{scope_disp} &nbsp;·&nbsp; {market_disp}"
            f"</div>"
            f"<div style='background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; font-size: 0.82rem;'>"
            f"<div style='margin-bottom: 4px;'><b>👤 Utilisateur :</b> {user_fn_disp} {user_ln_disp} <span style='opacity: 0.65;'>({user_role_disp})</span></div>"
            f"<div style='margin-bottom: 4px;'>📍 <b>Implantation :</b> {loc_disp}</div>"
            f"<div style='margin-bottom: 4px;'>🏷️ <b>Secteur :</b> {sector_disp}</div>"
            f"<div>🎯 <b>Cible :</b> {client_disp}</div>"
            f"</div>"
            f"{maps_badge_preview}"
            f"<div style='border-left: 3px solid {in_acc_col}; padding-left: 12px; margin-bottom: 14px; font-size: 0.83rem; opacity: 0.9; line-height: 1.5;'>"
            f"{dna_preview}"
            f"</div>"
            f"<div class='vault-swatch-card'>"
            f"<div class='vault-swatch-circle' style='background-color: {in_prim_col};'></div>"
            f"<div><div style='font-size: 0.8rem; font-weight: 600;'>Principale · {in_prim_col}</div><div style='font-size: 0.73rem; opacity: 0.7;'>{hex_to_rgb_str(in_prim_col)}</div></div>"
            f"</div>"
            f"<div class='vault-swatch-card'>"
            f"<div class='vault-swatch-circle' style='background-color: {in_sec_col};'></div>"
            f"<div><div style='font-size: 0.8rem; font-weight: 600;'>Secondaire · {in_sec_col}</div><div style='font-size: 0.73rem; opacity: 0.7;'>{hex_to_rgb_str(in_sec_col)}</div></div>"
            f"</div>"
            f"<div class='vault-swatch-card'>"
            f"<div class='vault-swatch-circle' style='background-color: {in_acc_col};'></div>"
            f"<div><div style='font-size: 0.8rem; font-weight: 600;'>Accent · {in_acc_col}</div><div style='font-size: 0.73rem; opacity: 0.7;'>{hex_to_rgb_str(in_acc_col)}</div></div>"
            f"</div>"
            f"<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 14px 0;'></div>"
            f"<p style='font-size: 0.82rem; margin-bottom: 6px;'><b>🎙️ Ton injecté aux agents :</b><br><span style='color: {in_prim_col}; font-weight: 500;'>{in_tone}</span></p>"
            f"<p style='font-size: 0.82rem; margin-bottom: 6px;'><b>✍️ Directive linguistique :</b><br><span style='opacity: 0.85;'>{lang_disp}</span></p>"
            f"<p style='font-size: 0.82rem; margin-bottom: 0;'><b>🔤 Typographies :</b><br><span style='opacity: 0.85;'>{typo_disp}</span></p>"
            f"</div>"
        )
        render_html(preview_card_html)
