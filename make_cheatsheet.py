#!/usr/bin/env python3
"""Generate a beginner's D&D 5E cheat sheet PDF tailored to the TWSC party."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, FrameBreak, NextPageTemplate, KeepInFrame
)
from reportlab.lib.enums import TA_LEFT

# ── Palette (matches the site's dark-fantasy gold theme, print-friendly) ──
GOLD = colors.HexColor("#9c6f1a")
GOLD_LIGHT = colors.HexColor("#c8973a")
INK = colors.HexColor("#2b2620")
RED = colors.HexColor("#8a2a14")
BG_BOX = colors.HexColor("#f6efe0")
BORDER = colors.HexColor("#d8c79c")

styles = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold",
                    fontSize=20, textColor=GOLD, spaceAfter=2, alignment=TA_LEFT)
SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontName="Helvetica-Oblique",
                     fontSize=9.5, textColor=INK, spaceAfter=8)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=11.5, textColor=RED, spaceBefore=4, spaceAfter=3,
                    leading=13)
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=8.6, textColor=INK, leading=11, spaceAfter=3)
BULLET = ParagraphStyle("BULLET", parent=BODY, leftIndent=10, bulletIndent=1,
                        spaceAfter=1.5)
SMALL = ParagraphStyle("SMALL", parent=BODY, fontSize=7.8, leading=9.5)
TAGLABEL = ParagraphStyle("TAGLABEL", parent=BODY, fontName="Helvetica-Bold",
                          fontSize=8.6, textColor=GOLD)


def b(text):
    return Paragraph("• " + text, BULLET)


def box(title, flowables, width):
    """A bordered, shaded callout box with a title bar."""
    inner = [Paragraph(title, ParagraphStyle(
        "boxtitle", fontName="Helvetica-Bold", fontSize=10,
        textColor=colors.white, leading=12))]
    title_tbl = Table([[inner[0]]], colWidths=[width])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    body_tbl = Table([[flowables]], colWidths=[width])
    body_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_BOX),
        ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [title_tbl, body_tbl, Spacer(1, 7)]


# ── Document with a two-column layout ──
PAGE_W, PAGE_H = letter
MARGIN = 0.5 * inch
GUTTER = 0.28 * inch
COL_W = (PAGE_W - 2 * MARGIN - GUTTER) / 2
COL_H = PAGE_H - 2 * MARGIN - 0.55 * inch  # leave room for header band


def header_footer(canvas, doc):
    canvas.saveState()
    # top rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(2)
    y = PAGE_H - MARGIN - 0.42 * inch
    canvas.line(MARGIN, y, PAGE_W - MARGIN, y)
    # footer
    canvas.setFont("Helvetica-Oblique", 7)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(PAGE_W / 2, MARGIN - 6,
                             "A Wild Sheep Chase — Player Cheat Sheet  ·  "
                             "page %d" % doc.page)
    canvas.restoreState()


def build_columns(y_top):
    left = Frame(MARGIN, MARGIN, COL_W, COL_H, id="L",
                 leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    right = Frame(MARGIN + COL_W + GUTTER, MARGIN, COL_W, COL_H, id="R",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    return [left, right]


doc = BaseDocTemplate(
    "/home/user/TWSC/player_cheat_sheet.pdf", pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
    title="A Wild Sheep Chase — Player Cheat Sheet", author="DM Reference")

frames = build_columns(COL_H)
doc.addPageTemplates([
    PageTemplate(id="twocol", frames=frames, onPage=header_footer),
])

story = []
W = COL_W

# ════════ TITLE (spans first column top) ════════
story.append(Paragraph("D&amp;D 5E — Beginner Cheat Sheet", H1))
story.append(Paragraph("Everything you need for your first few sessions. "
                       "When in doubt, just describe what you want to do — "
                       "the DM will help with the dice.", SUB))

# ════════ THE CORE LOOP ════════
core = [
    Paragraph("Almost everything uses one idea:", BODY),
    Paragraph("<b>d20 + your modifier + proficiency (if trained) "
              "vs. a target number.</b>", BODY),
    b("Roll the 20-sided die (d20)."),
    b("Add the relevant <b>ability modifier</b> (e.g. +3)."),
    b("Add your <b>proficiency bonus</b> (+2 for you) <i>if</i> you're "
      "trained in that skill/weapon/save."),
    b("Meet or beat the target (DC or enemy AC) = success."),
    Paragraph("<b>Advantage:</b> roll 2d20, take the higher. "
              "<b>Disadvantage:</b> roll 2d20, take the lower. "
              "They cancel out.", SMALL),
    Paragraph("<b>Natural 20</b> on an attack = critical hit (roll your "
              "damage dice twice). <b>Natural 1</b> on an attack = automatic "
              "miss.", SMALL),
]
story += box("THE ONE RULE THAT RUNS EVERYTHING", core, W)

# ════════ THE SIX ABILITIES ════════
ab = [
    Paragraph("<b>STR</b> — lifting, melee muscle, breaking things", SMALL),
    Paragraph("<b>DEX</b> — aim, stealth, reflexes, finesse weapons, AC", SMALL),
    Paragraph("<b>CON</b> — health, endurance, concentration saves", SMALL),
    Paragraph("<b>INT</b> — knowledge, investigation, wizardry", SMALL),
    Paragraph("<b>WIS</b> — perception, insight, druid/ranger magic", SMALL),
    Paragraph("<b>CHA</b> — persuasion, deception, presence", SMALL),
]
story += box("THE SIX ABILITIES", ab, W)

# ════════ YOUR TURN IN COMBAT ════════
turn = [
    Paragraph("On your turn you get <b>all three</b> of these, in any order:",
              BODY),
    Paragraph("<b>1. Move</b> up to your speed (split it however you like).",
              BULLET),
    Paragraph("<b>2. One Action</b> — the big thing you do (see list).",
              BULLET),
    Paragraph("<b>3. One Bonus Action</b> — only if a feature gives you one "
              "(e.g. off-hand attack, Cunning Action, Shillelagh).", BULLET),
    Paragraph("You also get <b>one Reaction</b> per round (e.g. an "
              "opportunity attack) — usable even on others' turns.", SMALL),
    Paragraph("<b>Common Actions:</b>", TAGLABEL),
    b("<b>Attack</b> — make a weapon or unarmed attack."),
    b("<b>Cast a Spell</b> — most take an action."),
    b("<b>Dash</b> — double your movement this turn."),
    b("<b>Disengage</b> — move away without provoking attacks."),
    b("<b>Dodge</b> — attackers have disadvantage on you."),
    b("<b>Hide</b> — Stealth check to become unseen."),
    b("<b>Help</b> — give an ally advantage on their next roll."),
]
story += box("YOUR TURN IN A FIGHT (Move · Action · Bonus Action)", turn, W)

# Move to right column
story.append(FrameBreak())

# ════════ HOW TO ATTACK ════════
atk = [
    Paragraph("<b>1. To-hit:</b> roll d20 + attack bonus vs. the target's "
              "<b>AC</b> (Armor Class).", BODY),
    Paragraph("<b>2. Damage:</b> if you hit, roll the weapon's damage dice "
              "+ your modifier (already printed on your sheet).", BODY),
    Paragraph("<b>Opportunity attack:</b> if you walk out of an enemy's reach, "
              "they get a free swing. Use <i>Disengage</i> or stay put to avoid "
              "it.", SMALL),
    Paragraph("<b>Cover &amp; positioning matter</b> — ask the DM. Attacking "
              "from hiding or with an ally flanking often gives advantage or "
              "Sneak Attack.", SMALL),
]
story += box("MAKING AN ATTACK", atk, W)

# ════════ SPELLCASTING BASICS ════════
spell = [
    Paragraph("<b>Cantrips</b> are free to cast, as often as you like.", BODY),
    Paragraph("<b>Leveled spells</b> use a <b>spell slot</b>. You have a "
              "limited number — once spent, they refresh after a rest.", BODY),
    Paragraph("<b>Spell save:</b> when your spell forces a save, the enemy "
              "rolls d20 + their modifier vs. <b>your Spell Save DC</b> "
              "(on your sheet). They fail = full effect.", SMALL),
    Paragraph("<b>Spell attack:</b> some spells make an attack roll instead — "
              "d20 + your spell attack bonus vs. their AC.", SMALL),
    Paragraph("<b>Concentration:</b> some spells say 'Concentration.' You can "
              "only hold <b>one</b> at a time. If you take damage, roll a CON "
              "save (DC 10 or half the damage, whichever is higher) or it "
              "drops.", SMALL),
    Paragraph("<b>Components:</b> most spells need you to speak (V) and gesture "
              "(S), so being gagged or bound can stop them.", SMALL),
]
story += box("SPELLCASTING BASICS", spell, W)

# ════════ STAYING ALIVE ════════
alive = [
    Paragraph("<b>Hit Points (HP):</b> your buffer. At 0 HP you fall "
              "unconscious.", SMALL),
    Paragraph("<b>Death saves:</b> while dying, on your turn roll a d20. "
              "10+ = success, under 10 = failure. <b>Three successes</b> = "
              "stable; <b>three failures</b> = dead. A nat 20 = pop back up "
              "with 1 HP.", SMALL),
    Paragraph("<b>Healing</b> any amount above 0 wakes you instantly. A "
              "<b>Short Rest</b> (~1 hr) lets you spend Hit Dice to heal; a "
              "<b>Long Rest</b> (~8 hr) restores all HP and slots.", SMALL),
]
story += box("STAYING ALIVE (HP &amp; Dying)", alive, W)

# ════════ WHEN YOU'RE STUCK ════════
stuck = [
    b("<b>Describe the goal</b>, not the rule: 'I want to vault the bar and "
      "tackle him.' The DM tells you what to roll."),
    b("Not sure if you can do something? Just ask the DM."),
    b("Use your features! Check your sheet's 'Turn Plan' box for your "
      "go-to move."),
    b("Teamwork beats heroics — <i>Help</i>, heal, and set each other up."),
]
story += box("WHEN IN DOUBT", stuck, W)

# ════════ PAGE 2: PARTY QUICK MOVES ════════
story.append(NextPageTemplate("twocol"))
story.append(FrameBreak())  # ensure page 2 starts cleanly via new page
# Force a new page by breaking out of both frames
story.append(Paragraph("Your Party — Go-To Moves", H1))
story.append(Paragraph("A reminder of the one or two things each of you does "
                       "best. Lean on these when it's your turn.", SUB))

bram = [
    Paragraph("<b>Half-Orc Ranger (Fey Wanderer) · Level 3 · AC 15 · HP 28</b>",
              TAGLABEL),
    b("<b>Main turn:</b> Attack with a sai (+5, 1d6+3), then <b>Bonus "
      "Action</b> attack with the off-hand sai (+5, 1d6+3)."),
    b("Once per turn add <b>Dreadful Strikes</b> (+1d4 psychic) on a hit."),
    b("Vs. a tough enemy: use <b>Favored Foe</b> for +1d4 (2/long rest)."),
    b("You can heal in a pinch: <b>Cure Wounds</b> (1d8+2, touch)."),
    b("Saved by <b>Relentless Endurance</b>: drop to 1 HP instead of 0 "
      "once per long rest."),
]
story += box("BRAM (Chris)", bram, W)

dusty = [
    Paragraph("<b>Hill Dwarf Druid (Coastal) · Level 5 · AC 14 · HP 48</b>",
              TAGLABEL),
    b("<b>Melee:</b> Shillelagh club (+7, 1d8+4) — your reliable swing."),
    b("<b>Open with a spell:</b> Call Lightning, Cure Wounds, Barkskin, "
      "or Mirror Image."),
    b("<b>Wild Shape → Giant Crab</b> (2/rest) to grapple and tank, "
      "protecting Bram &amp; Medrick."),
    b("Cast <b>Guidance</b> (+1d4) on allies before skill checks out of "
      "combat — constantly."),
    b("You're the healer/anchor: keep the squishier two standing."),
]
story += box("DUSTY (Emily)", dusty, W)

story.append(FrameBreak())

medrick = [
    Paragraph("<b>Lightfoot Halfling Rogue (Arcane Trickster) · Level 3 · "
              "AC 15 · HP 24</b>", TAGLABEL),
    b("<b>Main turn:</b> Shortbow or Rapier (+5). Add <b>Sneak Attack "
      "+2d6</b> once per turn when you have advantage <i>or</i> an ally is "
      "next to your target."),
    b("<b>Bonus Action (Cunning Action):</b> Hide, Dash, or Disengage — "
      "every turn."),
    b("With the <b>Cloak of Elvenkind</b>, Hide for advantage = easy "
      "Sneak Attack."),
    b("Tricks: Mage Hand (invisible), Minor Illusion, Disguise Self, "
      "and your scouting owl familiar."),
    b("<b>Lucky:</b> reroll natural 1s on d20s."),
]
story += box("MEDRICK (Dan)", medrick, W)

cheat = [
    Paragraph("<b>Quick reference for the table</b>", TAGLABEL),
    Paragraph("<b>AC</b> = how hard you are to hit. "
              "<b>DC</b> = difficulty of a task.", SMALL),
    Paragraph("Typical DCs: <b>10</b> easy · <b>15</b> medium · "
              "<b>20</b> hard.", SMALL),
    Paragraph("<b>Prone:</b> melee attacks vs. you have advantage; you have "
              "disadvantage to attack. Stand up = half your move.", SMALL),
    Paragraph("<b>Grappled / Restrained:</b> speed 0 (restrained also gives "
              "attackers advantage).", SMALL),
    Paragraph("<b>1 square = 5 ft.</b> Most melee reach is 5 ft.", SMALL),
    Paragraph("Round = 6 seconds. Everyone acts once per round in initiative "
              "order (d20 + DEX).", SMALL),
]
story += box("MINI GLOSSARY", cheat, W)

doc.build(story)
print("Wrote player_cheat_sheet.pdf")
