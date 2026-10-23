"""Construction de la présentation GHCG à partir du template PLB.

Repris de la formation PyTorch (DLPT) : même template, même charte, mêmes règles.

Chaque slide est créée à partir d'un layout du template (polices et décors
viennent du masque). Les schémas et le code sont dessinés avec des formes
simples pour rester modifiables dans PowerPoint.

Charte (reprise de la formation PyTorch) : le template est gardé, mais le fond suit la
proposition reçue de PLB. Les slides de titre, de section, de transition et de
clôture ont un fond marine ; les slides de contenu ont un fond blanc. Le logo
PLB est placé en haut à droite de chaque slide. Le fond et le logo sont posés à
la construction, le fichier du template n'est pas modifié. Sur fond blanc, les
textes et les traits clairs dessinés pour l'ancien fond bleu sont assombris
(voir _apply_charte) ; les formes pleines (boîtes, grilles, code) gardent leurs
couleurs.

Animations : sur les slides de contenu, chaque élément apparaît au clic avec
l'effet d'entrée « Dissolve In ». Chaque dessin déclare une étape (un clic) ;
with deck.together(): regroupe plusieurs dessins dans le même clic.
Le speech des notes doit compter une partie pour l'arrivée de la slide, puis
une partie par clic.
"""

import re
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_COLOR_TYPE, MSO_FILL
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = next((ROOT / "template").glob("*.pptx"))
ASSETS = Path(__file__).resolve().parent / "assets"
LOGO_ON_DARK = ASSETS / "logo_plb_fond_sombre.png"
LOGO_ON_LIGHT = ASSETS / "logo_plb_fond_clair.png"

# Palette du thème du template (ppt/theme/theme1.xml)
DARK_BG = RGBColor(0x1E, 0x55, 0xB8)
LIGHT_BG = RGBColor(0x6C, 0xAB, 0xF0)
BLUE = RGBColor(0x16, 0x74, 0xDC)
GREEN = RGBColor(0x5A, 0xE4, 0x95)
INDIGO = RGBColor(0x42, 0x53, 0xEF)
SKY = RGBColor(0x63, 0xC0, 0xF8)
DEEP = RGBColor(0x00, 0x70, 0xC0)
NAVY = RGBColor(0x00, 0x20, 0x60)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
# Fond des blocs de code : bleu nuit dérivé de NAVY, pour un contraste fort
CODE_BG = RGBColor(0x0B, 0x1E, 0x4A)
CODE_COMMENT = RGBColor(0x9C, 0xC7, 0xF5)
# Suggestion grisée de Copilot dans les blocs de code
GHOST = RGBColor(0x8A, 0x93, 0xA6)
# Carte « prompt » : fond bleu très clair, texte marine
PROMPT_BG = RGBColor(0xE8, 0xF1, 0xFD)
# Tableaux : lignes alternées
ROW_ALT = RGBColor(0xF2, 0xF6, 0xFC)

# Charte du 03/10/2026 : fond marine (slides de titre, section, transition, clôture),
# fond blanc (contenu). INK sert aussi de couleur de texte sur fond blanc.
INK = RGBColor(0x0C, 0x1A, 0x37)
INK_GREEN = RGBColor(0x0E, 0x8A, 0x4F)
# Sur fond blanc : blanc -> marine, bleu ciel -> bleu, vert clair -> vert foncé
LIGHT_REMAP = {"FFFFFF": INK, "63C0F8": BLUE, "5AE495": INK_GREEN}

MONO = "Courier New"

# Numéros des layouts du template (1 = premier layout du masque)
L_TITLE = 2
L_AGENDA = 10
L_SECTION_A = 7
L_SECTION_B = 8
L_CONTENT = 14
L_STATEMENT = 37
L_BIG = 34
L_COMPARE = 44
L_PROCESS = 48
L_LIST3 = 50
L_LIST4 = 51
L_CLOSING = 62
DARK_LAYOUTS = {L_TITLE, L_SECTION_A, L_SECTION_B, L_BIG, L_CLOSING}
# Logo en haut à gauche là où le décor du template occupe le coin haut droit
LOGO_TOP_LEFT = {L_TITLE, L_SECTION_A, L_CLOSING}

# Effet d'entrée « Dissolve In » de PowerPoint
DISSOLVE_PRESET_ID = "9"
DISSOLVE_DURATION_MS = "500"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


# Mentions interdites dans ce que voient ou entendent les stagiaires (la ligne Source des notes est exclue) :
# les chemins internes du dépôt de préparation. Les liens des documentations officielles sont permis.
# Sensible à la casse : AGENTS.MD (consignes du dépôt) est interdit, AGENTS.md (format Copilot) est permis
SOURCE_MENTION = re.compile(r"plan/|AGENTS\.MD|couverture\.md")


# « Module 3 », « module 5 » : numéros de parties de la formation, à ne pas afficher (nn.Module reste permis)
COURSE_MODULE = re.compile(r"\b[Mm]odules? \d")


@dataclass
class Notes:
    """Notes du formateur : speech (arrivée + un texte par clic), question, source."""
    speech: list
    question: str
    source: str


def notes(speech, question, source):
    if isinstance(speech, str):
        speech = [speech]
    return Notes(list(speech), question, source)


def render_notes(n):
    lines = ["Speech"]
    for i, part in enumerate(n.speech):
        prefix = "(Arrivée de la slide)" if i == 0 else f"[Clic {i}]"
        lines.append(f"{prefix} {part}")
    lines.append("")
    lines.append(f"Question au groupe : {n.question}")
    lines.append("")
    lines.append(f"Source : {n.source}")
    return "\n".join(lines)


def timing_xml(steps):
    """Élément p:timing : un clic par étape, effet Dissolve In sur chaque cible.

    Une cible est (shape_id, paragraphe) ; paragraphe vaut None pour la forme entière.
    """
    ids = iter(range(1, 10_000))

    def target(spid, paragraph):
        if paragraph is None:
            return f'<p:spTgt spid="{spid}"/>'
        return (f'<p:spTgt spid="{spid}"><p:txEl><p:pRg st="{paragraph}" end="{paragraph}"/>'
                f'</p:txEl></p:spTgt>')

    def effect(spid, paragraph, first):
        node = "clickEffect" if first else "withEffect"
        tgt = target(spid, paragraph)
        return (
            f'<p:par><p:cTn id="{next(ids)}" presetID="{DISSOLVE_PRESET_ID}" presetClass="entr" '
            f'presetSubtype="0" fill="hold" grpId="0" nodeType="{node}">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{next(ids)}" dur="1" fill="hold">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl>{tgt}</p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName>'
            f'</p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
            f'<p:animEffect transition="in" filter="dissolve"><p:cBhvr>'
            f'<p:cTn id="{next(ids)}" dur="{DISSOLVE_DURATION_MS}"/>'
            f'<p:tgtEl>{tgt}</p:tgtEl></p:cBhvr></p:animEffect>'
            f'</p:childTnLst></p:cTn></p:par>'
        )

    root_id, seq_id = next(ids), next(ids)
    clicks = []
    for step in steps:
        click_id, group_id = next(ids), next(ids)
        effects = "".join(effect(spid, par, i == 0) for i, (spid, par) in enumerate(step))
        clicks.append(
            f'<p:par><p:cTn id="{click_id}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
            f'</p:stCondLst><p:childTnLst><p:par><p:cTn id="{group_id}" fill="hold"><p:stCondLst>'
            f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>{effects}</p:childTnLst></p:cTn></p:par>'
            f'</p:childTnLst></p:cTn></p:par>'
        )
    return (
        f'<p:timing xmlns:p="{P_NS}"><p:tnLst><p:par>'
        f'<p:cTn id="{root_id}" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
        f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="{seq_id}" dur="indefinite" nodeType="mainSeq">'
        f'<p:childTnLst>{"".join(clicks)}</p:childTnLst></p:cTn>'
        f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        f'</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>'
        f'{{BLDLST}}</p:timing>'
    )


class Deck:
    def __init__(self):
        self.prs = Presentation(str(TEMPLATE))
        self._drop_template_slides()
        self.section_count = 0
        self.snippets = []
        self.code_sizes = []
        self.problems = []
        self.animation_report = []
        self._slide = None
        self._layout = None
        self._notes = None
        self._animated = False
        self._steps = []
        self._together = None
        self._target = None

    def _drop_template_slides(self):
        slide_ids = self.prs.slides._sldIdLst
        for slide_id in list(slide_ids):
            self.prs.part.drop_rel(slide_id.rId)
            slide_ids.remove(slide_id)

    def save(self, path):
        self._finish_slide()
        self.prs.save(str(path))

    def appendix(self, titles):
        """Place les détails optionnels après la clôture, masqués en diaporama.

        Le rapport d'animations et les extraits suivent la nouvelle numérotation.
        """
        self._finish_slide()
        slides = list(self.prs.slides)
        appendix = [i for i, slide in enumerate(slides)
                    if any(shape.has_text_frame and shape.text == title
                           for title in titles for shape in slide.shapes)]
        order = [i for i in range(len(slides)) if i not in appendix] + appendix
        numbering = {old + 1: new + 1 for new, old in enumerate(order)}
        ids = self.prs.slides._sldIdLst
        elements = list(ids)
        for element in elements:
            ids.remove(element)
        for i in order:
            ids.append(elements[i])
        for i in appendix:
            slides[i]._element.set("show", "0")
        self.animation_report = sorted((numbering[n], steps) for n, steps in self.animation_report)
        self.snippets = [(numbering[n], code, runnable, lang) for n, code, runnable, lang in self.snippets]
        self.code_sizes = [(numbering[n], size) for n, size in self.code_sizes]

    # ------------------------------------------------------------------
    # Slide courante, étapes d'animation et notes

    def _new_slide(self, layout_number, speaker_notes, animated):
        self._finish_slide()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[layout_number - 1])
        self._slide = slide
        self._layout = layout_number
        self._notes = speaker_notes
        self._animated = animated
        self._steps = []
        return slide

    def _check_no_module_word(self, number):
        """Les parties de la formation ne s'appellent pas « module » à l'écran (demande du 03/10/2026)."""
        for shape in self._slide.shapes:
            if shape.has_text_frame and COURSE_MODULE.search(shape.text_frame.text):
                self.problems.append(f"slide {number} : « module » affiché ({shape.text_frame.text[:50]})")

    def _check_no_source(self, number):
        """Les sources sont réservées au formateur : ni à l'écran, ni dans le speech, ni dans la question."""
        visible = [sh.text_frame.text for sh in self._slide.shapes if sh.has_text_frame]
        spoken = list(self._notes.speech) + [self._notes.question]
        for text in visible + spoken:
            for m in SOURCE_MENTION.finditer(text):
                self.problems.append(f"slide {number} : mention de source « {m.group(0)} » dans « {text[:60]} »")

    def _finish_slide(self):
        if self._slide is None:
            return
        number = len(self.prs.slides)
        if not isinstance(self._notes, Notes):
            raise TypeError(f"slide {number} : notes à construire avec notes(speech, question, source)")
        expected = 1 + len(self._steps)
        if len(self._notes.speech) != expected:
            self.problems.append(
                f"slide {number} : speech en {len(self._notes.speech)} parties, "
                f"attendu {expected} (arrivée + {len(self._steps)} clics)")
        self._check_no_source(number)
        self._check_no_module_word(number)
        self._apply_charte()
        self._slide.notes_slide.notes_text_frame.text = render_notes(self._notes)
        if self._steps:
            self._write_timing()
        self.animation_report.append((number, self._describe_steps()))
        self._slide = None

    def _apply_charte(self):
        """Fond, couleurs du texte et logo selon la charte : marine ou blanc."""
        slide = self._slide
        dark = self._layout in DARK_LAYOUTS
        background = slide.background.fill
        background.solid()
        background.fore_color.rgb = INK if dark else WHITE
        for shape in slide.shapes:
            if shape.is_placeholder:
                # Texte hérité du layout, prévu pour l'ancien fond : couleur explicite
                self._recolor_text(shape, {}, WHITE if dark else INK, force=dark)
            elif not dark:
                filled = getattr(shape, "fill", None) is not None and shape.fill.type == MSO_FILL.SOLID
                if not filled and shape.has_text_frame:
                    self._recolor_text(shape, LIGHT_REMAP, None)
                self._recolor_line(shape)
        logo = LOGO_ON_DARK if dark else LOGO_ON_LIGHT
        if self._layout in LOGO_TOP_LEFT:
            slide.shapes.add_picture(str(logo), Inches(0.75), Inches(0.35), height=Inches(0.5))
        else:
            slide.shapes.add_picture(str(logo), Inches(12.05), Inches(0.22), height=Inches(0.4))

    @staticmethod
    def _rgb(color):
        try:
            return str(color.rgb) if color.type == MSO_COLOR_TYPE.RGB else None
        except AttributeError:
            return None

    def _recolor_text(self, shape, remap, default, force=False):
        """Recolore les runs : remap pour les couleurs connues, default pour les couleurs héritées."""
        if not shape.has_text_frame:
            return
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                rgb = self._rgb(run.font.color)
                if force and default is not None:
                    run.font.color.rgb = default
                elif rgb is None:
                    if default is not None:
                        run.font.color.rgb = default
                elif rgb in remap:
                    run.font.color.rgb = remap[rgb]
            pPr = paragraph._p.pPr
            if pPr is not None and not force:
                for srgb in pPr.iter(qn("a:srgbClr")):
                    if srgb.get("val") in remap:
                        srgb.set("val", str(remap[srgb.get("val")]))

    @staticmethod
    def _recolor_line(shape):
        """Traits clairs (flèches, courbes, contours) assombris pour le fond blanc, lus dans le XML."""
        sp_pr = shape._element.find(qn("p:spPr"))
        line = sp_pr.find(qn("a:ln")) if sp_pr is not None else None
        if line is None:
            return
        for srgb in line.iter(qn("a:srgbClr")):
            if srgb.get("val") in LIGHT_REMAP:
                srgb.set("val", str(LIGHT_REMAP[srgb.get("val")]))

    def _write_timing(self):
        spids_by_paragraph = {spid for step in self._steps for spid, par in step if par is not None}
        whole_sp = set()
        graphics = set()
        for step in self._steps:
            for spid, par in step:
                tag = self._shape_tag(spid) if par is None else None
                if tag == "sp":
                    whole_sp.add(spid)
                elif tag == "graphicFrame":
                    graphics.add(spid)
        bld = "".join(f'<p:bldP spid="{spid}" grpId="0" build="p"/>' for spid in sorted(spids_by_paragraph))
        bld += "".join(f'<p:bldP spid="{spid}" grpId="0" animBg="1"/>' for spid in sorted(whole_sp))
        # Tableaux : construits d'un bloc
        bld += "".join(f'<p:bldGraphic spid="{spid}" grpId="0"><p:bldAsOne/></p:bldGraphic>'
                       for spid in sorted(graphics))
        xml = timing_xml(self._steps).replace("{BLDLST}", f"<p:bldLst>{bld}</p:bldLst>" if bld else "")
        timing = etree.fromstring(xml)
        sld = self._slide._element
        ext = sld.find(qn("p:extLst"))
        if ext is not None:
            ext.addprevious(timing)
        else:
            sld.append(timing)

    def _shape_tag(self, spid):
        for shape in self._slide.shapes:
            if shape.shape_id == spid:
                return etree.QName(shape._element).localname
        return None

    def _describe_steps(self):
        texts = {shape.shape_id: shape for shape in self._slide.shapes}
        described = []
        for step in self._steps:
            parts = []
            for spid, par in step:
                shape = texts[spid]
                if shape.has_text_frame and shape.text_frame.text.strip():
                    paragraphs = shape.text_frame.paragraphs
                    text = paragraphs[par].text if par is not None else shape.text_frame.text
                    parts.append(text.replace("\n", " / ")[:60])
                else:
                    parts.append(f"<{etree.QName(shape._element).localname}>")
            described.append(" + ".join(parts))
        return described

    def _add(self, targets, join=False):
        """Enregistre des cibles d'animation : nouvelle étape, ou ajout à la dernière."""
        if not self._animated:
            return
        if self._target is not None:
            self._steps[self._target - 1].extend(targets)
        elif self._together is not None:
            self._together.extend(targets)
        elif join and self._steps:
            self._steps[-1].extend(targets)
        else:
            self._steps.append(list(targets))

    @contextmanager
    def together(self):
        """Tout ce qui est dessiné dans ce bloc apparaît au même clic."""
        outer = self._together
        self._together = []
        try:
            yield
        finally:
            group, self._together = self._together, outer
            if group:
                self._add(group)

    @property
    def clicks(self):
        """Nombre de clics déjà créés sur la slide courante."""
        return len(self._steps)

    @contextmanager
    def at_click(self, number):
        """Ce qui est dessiné dans ce bloc apparaît au clic `number`, déjà créé."""
        previous, self._target = self._target, number
        try:
            yield
        finally:
            self._target = previous

    @contextmanager
    def still(self):
        """Ce qui est dessiné dans ce bloc est visible dès l'arrivée de la slide."""
        animated, self._animated = self._animated, False
        try:
            yield
        finally:
            self._animated = animated

    # ------------------------------------------------------------------
    # Outils de base

    @staticmethod
    def _placeholder(slide, idx):
        for ph in slide.placeholders:
            if ph.placeholder_format.idx == idx:
                return ph
        raise KeyError(f"placeholder {idx} absent")

    @staticmethod
    def _remove_empty_placeholders(slide):
        for ph in list(slide.placeholders):
            if not ph.has_text_frame or not ph.text_frame.text.strip():
                ph._element.getparent().remove(ph._element)

    @staticmethod
    def write(text_frame, text, size=None, color=None, bold=None, font=None, align=None):
        """Remplace le contenu d'un cadre texte. Une ligne par paragraphe."""
        lines = text.split("\n") if isinstance(text, str) else list(text)
        text_frame.clear()
        for i, line in enumerate(lines):
            p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
            if align is not None:
                p.alignment = align
            run = p.add_run()
            run.text = line
            if size:
                run.font.size = Pt(size)
            if color is not None:
                run.font.color.rgb = color
            if bold is not None:
                run.font.bold = bold
            if font:
                run.font.name = font

    def fill(self, slide, idx, text, **style):
        ph = self._placeholder(slide, idx)
        self.write(ph.text_frame, text, **style)
        return ph

    # ------------------------------------------------------------------
    # Formes de dessin (coordonnées en pouces)

    def text(self, slide, x, y, w, h, text, size=18, color=WHITE, bold=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=None, join=False):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        tf.margin_left = tf.margin_right = Inches(0.05)
        tf.margin_top = tf.margin_bottom = Inches(0.02)
        self.write(tf, text, size=size, color=color, bold=bold, font=font, align=align)
        self._add([(box.shape_id, None)], join=join)
        return box

    def bullets(self, slide, x, y, w, h, items, size=20, color=WHITE, gap=10, first_join=False):
        """Liste à puces, une puce par clic. Un tuple ("texte", 1) est indenté d'un niveau
        et apparaît avec la puce qui le précède. first_join=True : la première puce
        apparaît avec l'élément dessiné juste avant."""
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.clear()
        for i, item in enumerate(items):
            text, level = item if isinstance(item, tuple) else (item, 0)
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(gap)
            run = p.add_run()
            run.text = text
            run.font.size = Pt(size - 2 * level)
            run.font.color.rgb = color
            pPr = p._p.get_or_add_pPr()
            indent = 0.3 + 0.35 * level
            pPr.set("marL", str(int(Inches(indent))))
            pPr.set("indent", str(int(-Inches(0.3))))
            bullet_color = etree.SubElement(pPr, qn("a:buClr"))
            srgb = etree.SubElement(bullet_color, qn("a:srgbClr"))
            srgb.set("val", "5AE495")
            bullet = etree.SubElement(pPr, qn("a:buChar"))
            bullet.set("char", "•" if level == 0 else "–")
            self._add([(box.shape_id, i)], join=level > 0 or (i == 0 and first_join))
        return box

    def box(self, slide, x, y, w, h, text="", fill=BLUE, color=WHITE, size=16,
            bold=False, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, font=None,
            align=PP_ALIGN.CENTER, join=False):
        shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid()
            shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line
            shp.line.width = Pt(1.5)
        shp.shadow.inherit = False
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            shp.adjustments[0] = 0.12
        tf = shp.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.08)
        if text:
            self.write(tf, text, size=size, color=color, bold=bold, font=font, align=align)
        self._add([(shp.shape_id, None)], join=join)
        return shp

    def arrow(self, slide, x1, y1, x2, y2, color=WHITE, width=2.0, head=True, join=True):
        """Flèche. Par défaut, elle apparaît avec l'élément dessiné juste avant."""
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                          Inches(x2), Inches(y2))
        conn.line.color.rgb = color
        conn.line.width = Pt(width)
        if head:
            ln = conn.line._get_or_add_ln()
            tail = etree.SubElement(ln, qn("a:tailEnd"))
            tail.set("type", "triangle")
            tail.set("w", "med")
            tail.set("len", "med")
        self._add([(conn.shape_id, None)], join=join)
        return conn

    def code(self, slide, x, y, w, h, source, size=17, runnable=True, lang="python", join=False,
             ghost_from=None):
        """Bloc de code : fond bleu nuit, police à chasse fixe, commentaires en bleu clair.

        runnable=True : l'extrait est autonome et sera exécuté par check_snippets.py.
        ghost_from=n : à partir de la ligne n (0 = première), les lignes sont en gris italique,
        comme la suggestion grisée (ghost text) de Copilot.
        """
        self.snippets.append((len(self.prs.slides), source, runnable and lang == "python", lang))
        lines = source.strip("\n").split("\n")
        if len(lines) > 15:
            self.problems.append(f"slide {len(self.prs.slides)} : code de {len(lines)} lignes (max 15)")
        # Pas de retour à la ligne dans le code : on réduit la police pour que la
        # ligne la plus longue et toutes les lignes tiennent dans le bloc.
        # Courier New : un caractère fait 0.6 em de large ; une ligne fait 1.2 em de haut.
        longest = max(len(line) for line in lines)
        fit_width = (w - 0.6) * 72 / (0.6 * longest)
        fit_height = (h - 0.3) * 72 / (1.2 * len(lines))
        size = int(min(size, fit_width, fit_height) * 2) / 2
        self.code_sizes.append((len(self.prs.slides), size))
        if size < 15:
            self.problems.append(f"slide {len(self.prs.slides)} : code à {size} pt (minimum 15)")
        shp = self.box(slide, x, y, w, h, fill=CODE_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, join=join)
        shp.adjustments[0] = 0.04
        tf = shp.text_frame
        tf.word_wrap = False
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.clear()
        for i, line in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            run = p.add_run()
            run.text = line if line else " "
            run.font.name = MONO
            run.font.size = Pt(size)
            is_comment = line.strip().startswith(("#", "//")) and lang in ("python", "shell", "jsonc")
            is_ghost = ghost_from is not None and i >= ghost_from
            run.font.color.rgb = GHOST if is_ghost else CODE_COMMENT if is_comment else WHITE
            run.font.italic = is_ghost
            run.font.bold = False
        return shp

    def prompt(self, slide, x, y, w, h, text, label="Prompt", size=16, join=False):
        """Carte de prompt : étiquette verte, puis le texte du prompt sur fond bleu très clair.

        La carte et son étiquette apparaissent au même clic. Le texte doit tenir dans la carte :
        estimation à 0.55 em par caractère (Poppins) et 1.25 em par ligne.
        """
        lines = text.strip("\n").split("\n")
        per_line = max(1, int((w - 0.4) * 72 / (0.55 * size)))
        needed = sum(max(1, -(-len(line) // per_line)) for line in lines) * size * 1.25 / 72 + 0.55
        if needed > h:
            self.problems.append(f"slide {len(self.prs.slides)} : prompt trop long pour sa carte "
                                 f"({needed:.1f} pouces pour {h})")
        with self.together():
            card = self.box(slide, x, y, w, h, fill=PROMPT_BG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, join=join)
            card.adjustments[0] = 0.05
            tf = card.text_frame
            tf.vertical_anchor = MSO_ANCHOR.TOP
            tf.margin_left = tf.margin_right = Inches(0.2)
            tf.margin_top = Inches(0.45)
            self.write(tf, lines, size=size, color=INK, align=PP_ALIGN.LEFT)
            self.box(slide, x + 0.2, y + 0.1, 1.3, 0.3, label, fill=GREEN, color=NAVY, size=11, bold=True)
        return card

    def table(self, slide, x, y, w, rows, col_widths=None, size=14, row_h=0.42, join=False):
        """Tableau : première ligne en en-tête (bleu, texte blanc), lignes alternées ; un seul clic."""
        n_rows, n_cols = len(rows), len(rows[0])
        frame = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(row_h * n_rows))
        table = frame.table
        widths = col_widths or [w / n_cols] * n_cols
        for c, width in enumerate(widths):
            table.columns[c].width = Inches(width)
        for r, row in enumerate(rows):
            table.rows[r].height = Inches(row_h)
            for c, value in enumerate(row):
                cell = table.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = BLUE if r == 0 else (ROW_ALT if r % 2 == 0 else WHITE)
                cell.margin_left = cell.margin_right = Inches(0.08)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                self.write(cell.text_frame, str(value), size=size, color=WHITE if r == 0 else INK,
                           bold=(r == 0 or c == 0))
        # Pas de style de tableau du thème : les couleurs posées ci-dessus suffisent
        tbl_pr = table._tbl.tblPr
        tbl_pr.set("firstRow", "0")
        tbl_pr.set("bandRow", "0")
        self._add([(frame.shape_id, None)], join=join)
        return frame

    def grid(self, slide, x, y, values, cell=0.55, fill=BLUE, color=WHITE, size=14,
             highlight=(), highlight_fill=GREEN, highlight_color=NAVY, join=False):
        """Tenseur 2D dessiné case par case, qui apparaît en un seul clic.
        highlight : ensemble de (ligne, colonne)."""
        cells = []
        with self.still():
            for r, row in enumerate(values):
                for c, value in enumerate(row):
                    on = (r, c) in highlight
                    shp = self.box(slide, x + c * cell, y + r * cell, cell - 0.05, cell - 0.05,
                                   str(value), fill=highlight_fill if on else fill,
                                   color=highlight_color if on else color, size=size,
                                   shape=MSO_SHAPE.RECTANGLE)
                    cells.append((shp.shape_id, None))
        self._add(cells, join=join)

    def flow(self, slide, x, y, w, h, labels, fills=None, colors=None, size=16, gap=0.45):
        """Suite de boîtes reliées par des flèches, de gauche à droite, une boîte par clic.
        Chaque flèche apparaît avec la boîte vers laquelle elle pointe."""
        n = len(labels)
        bw = (w - gap * (n - 1)) / n
        for i, label in enumerate(labels):
            bx = x + i * (bw + gap)
            fill = fills[i] if fills else BLUE
            color = colors[i] if colors else WHITE
            with self.together():
                if i > 0:
                    self.arrow(slide, bx - gap + 0.05, y + h / 2, bx - 0.05, y + h / 2)
                self.box(slide, bx, y, bw, h, label, fill=fill, color=color, size=size, bold=True)

    def polyline(self, slide, points, color=WHITE, width=2.5, dash=False, join=True):
        """Ligne brisée passant par des points (x, y) en pouces."""
        builder = slide.shapes.build_freeform(Inches(points[0][0]), Inches(points[0][1]),
                                              scale=1.0)
        builder.add_line_segments([(Inches(px), Inches(py)) for px, py in points[1:]],
                                  close=False)
        shp = builder.convert_to_shape()
        shp.fill.background()
        shp.line.color.rgb = color
        shp.line.width = Pt(width)
        if dash:
            shp.line.dash_style = 4  # MSO_LINE_DASH_STYLE.DASH
        shp.shadow.inherit = False
        self._add([(shp.shape_id, None)], join=join)
        return shp

    def plot(self, slide, x, y, w, h, func, x_range, y_range, color=GREEN, width=3,
             axes=True, dash=False, samples=60, join=False):
        """Trace y = func(t) dans un cadre (x, y, w, h), avec des axes simples, en un clic."""
        (t0, t1), (v0, v1) = x_range, y_range

        def to_slide(t, v):
            v = min(max(v, v0), v1)
            return x + (t - t0) / (t1 - t0) * w, y + h - (v - v0) / (v1 - v0) * h

        shapes = []
        with self.still():
            if axes:
                zero_y = to_slide(t0, 0.0)[1] if v0 <= 0 <= v1 else y + h
                zero_x = to_slide(0.0, v0)[0] if t0 <= 0 <= t1 else x
                shapes.append(self.arrow(slide, x, zero_y, x + w, zero_y, color=SKY, width=1.25))
                shapes.append(self.arrow(slide, zero_x, y + h, zero_x, y, color=SKY, width=1.25))
            points = [to_slide(t0 + (t1 - t0) * i / samples, func(t0 + (t1 - t0) * i / samples))
                      for i in range(samples + 1)]
            shapes.append(self.polyline(slide, points, color=color, width=width, dash=dash))
        self._add([(s.shape_id, None) for s in shapes], join=join)
        return shapes[-1]

    # ------------------------------------------------------------------
    # Types de slides

    def title_slide(self, title, subtitle, info, speaker_notes):
        slide = self._new_slide(L_TITLE, speaker_notes, animated=False)
        self.fill(slide, 0, title)
        self.fill(slide, 1, subtitle, size=22)
        self.fill(slide, 11, info, size=14)
        self._remove_empty_placeholders(slide)
        return slide

    def agenda(self, title, items, speaker_notes):
        """Jusqu'à six entrées, colonne de gauche puis colonne de droite, une entrée par clic."""
        slide = self._new_slide(L_AGENDA, speaker_notes, animated=True)
        self.fill(slide, 0, title)
        slots = [(14, 13), (16, 15), (18, 17), (20, 19), (22, 21), (24, 23)]
        for i, ((num_idx, text_idx), item) in enumerate(zip(slots, items)):
            number = self.fill(slide, num_idx, f"{i + 1:02d}", size=16)
            label = self.fill(slide, text_idx, item, size=16)
            self._add([(number.shape_id, None), (label.shape_id, None)])
        self._remove_empty_placeholders(slide)
        return slide

    def section(self, title, speaker_notes):
        layout = L_SECTION_A if self.section_count % 2 == 0 else L_SECTION_B
        self.section_count += 1
        slide = self._new_slide(layout, speaker_notes, animated=False)
        self.fill(slide, 0, title)
        self._remove_empty_placeholders(slide)
        return slide

    def _items(self, slide, title, items, slots):
        self.fill(slide, 0, title)
        for (head_idx, body_idx), (head, body) in zip(slots, items):
            head_ph = self.fill(slide, head_idx, head, size=20)
            body_ph = self.fill(slide, body_idx, body, size=16)
            self._add([(head_ph.shape_id, None), (body_ph.shape_id, None)])
        self._remove_empty_placeholders(slide)
        return slide

    def list3(self, title, items, speaker_notes):
        """Titre à gauche, trois blocs (titre + texte) à droite, un bloc par clic."""
        slide = self._new_slide(L_LIST3, speaker_notes, animated=True)
        return self._items(slide, title, items, [(13, 14), (28, 29), (30, 31)])

    def list4(self, title, items, speaker_notes):
        """Quatre blocs (titre + texte) en grille, un bloc par clic, ligne par ligne."""
        slide = self._new_slide(L_LIST4, speaker_notes, animated=True)
        return self._items(slide, title, items, [(13, 14), (21, 22), (23, 24), (25, 26)])

    def process3(self, title, steps, speaker_notes):
        """Trois étapes de gauche à droite, une étape par clic."""
        slide = self._new_slide(L_PROCESS, speaker_notes, animated=True)
        self.fill(slide, 0, title)
        slots = [(28, 13, 14), (29, 32, 31), (30, 34, 33)]
        for i, ((num_idx, head_idx, body_idx), (head, body)) in enumerate(zip(slots, steps)):
            num = self.fill(slide, num_idx, str(i + 1), size=12)
            head_ph = self.fill(slide, head_idx, head, size=20)
            body_ph = self.fill(slide, body_idx, body, size=16)
            self._add([(num.shape_id, None), (head_ph.shape_id, None), (body_ph.shape_id, None)])
        self._remove_empty_placeholders(slide)
        return slide

    def compare(self, title, left_head, left_items, right_head, right_items, speaker_notes):
        """Deux colonnes, une puce par clic ; chaque en-tête arrive avec la première puce de sa colonne."""
        slide = self._new_slide(L_COMPARE, speaker_notes, animated=True)
        self.fill(slide, 0, title)
        for idx in (13, 14):
            ph = self._placeholder(slide, idx)
            ph._element.getparent().remove(ph._element)
        left = self.fill(slide, 1, left_head, size=18)
        self._add([(left.shape_id, None)])
        self.bullets(slide, 0.95, 3.1, 5.6, 3.4, left_items, size=18, first_join=True)
        right = self.fill(slide, 3, right_head, size=18)
        self._add([(right.shape_id, None)])
        self.bullets(slide, 6.75, 3.1, 5.6, 3.4, right_items, size=18, first_join=True)
        self._remove_empty_placeholders(slide)
        return slide

    def statement(self, text, speaker_notes):
        slide = self._new_slide(L_STATEMENT, speaker_notes, animated=True)
        ph = self.fill(slide, 13, text, size=36, bold=True)
        self._add([(ph.shape_id, None)])
        self._remove_empty_placeholders(slide)
        return slide

    def transition(self, kind, name, filename, minutes, speaker_notes):
        """Slide de passage vers une démo ou un TP : nom du fichier et durée."""
        slide = self._new_slide(L_BIG, speaker_notes, animated=False)
        self.fill(slide, 0, kind)
        self.fill(slide, 1, [name, filename, f"Durée : {minutes} min"], size=20)
        self._remove_empty_placeholders(slide)
        return slide

    def content(self, title, speaker_notes):
        """Slide libre : titre en haut (toujours visible), zone utile de y=1.8 à y=6.6 pouces."""
        if not self._title_fits(title):
            self.problems.append(f"slide {len(self.prs.slides) + 1} : titre trop long ({title})")
        slide = self._new_slide(L_CONTENT, speaker_notes, animated=True)
        self.fill(slide, 0, title)
        self._remove_empty_placeholders(slide)
        return slide

    @staticmethod
    def _title_fits(title, width=12.0, size=36):
        """Le titre tient-il sur une ligne ? Mesure réelle en Poppins SemiBold si la police est installée."""
        font_path = Path.home() / "Library/Fonts/Poppins-SemiBold.otf"
        if not font_path.exists():
            return len(title) <= 44
        from PIL import ImageFont
        font = ImageFont.truetype(str(font_path), size)
        return font.getlength(title) / 72 <= width

    def closing(self, title, speaker_notes):
        slide = self._new_slide(L_CLOSING, speaker_notes, animated=False)
        self.fill(slide, 0, title)
        self._remove_empty_placeholders(slide)
        return slide
