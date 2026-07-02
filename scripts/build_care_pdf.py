#!/usr/bin/env python3
"""Generate novuu-prepost-care-instructions.pdf from the canonical care +
FAQ content that also lives on the service pages. Regenerate whenever the
on-site copy changes so the downloadable handout stays in sync.

Fonts (Cormorant Garamond + Jost) and the brand palette mirror the website.

Requirements:
  pip install reportlab
  Brand TTFs in FONT_DIR (defaults to /tmp/fonts), from Google Fonts:
    CormorantGaramond.ttf         ofl/cormorantgaramond/CormorantGaramond[wght].ttf
    CormorantGaramond-Italic.ttf  ofl/cormorantgaramond/CormorantGaramond-Italic[wght].ttf
    Jost.ttf                       ofl/jost/Jost[wght].ttf
  (raw.githubusercontent.com/google/fonts/main/...)

Usage:  python3 scripts/build_care_pdf.py
"""
import html
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    KeepTogether, PageBreak, HRFlowable,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DIR = os.environ.get("FONT_DIR", "/tmp/fonts")
OUT = os.path.join(ROOT, "novuu-prepost-care-instructions.pdf")

# Brand palette (from the site CSS variables)
GREEN = "#2B3A36"
SAGE = "#9DB0A2"
INK = "#1A1A1A"
CREAM = "#F1EAE0"
MUTED = "#5B6660"

pdfmetrics.registerFont(TTFont("Cormorant", os.path.join(FONT_DIR, "CormorantGaramond.ttf")))
pdfmetrics.registerFont(TTFont("Cormorant-Italic", os.path.join(FONT_DIR, "CormorantGaramond-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Jost", os.path.join(FONT_DIR, "Jost.ttf")))

PAGE_W, PAGE_H = letter
MX = 0.85 * inch          # side margins
MT = 0.95 * inch          # top margin
MB = 0.85 * inch          # bottom margin


def esc(s):
    """HTML-unescape site copy to unicode, then XML-escape for Paragraph."""
    s = html.unescape(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---- paragraph styles -------------------------------------------------------
title = ParagraphStyle("title", fontName="Cormorant", fontSize=34, leading=36,
                       textColor=GREEN, alignment=TA_CENTER, spaceAfter=2)
subtitle = ParagraphStyle("subtitle", fontName="Jost", fontSize=11, leading=16,
                          textColor=MUTED, alignment=TA_CENTER, spaceAfter=2)
eyebrow = ParagraphStyle("eyebrow", fontName="Jost", fontSize=8.5, leading=12,
                         textColor=SAGE, alignment=TA_CENTER, spaceBefore=0)
service = ParagraphStyle("service", fontName="Cormorant", fontSize=21, leading=24,
                         textColor=GREEN, spaceBefore=6, spaceAfter=2)
colhead = ParagraphStyle("colhead", fontName="Jost", fontSize=9, leading=13,
                         textColor=GREEN, spaceBefore=8, spaceAfter=3)
bullet = ParagraphStyle("bullet", fontName="Jost", fontSize=9.3, leading=13.4,
                        textColor=INK, leftIndent=13, firstLineIndent=-13,
                        spaceAfter=3)
sectionhead = ParagraphStyle("sectionhead", fontName="Cormorant", fontSize=26,
                             leading=28, textColor=GREEN, alignment=TA_CENTER,
                             spaceAfter=4)
faq_topic = ParagraphStyle("faqtopic", fontName="Cormorant", fontSize=18,
                           leading=21, textColor=GREEN, spaceBefore=8, spaceAfter=3)
faq_q = ParagraphStyle("faqq", fontName="Jost", fontSize=9.6, leading=13,
                       textColor=GREEN, spaceBefore=6, spaceAfter=1)
faq_a = ParagraphStyle("faqa", fontName="Jost", fontSize=9.3, leading=13.6,
                       textColor=INK, spaceAfter=2)


def bul(text):
    return Paragraph(f'<font color="{SAGE}">&#8226;</font>&nbsp;&nbsp;{esc(text)}', bullet)


# ---- content ---------------------------------------------------------------
CARE = [
    ("Neurotoxin", "Botox / Dysport / Daxxify / Xeomin",
     ["Avoid alcohol for at least 24 hours before your appointment",
      "Avoid blood-thinning medications and supplements (aspirin, ibuprofen, fish oil, vitamin E, ginkgo biloba) for 3 days prior, if medically safe to do so",
      "Arrive with a clean face, free of makeup (we have makeup wipes & face wash at the office if needed)",
      "Avoid scheduling your appointment within 2 weeks before a major event",
      "Inform your provider of any medications, supplements, or medical conditions"],
     ["Do not rub, massage, or apply pressure to treated areas for 24 hours",
      "Stay upright for at least 4 hours after treatment",
      "Avoid strenuous exercise for 24 hours",
      "Avoid heat exposure (saunas, hot tubs, hot yoga) for 24 hours",
      "Avoid alcohol for 24 hours",
      "Do not receive facials, massages, or laser treatments for 24 hours",
      "Full results appear after 2 weeks — if you feel you need a touch-up, call our office to schedule between 2–3 weeks post injection"]),
    ("Dermal Filler", None,
     ["Avoid alcohol for at least 24 hours before your appointment",
      "Avoid blood thinners and supplements (aspirin, ibuprofen, fish oil, vitamin E, ginkgo biloba) for 3 days prior, if medically safe to do so",
      "Stay well hydrated in the days leading up to your appointment",
      "Avoid scheduling within 1–2 months of a major event if possible",
      "Inform your provider of any history of cold sores if treating the lip area",
      "Arrive with a clean face, free of makeup (we have makeup wipes & face wash at the office if needed)"],
     ["Expect mild swelling, bruising, and tenderness for up to 14 days",
      "No makeup for 24 hours",
      "Avoid NSAIDs; Tylenol is OK",
      "Do not massage or apply pressure to treated areas unless specifically instructed",
      "Avoid strenuous exercise for 24–48 hours",
      "Avoid alcohol for 24–48 hours",
      "Avoid extreme heat or cold (saunas, hot tubs, ice packs directly on skin) for 48 hours",
      "Sleep on your back with your head slightly elevated for the first 2 nights",
      "Avoid dental procedures, surgeries, and vaccines for 2 weeks following filler",
      "Avoid laser treatments, facials, massages, or face treatments for 2 weeks",
      "Final results are visible once swelling fully resolves, typically within 2–4 weeks — don’t love it or hate it for 2 weeks!"]),
    ("Biostimulators", "Radiesse",
     ["Avoid alcohol for at least 24–48 hours before your appointment",
      "Avoid blood thinners and supplements (aspirin, ibuprofen, fish oil, vitamin E, ginkgo biloba) for 3 days prior, if medically safe to do so",
      "Stay well hydrated in the days leading up to your appointment",
      "Arrive with a clean face, free of makeup (we have makeup wipes & face wash at the office if needed)",
      "Inform your provider of any medications, supplements, or medical conditions"],
     ["You may have swelling, tenderness, and bruising for up to 2 weeks post-treatment",
      "Do not massage treated areas unless instructed by your provider",
      "Avoid NSAIDs; Tylenol is OK",
      "Avoid strenuous exercise for 48 hours",
      "Avoid alcohol for 24 hours",
      "Avoid extreme heat (saunas, steam rooms, hot yoga) for 48 hours",
      "Results develop gradually over 4–12 weeks as collagen production is stimulated",
      "A series of treatments may be recommended for optimal results"]),
    ("Microneedling", None,
     ["Avoid retinoids (tretinoin, retinol) for 5–7 days before treatment",
      "Avoid blood thinners and supplements (aspirin, ibuprofen, fish oil, vitamin E) for 3 days prior, if medically safe to do so",
      "Avoid active skin infections, irritation, open wounds, sunburn, or severe breakouts in the treatment area — call us to reschedule",
      "Avoid sun exposure and tanning for at least 2 weeks before treatment",
      "Do not use exfoliating acids (AHA, BHA, glycolic) for 3 days prior",
      "Arrive with a clean face, free of makeup (we have makeup wipes & face wash at the office if needed)",
      "Stay well hydrated leading up to your appointment",
      "Inform your provider of any history of cold sores or keloid scarring"],
     ["Skin will appear red and feel similar to a mild sunburn for 24–72 hours; this is normal",
      "Change your pillowcase",
      "Do not wash your face or apply any products for at least 4–6 hours post-treatment (if you received microneedling with PRF or VAMP, please wait 12–24 hours before washing your face)",
      "You will be given a topical skin hydrator at your appointment to use for the first 24 hours — we do not recommend any other products during this time",
      "Avoid retinoids, exfoliating acids, and active skincare ingredients for 7 days until your skin is healed",
      "Avoid direct sun exposure and wear SPF 30 or higher daily (after 24 hours)",
      "Avoid strenuous exercise, sweating, and heat exposure for 24–48 hours",
      "You may experience some peeling on days 3–5; do NOT pick any flaking skin",
      "Results improve progressively — optimal results are typically seen after a series of 3 treatments spaced 4–6 weeks apart"]),
    ("PRF EZ Gel", None,
     ["Stay well hydrated and eat a balanced, nutrient-rich meal before your appointment — the quality of your PRF is directly influenced by the quality of your blood, so proper hydration and nutrition in the days leading up to your treatment will support optimal results",
      "Avoid alcohol for at least 24–48 hours before your appointment",
      "Avoid blood-thinning and anti-inflammatory medications (aspirin, ibuprofen, fish oil, vitamin E, ginkgo biloba) for 3 days prior, if medically safe to do so",
      "Arrive with a clean face, free of makeup (we have makeup wipes & face wash at the office if needed)",
      "Avoid scheduling within 2 weeks of a major event",
      "Inform your provider of any medications, supplements, or medical conditions"],
     ["Expect swelling, redness, and possible bruising for 3–5 days; this is normal and part of the healing process — please plan special events accordingly",
      "Avoid anti-inflammatory medications (NSAIDs, Advil, Aspirin), ice, and Arnica as these can suppress the regenerative process — Tylenol is OK",
      "Avoid touching, rubbing, or massaging the treated area for 24 hours",
      "Avoid strenuous exercise and excessive sweating for 48 hours",
      "Avoid alcohol for 24–48 hours",
      "Avoid extreme heat (saunas, steam rooms, hot yoga) for 48–72 hours",
      "No makeup in the treatment area for 24 hours",
      "Avoid laser treatments, chemical peels, or microneedling for 1 week",
      "Results develop gradually over 4–12 weeks as your body produces new collagen and elastin",
      "A series of 3 treatments spaced 4–6 weeks apart is usually recommended for optimal results"]),
    ("VI Chemical Peel", None,
     ["Avoid retinoids (tretinoin, retinol) for 5–7 days before your peel",
      "Avoid exfoliating acids (AHA, BHA, glycolic, salicylic) for 5–7 days prior",
      "Avoid waxing, threading, or laser treatments on the face for at least 2 weeks before your peel",
      "Avoid prolonged sun exposure and tanning for at least 2 weeks before treatment; arrive without a sunburn",
      "Discontinue use of any prescription topicals unless advised otherwise by your provider",
      "Arrive with a clean face, free of makeup (we have makeup wipes & face wash at the office if needed)",
      "Inform your provider of any history of cold sores; antiviral prophylaxis may be recommended",
      "Inform your provider of any current medications, especially Accutane (you must be off Accutane for at least 6 months before receiving a chemical peel)"],
     ["Leave the peel solution on for the time instructed by your provider; do not wash your face early",
      "Peeling typically begins on days 2–3 and can last through day 7; this is expected and normal",
      "Do not pick, pull, or peel flaking skin; allow it to shed naturally to avoid scarring or hyperpigmentation",
      "Use only the post-peel kit products provided; do not introduce any other skincare during the healing period",
      "Avoid direct sun exposure entirely during the peeling phase; wear SPF 30 or higher every day once healed",
      "Avoid strenuous exercise and sweating for the first 48 hours",
      "Avoid alcohol for 24–48 hours",
      "Avoid retinoids, exfoliating acids, and active skincare for at least 7–10 days post-peel",
      "Avoid laser treatments, microneedling, or waxing for 4 weeks",
      "Avoid swimming pools and hot tubs during the healing process",
      "Final results are visible once peeling is complete, typically within 7–10 days — skin will appear brighter, smoother, and more even in tone"]),
]

FAQ = [
    ("Neurotoxin", [
        ("How long will my results last?",
         "Tox results can vary from person to person, but on average you can expect your treatment to last 3–4 months, with results peaking around 6–8 weeks."),
        ("How quickly will I notice a difference?",
         "Neurotoxins take up to 14 days to fully settle, but you may begin to feel the effects in as little as 24 hours."),
        ("What if I need more units?",
         "Please schedule a follow-up appointment 2–3 weeks after your treatment so we can assess your movement and perform a dosage adjustment as needed."),
        ("How many units will I need?",
         "Everyone’s anatomy and aesthetic goals are different. A general guideline is around 20 units for each of the upper facial muscles (forehead, “eleven lines,” and crow’s feet)."),
    ]),
    ("Dermal Filler", [
        ("Am I going to swell or bruise?",
         "Dermal fillers are introduced into the body via a needle or cannula, and because of this mild trauma most people can expect bruising and swelling to some degree."),
        ("How long will I be swollen or bruised?",
         "The extent of your bruising and/or swelling is unique to you, but most people are able to resume regular daily activities after 24–48 hours. Arnica gel and Tylenol will be provided after your appointment, along with aftercare do’s and don’ts to ensure safe and healthy healing."),
        ("How long do dermal filler results last?",
         "Results are visible immediately and typically last 6–18 months, depending on the type of filler used, the area treated, and individual factors like metabolism and lifestyle."),
        ("How many syringes will I need?",
         "That depends entirely on your current anatomy and aesthetic goals. You and your provider will create a treatment plan together so we can help you achieve the look you’re going for."),
        ("Can I pay for a half syringe?",
         "We do not offer half syringes, but we will keep any leftover filler from your syringe for 2 weeks. After two weeks, you’ll come in for a follow-up and any remaining filler can be used at that visit."),
        ("What if I don’t like my results?",
         "The good news is that dermal fillers are long-lasting but temporary. You can wait for your body to naturally metabolize the filler, or you can come in to have it dissolved with a special filler-dissolving agent."),
    ]),
    ("Microneedling", [
        ("Does microneedling hurt?",
         "Most clients are surprised by how comfortable it is. We apply a strong medical-grade numbing cream before your session, so you’ll typically feel light pressure and vibration rather than pain. Most patients report little to no pain during the procedure."),
        ("How many sessions will I need?",
         "We typically recommend a series of three treatments spaced 4–6 weeks apart. After this series is completed, you can maintain your results with a treatment every 3–4 months."),
        ("What does microneedling do?",
         "Microneedling creates channels in the skin using sterile needles. These channels allow skincare products to penetrate more deeply and signal the body to produce more collagen — a foundational building block of the skin that creates tighter, firmer, more supple skin."),
        ("When will I see results?",
         "You’ll often notice a healthy glow and smoother texture within a few days. Because microneedling works by stimulating your own collagen, the most meaningful improvements in tone, firmness, and scars appear over 4–6 weeks and continue to build with each session."),
        ("What is a good candidate for microneedling?",
         "Microneedling works for all skin types and tones. It should be avoided by people who are pregnant or breastfeeding, and those with active acne in the treatment area."),
    ]),
    ("Chemical Peels", [
        ("What is a chemical peel?",
         "A chemical peel consists of skin-friendly chemicals that are expertly applied to your skin, chemically exfoliating the outer layer to reveal fresher, healthier skin beneath."),
        ("What are chemical peels good for?",
         "Chemical peels can treat a wide variety of skin conditions, including fine lines and wrinkles, post-inflammatory hyperpigmentation (PIH), acne scarring, uneven skin tone, and dullness. Talk to your provider about your aesthetic goals."),
        ("Do chemical peels hurt?",
         "Not at all. Chemical peels are a completely painless procedure."),
        ("What is the downtime like?",
         "After your chemical peel, you will typically begin to peel around day 3 and be finished by day 7. The severity of peeling depends on the prior condition of your skin and whether you regularly use retinoids or active skincare ingredients."),
    ]),
    ("IV Hydration", [
        ("What are IVs for?",
         "An IV can be great for replenishing and rebalancing electrolytes, helping soothe migraines, easing body aches, relieving nausea, boosting immunity before travel, and cutting colds short!"),
        ("How long does a session take?",
         "Most IV drips take between 30 and 40 minutes, depending on the blend selected. You can relax comfortably during your session in our IV lounge, making it an easy addition to your self-care routine."),
        ("What can IV hydration help with?",
         "IV hydration can support a wide range of goals and concerns, including fatigue and low energy, dehydration, immune support, hangover recovery, brain fog, athletic recovery, skin health and glow, jet lag, and general wellness maintenance."),
        ("Are there any contraindications?",
         "Certain medical conditions such as kidney disease, heart failure, or fluid-sensitive conditions may make IV hydration inappropriate. This is why we complete a thorough health history review before every session. If you have questions about whether it’s right for you, feel free to reach out before booking."),
        ("Who is a good candidate for IV hydration?",
         "IV hydration is a great option for busy professionals, athletes, frequent travelers, those feeling run down or under the weather, or anyone looking to optimize their overall wellness. A brief health intake is completed prior to your first session to confirm it’s appropriate for you."),
    ]),
    ("PRF EZ Gel", [
        ("What is PRF EZ Gel?",
         "PRF EZ Gel is an advanced, all-natural filler alternative made entirely from your own blood. We draw a small amount of blood, process it to concentrate the platelet-rich fibrin, and then heat it to create a gel-like consistency that can be injected to restore volume, stimulate collagen, and rejuvenate the skin from the inside out."),
        ("How is PRF EZ Gel different from PRP or traditional fillers?",
         "Unlike PRP (platelet-rich plasma), PRF contains more white blood cells and fibrin, which allows for a slower release of growth factors and longer-lasting results. Unlike traditional dermal fillers, PRF EZ Gel is 100% autologous — from your own body with no synthetic ingredients — and actively improves skin quality, texture, and tone over time."),
        ("What areas can be treated with PRF EZ Gel?",
         "PRF EZ Gel is commonly used to address volume loss in the under eyes, cheeks, temples, jawline, and smile lines. It is also an excellent option for skin laxity and overall facial rejuvenation."),
        ("What can I expect after my PRF EZ Gel treatment?",
         "Swelling, redness, and bruising in the treated areas is normal and typically resolves within a few days to a week. Because PRF EZ Gel is derived from your own blood, the risk of allergic reaction or rejection is extremely low. Final results are typically visible around 4–6 weeks post-treatment as collagen remodeling continues."),
        ("How many sessions will I need, and how long do results last?",
         "You may see improvement after a single session, though a series of 3 treatments spaced 4–6 weeks apart is often recommended for optimal and longer-lasting results. Effects can last 6–12 months or longer, depending on your skin health, age, and lifestyle."),
    ]),
    ("Radiesse", [
        ("What is Radiesse?",
         "Radiesse is an FDA-approved biostimulatory filler made of calcium hydroxylapatite (CaHA) microspheres. It provides immediate volume while stimulating your body’s own collagen production for longer-lasting results."),
        ("What can Radiesse treat?",
         "Common treatment areas include the cheeks, jawline, nasolabial folds, marionette lines, and hands."),
        ("How is Radiesse different from hyaluronic acid fillers?",
         "Radiesse is a biostimulator, meaning it actively triggers new collagen and elastin production in addition to adding volume. Unlike HA fillers, it is not reversible with hyaluronidase."),
        ("How long do results last?",
         "Most patients enjoy results for 12–18 months or longer. Because Radiesse stimulates collagen, results can continue to improve over time and may last even longer with maintenance sessions."),
        ("When will I see results?",
         "Most patients begin to notice improvements within a few weeks, with optimal results visible around 3–6 months after treatment as collagen builds."),
        ("Is there any downtime?",
         "Little to none. You may experience mild swelling, redness, or bruising for a few days. We recommend avoiding strenuous exercise, alcohol, and excessive heat for 24–48 hours."),
        ("Who is a good candidate for Radiesse?",
         "Most healthy adults looking to restore volume, improve skin laxity, or address moderate to severe wrinkles are great candidates. It is not recommended for patients who are pregnant, breastfeeding, or have active skin infections at the treatment site."),
        ("Can Radiesse be combined with other treatments?",
         "Absolutely. Radiesse pairs well with neurotoxin, other dermal fillers, PRF EZ Gel, and skin-rejuvenating treatments. Your provider will create a personalized plan during your consultation."),
        ("Is Radiesse safe?",
         "Yes. Radiesse has been FDA approved since 2006 and has a strong safety record. All treatments at Nōvuu Medspa are performed by Jess, a board-certified nurse practitioner with advanced aesthetic training."),
    ]),
]


# ---- page furniture --------------------------------------------------------
def draw_bg(canvas, doc):
    canvas.saveState()
    # slim top accent band
    canvas.setFillColor(GREEN)
    canvas.rect(0, PAGE_H - 0.28 * inch, PAGE_W, 0.28 * inch, fill=1, stroke=0)
    # footer
    canvas.setFont("Jost", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(PAGE_W / 2, 0.5 * inch,
                             "Nōvuu Medspa   ·   novuumedspa.com")
    canvas.drawRightString(PAGE_W - MX, 0.5 * inch, str(canvas.getPageNumber()))
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(OUT, pagesize=letter,
                          leftMargin=MX, rightMargin=MX,
                          topMargin=MT, bottomMargin=MB,
                          title="Nōvuu Medspa — Pre & Post Care Instructions",
                          author="Nōvuu Medspa")
    frame = Frame(MX, MB, PAGE_W - 2 * MX, PAGE_H - MT - MB, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=draw_bg)])

    S = []
    # masthead
    S.append(Paragraph("PRE &amp; POST CARE", eyebrow))
    S.append(Paragraph("NŌVUU MEDSPA", title))
    S.append(Paragraph("Pre &amp; Post Care Instructions", subtitle))
    S.append(Spacer(1, 6))
    S.append(HRFlowable(width="38%", thickness=0.8, color=SAGE, spaceBefore=2,
                        spaceAfter=12, hAlign="CENTER", lineCap="round"))

    for name, sub, pre, post in CARE:
        heading = esc(name) if not sub else \
            f"{esc(name)} <font size=12 color='{MUTED}'>({esc(sub)})</font>"
        # keep the service heading, rule, subhead and first bullet together
        S.append(KeepTogether([
            Paragraph(heading, service),
            HRFlowable(width="100%", thickness=0.6, color=SAGE,
                       spaceBefore=1, spaceAfter=5, lineCap="round"),
            Paragraph("PRE-TREATMENT", colhead),
            bul(pre[0]),
        ]))
        for b in pre[1:]:
            S.append(bul(b))
        S.append(Paragraph("POST-TREATMENT", colhead))
        for b in post:
            S.append(bul(b))
        S.append(Spacer(1, 10))

    # FAQ
    S.append(PageBreak())
    S.append(Paragraph("FREQUENTLY ASKED QUESTIONS", eyebrow))
    S.append(Paragraph("Questions, Answered", sectionhead))
    S.append(HRFlowable(width="38%", thickness=0.8, color=SAGE, spaceBefore=2,
                        spaceAfter=12, hAlign="CENTER", lineCap="round"))
    for topic, qas in FAQ:
        head = [Paragraph(esc(topic), faq_topic),
                HRFlowable(width="100%", thickness=0.6, color=SAGE,
                           spaceBefore=1, spaceAfter=4, lineCap="round"),
                Paragraph(esc(qas[0][0]), faq_q),
                Paragraph(esc(qas[0][1]), faq_a)]
        S.append(KeepTogether(head))
        for q, a in qas[1:]:
            S.append(KeepTogether([Paragraph(esc(q), faq_q),
                                   Paragraph(esc(a), faq_a)]))
        S.append(Spacer(1, 8))

    S.append(Spacer(1, 6))
    S.append(Paragraph("Questions? Visit us at novuumedspa.com",
                       ParagraphStyle("close", parent=faq_a, alignment=TA_CENTER,
                                      textColor=MUTED, fontSize=9.5)))

    doc.build(S)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
