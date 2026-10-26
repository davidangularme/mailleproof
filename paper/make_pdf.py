"""Document Zenodo : a(16) = 113 pour OEIS A389241 (généré à partir de mailleproof/phase3/lots.json)."""
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

HERE = Path(__file__).resolve().parent
F = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Arial", F + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", F + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", F + "Arial Italic.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")

ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["Normal"], fontName="Arial", fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
small = ParagraphStyle("s", parent=body, fontSize=8.5, leading=11)
h1 = ParagraphStyle("h1", parent=body, fontName="Arial-Bold", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=5,
                    alignment=0)
title = ParagraphStyle("t", parent=body, fontName="Arial-Bold", fontSize=17, leading=22, alignment=TA_CENTER, spaceAfter=8)
center = ParagraphStyle("c", parent=body, alignment=TA_CENTER, spaceAfter=2)
code = ParagraphStyle("code", fontName="Courier", fontSize=8.5, leading=10.5, leftIndent=12, spaceAfter=6)

data = json.loads((HERE.parent / "phase3/lots.json").read_text())
lots = data["lots"]
orig_h = sum(l["original"]["duration_s"] or 0 for l in lots) / 3600
rep_h = sum(l["reproduction"]["duration_s"] or 0 for l in lots) / 3600
host2 = sum(1 for l in lots if l["reproduction"]["host"] == "host-2")

W = [1, 2, 6, 11, 13, 4, 14, 9, 12, 8, 15, 16, 10, 5, 7, 3]
sums = {sum(W[i:j]) for i in range(16) for j in range(i + 1, 17)}
assert len(sums) == 113

P = lambda t, s=body: Paragraph(t, s)  # noqa: E731
story = [
    P("a(16) = 113 for OEIS A389241: a witness and an exhaustive search re-executed independently", title),
    P("<b>Frédéric David Blum</b>", center),
    P("Catalyst AI Research, Haifa, Israel", center),
    P("ORCID 0009-0009-2487-2974 · freddavidblum@catalystais.com", center),
    P("26 October 2026 · version 1", center),
    Spacer(1, 10),
    P("<b>Abstract.</b> Sequence A389241 of the OEIS gives, for each n, the maximum number of distinct sums of "
      "consecutive terms of a permutation of 1..n; it was known up to a(15) = 100. We show a(16) = 113. A permutation "
      "of 1..16 with 113 distinct consecutive sums gives the lower bound. An exhaustive branch-and-bound search over all "
      "permutations of 1..16, split into 60 runs that together cover the 240 possible ordered first pairs, finds none "
      "with 114 or more. Each run first recovers the known values a(3)..a(9) and checks the branch-and-bound against "
      "brute force; each run was re-executed by a different AI agent with a byte-identical output. The exact programs, "
      "their outputs, SHA-256 fingerprints and a checker that verifies all records in seconds are published with this "
      "record, and any run can be re-executed."),
    P("1. The sequence", h1),
    P("For a permutation p = (p<sub>1</sub>, ..., p<sub>n</sub>) of 1..n, consider the n(n+1)/2 sums of consecutive "
      "terms p<sub>i</sub> + ... + p<sub>j</sub>, 1 ≤ i ≤ j ≤ n, and let s(p) be the number of distinct values among "
      "them. A389241(n) is the maximum of s(p) over all permutations of 1..n. The known terms end with a(15) = 100 "
      "[1]. For n = 16 there are 136 consecutive sums, so a(16) ≤ 136; this note shows a(16) = 113."),
    P("2. Lower bound: a(16) ≥ 113", h1),
    P("The permutation"),
    Preformatted("[" + ", ".join(map(str, W)) + "]", code),
    P("has exactly 113 distinct consecutive sums. This takes a few lines to check (<font face='Courier'>verify.py</font> "
      "in [2]); a second program written independently (<font face='Courier'>recount.py</font>) gives the same count. "
      "The permutation was found on 20 October 2026 by the branch-and-bound program of Section 3, run on the prefix [1, 2]."),
    P("3. Upper bound: no permutation of 1..16 reaches 114", h1),
    P("<b>Algorithm.</b> The search is a depth-first branch-and-bound written in C (compiled with "
      "<font face='Courier'>gcc -O2</font>) and embedded in a short Python driver. A permutation is built from left to "
      "right. When a value x is appended, the new consecutive sums are the sums ending at x; the program counts how many "
      "of them repeat a value already present. Appending terms never removes a sum, so a repetition, once it occurs, "
      "persists in every completion of the prefix. If D repetitions have occurred, every completion has at most "
      "136 − D distinct sums; the branch is abandoned as soon as 136 − D ≤ 113. A branch therefore survives only if it "
      "could still exceed 113, and a completed permutation is reported only if it has at least 114 distinct sums. The "
      "bound is exact bookkeeping, not a heuristic: no permutation reaching 114 can be pruned."),
    P("<b>Partition of the search.</b> Every permutation of 1..16 starts with one of the 240 ordered pairs (a, b), "
      "a ≠ b. The program takes a list of prefixes (its only variable line, <font face='Courier'>PREFIXES</font>) and "
      "explores all permutations starting with each of them. The search was split into runs of four pairs each. "
      f"The {len(lots)} runs published here cover all 240 pairs (some pairs are covered by more than one run); "
      "the checker reads the covered prefixes from the programs themselves, not from metadata."),
    P("<b>Positive control.</b> Before the search, every run computes a(3)..a(9) by brute force over all permutations, "
      "prints them (6, 9, 13, 19, 25, 32, 39, the known values) and checks that the branch-and-bound returns the same "
      "maxima as brute force for n = 3..9, for every first element and for every first pair. A run whose control "
      "fails does not count. This guards against a program that reports nothing because it searches nothing."),
    P("<b>Result.</b> For each of the 240 pairs, the output reports <font face='Courier'>trouve_geq114 False</font>: "
      "no permutation of 1..16 with that prefix has 114 or more distinct consecutive sums. With Section 2, "
      "<b>a(16) = 113</b>."),
    P("4. Records, independent re-execution and checking", h1),
    P("Every run was executed on a dedicated compute host without network access that records the SHA-256 of the exact "
      "program and of its standard output. Every run was then re-executed, from the same program, by a different AI "
      "agent, and the two outputs have the same SHA-256 (byte-identical). The output contains no timing or random "
      f"value, so identity is expected from a correct run. The {len(lots)} runs took about {orig_h:.0f} CPU hours and the "
      f"re-executions about {rep_h:.0f} more."),
    P(f"<b>Hosts.</b> Until 26 October 2026 the re-executions ran on the same compute host as the original runs "
      f"(<i>host-1</i>); from that date they run on a second, independent host (<i>host-2</i>). In this record "
      f"{host2} of the {len(lots)} re-executions ran on host-2. An earlier version of the repository described the "
      "first phase-3 re-execution as made \"on a different server\": it was submitted by a different agent but ran on "
      "the same host; the repository carries a dated correction."),
    P("<b>Checking.</b> <font face='Courier'>phase3/verify_phase3.py</font> [2] checks, for each run: the SHA-256 of "
      "the published program; that the program is the reference search up to its PREFIXES line, comments and blank "
      "lines; the SHA-256 of the output and its equality with the re-execution; the positive control; and, for each "
      "prefix, that the best score is at most 113 and that no permutation reaches 114. It then checks that the prefixes "
      "cover all 240 pairs. Any run can be re-executed with <font face='Courier'>python3 phase3/codes/lotNN.py</font> "
      "(1 to 6 CPU hours each; gcc required)."),
    P("5. How the computation was organised", h1),
    P("The work was organised and carried out by three AI agents (Claude Haiku, Anthropic), each on its own server, "
      "which split the search, launched the runs and checked each other's results. The organising principle is that no "
      "agent can make a result count by stating it: the computations are executed and recorded by the compute host, "
      "a result is accepted only after re-execution by another agent with an identical output, and every program must "
      "first recover known values. The model cost of the agents for the exhaustive search was about 14 US dollars. The "
      "method by which the agents coordinate is the subject of patent applications and is not described here; the "
      "mathematical result does not depend on it, since every computation is published and can be re-run."),
    P("6. Limitations", h1),
    P("The upper bound rests on one program (one algorithm, one implementation). Re-executions check that the runs "
      "were performed and reported faithfully, not that the program is correct; that rests on the simplicity of the "
      "bound (Section 3), on the positive controls, and on anyone's ability to read and re-run the code. A second, "
      "independent implementation, or a formal proof of the pruning rule, would strengthen the result further. Most "
      "re-executions ran on the same host as the originals (Section 4)."),
    P("Data availability", h1),
    P("The witness, the 60 exact programs, their outputs and fingerprints, the reference program and the checkers are "
      "in the repository [2] and archived with this record."),
    P("References", h1),
    P("[1] OEIS Foundation Inc., The On-Line Encyclopedia of Integer Sequences, A389241, https://oeis.org/A389241.", small),
    P("[2] F. D. Blum, mailleproof: witness and exhaustive-search certificate for A389241(16), "
      "https://github.com/davidangularme/mailleproof (2026).", small),
    PageBreak(),
    P("Appendix: the 60 runs", h1),
    P("Prefixes searched by each run (read from its program), duration of the original run and of its independent "
      "re-execution, and the host of the re-execution. Durations in hours.", small),
]
rows = [["Run", "Prefixes (first two elements)", "Original", "Re-exec.", "Host"]]
for l in lots:
    rows.append([str(l["lot"]), ", ".join(l["prefixes"]),
                 f"{(l['original']['duration_s'] or 0) / 3600:.1f}", f"{(l['reproduction']['duration_s'] or 0) / 3600:.1f}",
                 l["reproduction"]["host"]])
t = Table(rows, colWidths=[1.2 * cm, 9.3 * cm, 1.8 * cm, 1.8 * cm, 1.6 * cm], repeatRows=1)
t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Arial", 8), ("FONT", (0, 0), (-1, 0), "Arial-Bold", 8),
                       ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("ALIGN", (2, 0), (3, -1), "RIGHT"),
                       ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
                       ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
story.append(t)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"F. D. Blum — a(16) = 113 for OEIS A389241 — {doc.page}")
    canvas.restoreState()


out = HERE / "a16_113_A389241_Blum_2026.pdf"
doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm,
                        bottomMargin=2 * cm, title="a(16) = 113 for OEIS A389241", author="Frédéric David Blum",
                        subject="OEIS A389241, a(16) = 113: witness and exhaustive-search certificate",
                        keywords="OEIS, A389241, integer sequences, exhaustive search, branch and bound")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(out)
