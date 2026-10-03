from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Movie_Lab_Assignment_2_Report.pdf"
SHOT = ROOT / "screenshots"

INK = colors.HexColor("#20251d")
MUTED = colors.HexColor("#687064")
LIME = colors.HexColor("#91aa4a")
PAPER = colors.HexColor("#f4f3ee")
LINE = colors.HexColor("#d6d9cd")


class Report(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                         topMargin=19*mm, bottomMargin=18*mm, title="Movie Lab Assignment 2")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=3*mm, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="report", frames=frame, onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setFillColor(LIME)
        canvas.rect(18*mm, h-11*mm, 15*mm, 1.1*mm, fill=1, stroke=0)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(w-18*mm, h-11.2*mm, "FRAME.  /  ASSIGNMENT 02")
        canvas.setStrokeColor(LINE)
        canvas.line(18*mm, 13*mm, w-18*mm, 13*mm)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(18*mm, 8.5*mm, "MOVIE DISCOVERY / UI REDESIGN")
        canvas.drawRightString(w-18*mm, 8.5*mm, f"{doc.page:02d}")
        canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleFrame", fontName="Helvetica-Bold", fontSize=29,
                          leading=33, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="SubtitleFrame", fontName="Helvetica", fontSize=11,
                          leading=16, textColor=MUTED, spaceAfter=13))
styles.add(ParagraphStyle(name="SectionFrame", fontName="Helvetica-Bold", fontSize=16,
                          leading=20, textColor=INK, spaceBefore=9, spaceAfter=6))
styles.add(ParagraphStyle(name="SubheadFrame", fontName="Helvetica-Bold", fontSize=11,
                          leading=14, textColor=INK, spaceBefore=4, spaceAfter=3))
styles.add(ParagraphStyle(name="BodyFrame", fontName="Helvetica", fontSize=9.4,
                          leading=14, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="BulletFrame", fontName="Helvetica", fontSize=9,
                          leading=13, leftIndent=12, firstLineIndent=-9,
                          textColor=INK, spaceAfter=3))
styles.add(ParagraphStyle(name="CaptionFrame", fontName="Helvetica", fontSize=8,
                          leading=11, textColor=MUTED, spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="SmallFrame", fontName="Helvetica", fontSize=8,
                          leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name="EyebrowFrame", fontName="Helvetica-Bold", fontSize=8,
                          leading=11, textColor=LIME, spaceAfter=5))


def para(text, style="BodyFrame"):
    return Paragraph(text, styles[style])


def bullet(text):
    return para(f"<font color='#91aa4a'>/</font>  {text}", "BulletFrame")


def image(path, max_width, max_height=None):
    img = Image(str(path))
    scale = min(max_width / img.imageWidth,
                (max_height / img.imageHeight) if max_height else 1)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    img.hAlign = "CENTER"
    return img


def screenshot_cell(filename, caption, width):
    return [image(SHOT / filename, width), para(caption, "CaptionFrame")]


doc = Report(str(OUT))
story = []

# Page 1: purpose, visual language and the API-key entry point.
story += [para("PROJECT / UI REDESIGN", "EyebrowFrame"),
          para("Movie Lab, reimagined.", "TitleFrame"),
          para("Assignment 2  /  A personal cinema for discovering films through real TMDB data.", "SubtitleFrame"),
          para("Introduction", "SectionFrame"),
          para("FRAME. is a custom movie-discovery interface built on the existing Vue and TMDB project. The redesign carries the same live movie functionality into a more considered, cinematic visual system.", "BodyFrame"),
          para("UI Changes", "SectionFrame"),
          bullet("Replaced the starter styling with a deep charcoal palette, editorial serif headlines, small mono labels and acid-green accents."),
          bullet("Created a welcome and API-key connection screen, then a matching connected-state hero with search and key-change controls."),
          bullet("Redesigned the catalog, result counts, responsive movie cards, poster fallback, rating badges and page controls."),
          bullet("Added custom loading skeletons, empty-result guidance, API error and retry panels, focus visibility, reduced-motion support and a matching favicon."),
          para("Why I Made These Changes", "SectionFrame"),
          para("The original page had one visual language for every state. A consistent identity makes the hand-off from connecting a key to browsing feel intentional. Strong poster framing helps people scan a catalog; restrained metadata and excerpts keep titles and ratings easy to find without competing with the artwork.", "BodyFrame"),
          para("01 / The first connection and the live popular collection", "SubheadFrame")]
left = screenshot_cell("connection.jpg", "<b>01</b>  Welcome view: clear key entry, privacy note and a direct link to request a TMDB key.", 78*mm)
right = screenshot_cell("popular.jpg", "<b>02</b>  Connected catalog: the search hero, popular section and actual TMDB poster cards.", 78*mm)
shots = Table([[left, right]], colWidths=[85*mm, 85*mm], hAlign="LEFT")
shots.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 5*mm),
                           ("TOPPADDING", (0, 0), (-1, -1), 2*mm),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
story += [shots, PageBreak()]

# Page 2: real search, cards and usability outcomes.
story += [para("02 / REAL SEARCH, MORE LEGIBLE RESULTS", "EyebrowFrame"),
          para("From a title to a whole collection.", "TitleFrame"),
          para("Search results keep the same visual language as the popular catalog, while making the active query and result count explicit.", "SubtitleFrame"),
          image(SHOT / "search.jpg", 174*mm, 105*mm),
          para("03  /  Live TMDB search for Dune. The first results show poster artwork, year, rating, title, synopsis and direct TMDB links.", "CaptionFrame"),
          Spacer(1, 5*mm),
          para("Effect on Appearance and Usability", "SectionFrame"),
          bullet("A restrained dark palette gives movie posters visual weight; the green rating markers remain distinct from supporting text."),
          bullet("Responsive grids reduce card count as the viewport narrows, while card content remains readable and links retain visible keyboard focus."),
          bullet("Search, popular browsing, pagination, empty results and API errors have clear labels and next actions. The key remains in memory and is cleared on reload or when changed."),
          para("The 390px layout was checked after correcting an oversized mobile headline that initially caused horizontal overflow. The responsive page now remains within the viewport.", "BodyFrame"),
          para("TMDB results and posters shown above were loaded live during browser verification; no sample movie data was substituted.", "SmallFrame"),
          PageBreak()]

# Page 3: error and empty states plus conclusion.
story += [para("03 / EVERY STATE HAS A NEXT STEP", "EyebrowFrame"),
          para("Clear guidance when results are missing.", "TitleFrame"),
          para("Empty and API-error views use the same design language, with concise explanations and useful recovery actions.", "SubtitleFrame")]
left = screenshot_cell("empty.jpg", "<b>04</b>  Empty search: confirms zero films and offers a return to popular titles.", 78*mm)
right = screenshot_cell("error.jpg", "<b>05</b>  Invalid API key: explains rejection and provides a retry route.", 78*mm)
shots = Table([[left, right]], colWidths=[85*mm, 85*mm], hAlign="LEFT")
shots.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 5*mm),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
story += [shots, Spacer(1, 5*mm),
          para("Verification", "SectionFrame"),
          para("The production build completed. In the live browser, popular movies loaded, a Dune search returned results, and pagination advanced to page 2. A no-match search displayed the empty state; a deliberately invalid API key displayed TMDB's 401 message. The page was also checked at a 390px mobile viewport.", "BodyFrame"),
          para("Conclusion", "SectionFrame"),
          para("FRAME. gives Movie Lab a recognizable identity across connection, discovery, search, loading and recovery states. It retains real TMDB behavior while making the interface clearer, more cohesive and more comfortable to use on smaller screens.", "BodyFrame"),
          Spacer(1, 2*mm),
          para("Technology: Vue 3 + Vite  /  Data: TMDB API  /  Delivery: static site, GitHub Pages-ready", "SmallFrame")]

doc.build(story)
print(OUT)
