# -*- coding: utf-8 -*-
import json, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from snippets import CODE
from exam_content import MCQ, SA
OUT = json.load(open(os.path.join(os.path.dirname(__file__), 'outputs.json')))
for k, v in OUT.items():
    assert not v.startswith('ERROR'), k
esc = html.escape
L = 'ABCDE'

CSS = """
@page { size: A4; margin: 13mm 14mm 14mm 14mm; @bottom-center { content: counter(page) " / " counter(pages); font: 8pt Helvetica, Arial; color:#666; } }
* { box-sizing: border-box; }
body { font: 9.6pt/1.38 "Helvetica Neue", Helvetica, Arial, sans-serif; color:#111; margin:0; }
h1 { font-size: 19pt; margin: 0 0 2mm; } h2 { font-size: 13pt; margin: 6mm 0 2mm; padding-bottom: 1mm; border-bottom: 1.5px solid #222; }
.meta { color:#444; font-size: 9pt; }
.box { border:1px solid #999; border-radius: 3px; padding: 2.5mm 3.5mm; margin: 2.5mm 0; background:#fafafa; }
.q { break-inside: avoid; margin: 0 0 5mm; }
.q.long { break-inside: auto; }
.qh { font-weight: 700; margin-bottom: 1mm; } .qh .wk { font-weight: 400; color:#555; font-size: 8.4pt; }
.marks { float:right; font-weight:600; }
pre { background:#f3f4f6; border:1px solid #d6d9de; border-radius:3px; padding: 2mm 2.6mm; margin: 1.5mm 0; font: 8.1pt/1.32 Menlo, Consolas, monospace; white-space: pre-wrap; word-break: break-word; break-inside: avoid; }
pre.out { background:#eef6ee; border-color:#bcd7bc; }
code { font: 8.6pt Menlo, Consolas, monospace; background:#f0f0f0; padding: 0 1px; border-radius:2px; }
.opt { margin: 0.6mm 0 0.6mm 3mm; } .opt b.l { display:inline-block; width: 5mm; }
.ans { margin-top: 1.5mm; font-size: 8.8pt; color:#444; }
.v { margin: 1mm 0 1mm 0; padding-left: 2mm; } .ok { border-left: 3px solid #2e8b57; } .no { border-left: 3px solid #c0392b; }
.tag { font-weight: 700; } .ok .tag { color:#2e8b57; } .no .tag { color:#c0392b; }
.key { margin-top: 1.5mm; font-weight: 700; background:#fff6d6; border:1px solid #e6cf7a; display:inline-block; padding: 0.4mm 2mm; border-radius: 3px; }
table { border-collapse: collapse; margin: 1.5mm 0; font-size: 9pt; } th, td { border:1px solid #bbb; padding: 0.7mm 2.4mm; text-align:left; } th { background:#eee; }
.parts { margin: 1mm 0 0 3mm; } .parts div { margin: 0.6mm 0; }
.line { border-bottom: 1px dotted #666; display:inline-block; width: 40mm; height: 4mm; vertical-align: bottom; }
.small { font-size: 8.6pt; color:#555; } .sol p { margin: 1.4mm 0; } .sol ul { margin: 1mm 0 1mm 5mm; padding:0; }
.cover { break-after: page; }
"""

def pre(code, cls=''):
    return f'<pre class="{cls}">{esc(code)}</pre>'

def head(title, sub):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(title)}</title><style>{CSS}</style></head><body>'

def cover(answers):
    t = 'FIT5149 · Code-Reading Mock Exam' + (' · ANSWER KEY' if answers else '')
    rows = ''
    wk = {}
    for q in MCQ: wk.setdefault(q['week'].split(' · ')[0], []).append(q['id'])
    for q in SA: wk.setdefault(q['week'].split(' · ')[0], []).append(q['id'])
    order = sorted(wk, key=lambda w: int(w.replace('Week','').split('–')[0]))
    for w in order:
        rows += f'<tr><td>{w}</td><td>{", ".join(wk[w])}</td></tr>'
    s = f'<div class="cover"><h1>{t}</h1><div class="meta">Semester 2 · Weeks 1–12 · every question gives code and asks for its output / result</div>'
    s += '''<div class="box"><b>Instructions</b><ul style="margin:1mm 0 0 4mm;padding:0">
<li>100 marks: <b>Section A</b> — 16 select-all multiple-choice questions (2 marks each = 32); <b>Section B</b> — 13 short-answer questions (68 marks).</li>
<li>No computer is allowed: every answer can be derived by hand or with a scientific calculator. Randomness is always supplied explicitly (no unseeded random calls).</li>
<li>Library behaviour is as in the unit notebooks: NumPy ≥ 2, scikit-learn 1.x, statsmodels/patsy, PyTorch 2.x, pgmpy 1.1 (<code>DiscreteBayesianNetwork</code>, <code>DiscreteMarkovNetwork</code>). Arrays are printed by NumPy defaults.</li>
<li>For multiple-choice questions select <b>all</b> correct options; one or more may be correct.</li></ul></div>'''
    s += '<table><tr><th>Week</th><th>Questions</th></tr>' + rows + '</table>'
    if answers:
        s += '<div class="box small">Mọi output trong tài liệu này được <b>chạy thật</b> bằng Python 3.13 (numpy 2.3, scikit-learn 1.7, pgmpy 1.1.2, PyTorch 2.11) rồi mới viết lời giải. Lời giải bằng tiếng Việt, thuật ngữ giữ tiếng Anh.</div>'
    s += '</div>'
    return s

def render(answers):
    h = head('FIT5149 Code-Reading Mock', '')
    h += cover(answers)
    n = 0
    h += '<h2>Section A — Multiple choice (select all correct options) · 32 marks</h2>'
    for q in MCQ:
        n += 1
        h += f'<div class="q"><div class="qh"><span class="marks">(2 marks)</span>Question {n} <span class="wk">· {q["week"]}</span></div>'
        h += f'<div>{q["stem"]}</div>' + pre(CODE[q['code']])
        if q.get('show_output'):
            h += '<div class="small">Printed output:</div>' + pre(OUT[q['code']], 'out')
        if not answers:
            for i, (txt, ok, why) in enumerate(q['options']):
                h += f'<div class="opt"><b class="l">{L[i]}.</b>{txt}</div>'
            h += '<div class="ans">Answer: <span class="line"></span></div>'
        else:
            if not q.get('show_output'):
                h += '<div class="small">Output (đã chạy thật):</div>' + pre(OUT[q['code']], 'out')
            for i, (txt, ok, why) in enumerate(q['options']):
                cls = 'ok' if ok else 'no'; tag = '✔ ĐÚNG' if ok else '✘ SAI'
                h += f'<div class="v {cls}"><b>{L[i]}.</b> {txt}<br><span class="tag">{tag}</span> — {why}</div>'
            h += f'<div class="key">{q["key_note"]}</div>'
        h += '</div>'
    h += '<h2>Section B — Short answer · 68 marks</h2>'
    for q in SA:
        n += 1
        h += f'<div class="q long"><div class="qh"><span class="marks">({q["marks"]} marks)</span>Question {n} <span class="wk">· {q["week"]}</span></div>'
        h += f'<div>{q["stem"]}</div>' + pre(CODE[q['code']])
        if q.get('code2'):
            h += '<div class="small">Part 2:</div>' + pre(CODE[q['code2']])
        h += '<div class="parts">' + ''.join(f'<div>{p} <span class="small">[{m}]</span></div>' for p, m in q['parts']) + '</div>'
        if answers:
            outs = OUT[q['code']] + (('\n--- part 2 ---\n' + OUT[q['code2']]) if q.get('code2') else '')
            h += '<div class="small" style="margin-top:2mm">Output (đã chạy thật):</div>' + pre(outs, 'out')
            h += f'<div class="sol">{q["sol"]}</div>'
        h += '</div>'
    h += '</body></html>'
    return h

here = os.path.dirname(os.path.abspath(__file__))
dst = os.path.dirname(here)
open(os.path.join(dst, 'FIT5149_Code_Output_Exam.html'), 'w').write(render(False))
open(os.path.join(dst, 'FIT5149_Code_Output_Exam_Answers.html'), 'w').write(render(True))
tot = 2*len(MCQ) + sum(q['marks'] for q in SA); print('total marks', tot, 'questions', len(MCQ)+len(SA))
