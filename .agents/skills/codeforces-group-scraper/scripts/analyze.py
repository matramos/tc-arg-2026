#!/usr/bin/env python3
import json
import sys
import re
from collections import Counter, defaultdict

def parse_contest_info(name):
    # Determine Day
    day_match = re.search(r'(?:day|día|dia|contest\s*#)\s*(\d+)', name, re.IGNORECASE)
    day = int(day_match.group(1)) if day_match else None
    
    # Determine Level
    level = None
    if re.search(r'inicial', name, re.IGNORECASE):
        level = 'Inicial'
    elif re.search(r'avanzado', name, re.IGNORECASE):
        level = 'Avanzado'
        
    return day, level

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze.py <submissions_json_file>", file=sys.stderr)
        sys.exit(1)
        
    filepath = sys.argv[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    submissions = data.get("submissions", [])
    contests_info = {c["id"]: c["name"] for c in data.get("contests", [])}
    
    total_subs = len(submissions)
    print(f"Loaded {total_subs} submissions.")
    
    # 1. Contest details mapping
    contest_stats = defaultdict(lambda: {
        "name": "",
        "submissions_count": 0,
        "accepted_count": 0,
        "users": set(),
        "problems": set(),
        "day": None,
        "level": None
    })
    
    for c_id, c_name in contests_info.items():
        day, level = parse_contest_info(c_name)
        contest_stats[c_id]["name"] = c_name
        contest_stats[c_id]["day"] = day
        contest_stats[c_id]["level"] = level
        
    # 2. Process submissions
    unique_users_all = set()
    unique_problems_all = set()
    problems_per_contest = defaultdict(set) # (contest_id) -> set of problem letters/names
    
    languages = []
    verdicts = []
    
    # Submissions per day and level: (day, level) -> count
    subs_by_day_level = defaultdict(int)
    
    for sub in submissions:
        c_id = sub["contest_id"]
        user = sub["user"]
        prob = sub["problem"]
        lang = sub["language"]
        verdict = sub["verdict"]
        
        unique_users_all.add(user)
        
        prob_clean = prob
        if " - " in prob:
            parts = prob.split(" - ", 1)
            prob_letter = parts[0].strip()
            prob_name = parts[1].strip()
            prob_clean = prob_name
            problems_per_contest[c_id].add(prob_letter)
        else:
            prob_clean = prob.strip()
            problems_per_contest[c_id].add(prob_clean)
            
        unique_problems_all.add(prob_clean.lower())
        
        # Track for contest
        stats = contest_stats[c_id]
        stats["submissions_count"] += 1
        stats["users"].add(user)
        stats["problems"].add(prob_clean.lower())
        
        # Track languages
        languages.append(lang)
        
        # Track verdicts
        verdicts.append(verdict)
        if "accepted" in verdict.lower() or "ok" in verdict.lower():
            stats["accepted_count"] += 1
            
        # Day & Level submissions
        day = stats["day"]
        level = stats["level"]
        if day and level:
            subs_by_day_level[(day, level)] += 1
            
    # Calculate problem stats
    total_problems_with_dups = sum(len(probs) for probs in problems_per_contest.values())
    unique_problems_count = len(unique_problems_all)
    
    # 3. Compile LaTeX Code for Stats Frame
    num_contests = len(contests_info)
    avg_problems_per_contest = total_problems_with_dups / num_contests if num_contests > 0 else 0
    
    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Estadísticas del Training Camp'")
    print("="*50)
    stats_latex = f"""\\begin{{frame}}{{Estadísticas del Training Camp}}
\\begin{{center}}
\\Large
\\textbf{{Grupo:}} Training Camp Argentina 2026

\\vspace{{0.3cm}}

\\normalsize
\\begin{{itemize}}
\\item \\textbf{{Total de Contests:}} {num_contests}
\\item \\textbf{{Total de Problemas (incluyendo duplicados):}} {total_problems_with_dups}
\\item \\textbf{{Problemas Únicos:}} {unique_problems_count}
\\item \\textbf{{Promedio por Contest:}} {avg_problems_per_contest:.2f} problemas
\\end{{itemize}}

\\end{{center}}
\\end{{frame}}"""
    print(stats_latex)
    
    # 4. Generate LaTeX for Submissions per Day Chart
    max_day_val = 0
    for day in range(1, 9):
        max_day_val = max(max_day_val, subs_by_day_level.get((day, "Inicial"), 0))
        max_day_val = max(max_day_val, subs_by_day_level.get((day, "Avanzado"), 0))
        
    y_axis_max_val = ((max_day_val // 200) + 1) * 200 if max_day_val > 0 else 1800
    if y_axis_max_val < 1000:
        y_axis_max_val = 1000
    
    scale_y = 8.0 / y_axis_max_val if y_axis_max_val > 0 else 1.0
    
    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Submissions por Día - Gráfico'")
    print("="*50)
    
    # Generate Y-axis labels dynamically
    y_labels = []
    step = y_axis_max_val // 9
    if step > 100:
        step = ((step // 50) + 1) * 50
    elif step > 10:
        step = ((step // 5) + 1) * 5
    else:
        step = 100
        
    y_ticks = []
    current_y = 0
    while current_y <= y_axis_max_val:
        y_ticks.append(current_y)
        current_y += step
    
    y_axis_max_val = y_ticks[-1]
    scale_y = 8.0 / y_axis_max_val
    
    y_ticks_str = ", ".join([f"{idx}/{val}" for idx, val in enumerate(y_ticks)])
    
    bars_inicial = []
    bars_avanzado = []
    for day in range(1, 9):
        val_i = subs_by_day_level.get((day, "Inicial"), 0)
        h_i = val_i * scale_y
        bars_inicial.append(f"\\fill[blue!80] ({day-1}.6,0) rectangle ({day-1}.9,{h_i:.3f}); % Day {day} ({val_i})")
        
        val_a = subs_by_day_level.get((day, "Avanzado"), 0)
        h_a = val_a * scale_y
        bars_avanzado.append(f"\\fill[red!80] ({day}.1,0) rectangle ({day}.4,{h_a:.3f}); % Day {day} ({val_a})")
        
    chart_latex = f"""\\begin{{frame}}{{Submissions por Día - Gráfico}}
\\begin{{center}}

\\vspace{{0.1cm}}

\\begin{{tikzpicture}}[scale=0.7]
% Y-axis (submissions)
\\draw[->,very thick] (0,0) -- (0,9) node[above] {{\\textbf{{Submissions}}}};
\\foreach \\y/\\label in {{{y_ticks_str}}} {{
    \\draw[thick] (0,\\y) -- (-0.15,\\y) node[left] {{\\textbf{{\\label}}}};
}}

% X-axis (days)
\\draw[->,very thick] (0,0) -- (9,0) node[right] {{\\textbf{{Días}}}};
\\foreach \\x in {{1,2,3,4,5,6,7,8}} {{
    \\draw[thick] (\\x,0) -- (\\x,-0.15) node[below] {{\\textbf{{\\x}}}};
}}

% Bars for Inicial submissions (blue)
""" + "\n".join(bars_inicial) + "\n\n% Bars for Avanzado submissions (red)\n" + "\n".join(bars_avanzado) + f"""

% Legend
\\fill[blue!80] (9.5,8.3) rectangle (10.2,8.7);
\\node[right] at (10.3,8.5) {{\\textbf{{Inicial}}}};
\\fill[red!80] (9.5,7.3) rectangle (10.2,7.7);
\\node[right] at (10.3,7.5) {{\\textbf{{Avanzado}}}};

\\end{{tikzpicture}}
\\end{{center}}
\\end{{frame}}"""
    print(chart_latex)
    
    # 5. Languages
    lang_counter = Counter()
    other_lang_counter = Counter()
    for lang in languages:
        l_lower = lang.lower()
        if "c++23" in l_lower or "c++ 23" in l_lower:
            lang_counter["C++23"] += 1
        elif "c++20" in l_lower or "c++ 20" in l_lower:
            lang_counter["C++20"] += 1
        elif "c++17" in l_lower or "c++ 17" in l_lower:
            lang_counter["C++17"] += 1
        elif "python" in l_lower or "pypy" in l_lower:
            lang_counter["Python"] += 1
        else:
            lang_counter["Otros"] += 1
            other_lang_counter[lang] += 1
            
    total_langs = sum(lang_counter.values())
    lang_pcts = {k: (v / total_langs)*100 for k, v in lang_counter.items()}
    sorted_lang_pcts = sorted(lang_pcts.items(), key=lambda x: x[1], reverse=True)
    lang_pie_str = ", ".join([f"{pct:.1f}/{name}" for name, pct in sorted_lang_pcts])
    
    other_langs_list = []
    for o_lang, o_count in other_lang_counter.most_common():
        other_langs_list.append(f"{o_lang} ({o_count})")
    
    if other_langs_list:
        other_langs_str = ", ".join(other_langs_list)
        other_langs_latex = f"""
\\vspace{{0.3cm}}
\\small
\\textbf{{Otros incluye:}} {other_langs_str}"""
    else:
        other_langs_latex = ""
    
    # Verdicts
    verdict_counter = Counter()
    for verd in verdicts:
        v_lower = verd.lower()
        if "accepted" in v_lower or "ok" in v_lower:
            verdict_counter["Accepted"] += 1
        elif "wrong answer" in v_lower or "wa" in v_lower:
            verdict_counter["Wrong Answer"] += 1
        elif "time limit" in v_lower or "tle" in v_lower:
            verdict_counter["Time Limit"] += 1
        elif "runtime error" in v_lower or "re" in v_lower:
            verdict_counter["Runtime Error"] += 1
        elif "compilation" in v_lower or "ce" in v_lower:
            verdict_counter["Compilation"] += 1
        elif "memory limit" in v_lower or "mle" in v_lower:
            verdict_counter["Memory Limit"] += 1
        else:
            verdict_counter["Otros"] += 1
            
    total_verdicts = sum(verdict_counter.values())
    verd_pcts = {k: (v / total_verdicts)*100 for k, v in verdict_counter.items()}
    sorted_verd_pcts = sorted(verd_pcts.items(), key=lambda x: x[1], reverse=True)
    verd_pie_str = ", ".join([f"{pct:.1f}/{name}" for name, pct in sorted_verd_pcts if pct > 0.5])
    
    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Lenguajes Utilizados'")
    print("="*50)
    languages_latex = f"""\\begin{{frame}}{{Lenguajes Utilizados}}
\\begin{{center}}

\\vspace{{0.2cm}}

\\begin{{tikzpicture}}
\\pie[text=legend, radius=1.8, sum=auto, after number=\\%]
  {{{lang_pie_str}}}
\\end{{tikzpicture}}
{other_langs_latex}
\\end{{center}}
\\end{{frame}}"""
    print(languages_latex)
    
    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Respuestas del Juez'")
    print("="*50)
    verdicts_latex = f"""\\begin{{frame}}{{Respuestas del Juez}}
\\begin{{center}}

\\vspace{{0.2cm}}

\\begin{{tikzpicture}}
\\pie[text=legend, radius=1.8, sum=auto, after number=\\%]
  {{{verd_pie_str}}}
\\end{{tikzpicture}}
\\end{{center}}
\\end{{frame}}"""
    print(verdicts_latex)
    
    # 6. Additional metrics
    most_users_contest = max(contest_stats.items(), key=lambda x: len(x[1]["users"]))
    most_users_count = len(most_users_contest[1]["users"])
    most_users_name = most_users_contest[1]["name"]
    
    most_subs_contest = max(contest_stats.items(), key=lambda x: x[1]["submissions_count"])
    most_subs_count = most_subs_contest[1]["submissions_count"]
    most_subs_name = most_subs_contest[1]["name"]
    
    avg_subs_per_contest = total_subs / num_contests if num_contests > 0 else 0
    total_unique_users = len(unique_users_all)
    subs_per_user = total_subs / total_unique_users if total_unique_users > 0 else 0
    
    inicial_contests = [(k, v) for k, v in contest_stats.items() if v["level"] == "Inicial" and v["submissions_count"] > 0]
    if inicial_contests:
        best_inicial = max(inicial_contests, key=lambda x: x[1]["accepted_count"] / x[1]["submissions_count"])
        best_inicial_name = best_inicial[1]["name"]
        best_inicial_pct = (best_inicial[1]["accepted_count"] / best_inicial[1]["submissions_count"]) * 100
    else:
        best_inicial_name = "N/A"
        best_inicial_pct = 0.0
        
    all_active_contests = [(k, v) for k, v in contest_stats.items() if v["submissions_count"] > 0]
    if all_active_contests:
        hardest = min(all_active_contests, key=lambda x: x[1]["accepted_count"] / x[1]["submissions_count"])
        hardest_name = hardest[1]["name"]
        hardest_pct = (hardest[1]["accepted_count"] / hardest[1]["submissions_count"]) * 100
    else:
        hardest_name = "N/A"
        hardest_pct = 0.0
        
    prob_counts = [len(v["problems"]) for v in contest_stats.values() if v["submissions_count"] > 0]
    min_probs = min(prob_counts) if prob_counts else 0
    max_probs = max(prob_counts) if prob_counts else 0
    
    most_users_name_escaped = most_users_name.replace("#", "\\#")
    most_subs_name_escaped = most_subs_name.replace("#", "\\#")
    best_inicial_name_escaped = best_inicial_name.replace("#", "\\#")
    hardest_name_escaped = hardest_name.replace("#", "\\#")

    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Participación por Contest'")
    print("="*50)
    participation_latex = f"""\\begin{{frame}}{{Participación por Contest}}
\\begin{{center}}
\\Large
\\textbf{{Estadísticas de Participación}}

\\vspace{{0.6cm}}

\\large
\\begin{{itemize}}
\\item \\textbf{{Más Participantes:}} {most_users_name_escaped} ({most_users_count})
\\item \\textbf{{Más Submissions:}} {most_subs_name_escaped} ({most_subs_count:,})
\\item \\textbf{{Promedio Submissions:}} {avg_subs_per_contest:.0f} por contest
\\item \\textbf{{Participantes Únicos:}} {total_unique_users} total
\\end{{itemize}}
\\end{{center}}
\\end{{frame}}"""
    print(participation_latex)
    
    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Métricas de Rendimiento'")
    print("="*50)
    performance_latex = f"""\\begin{{frame}}{{Métricas de Rendimiento}}
\\begin{{center}}
\\Large
\\textbf{{Rendimiento de los Alumnos}}

\\vspace{{0.6cm}}

\\large
\\begin{{itemize}}
\\item \\textbf{{Submissions/Participante:}} {subs_per_user:.1f} promedio
\\item \\textbf{{Mejor Contest Inicial:}} {best_inicial_name_escaped} ({best_inicial_pct:.1f}\\% accepted)
\\item \\textbf{{Contest Más Difícil:}} {hardest_name_escaped} ({hardest_pct:.1f}\\% accepted)
\\item \\textbf{{Problemas Intentados:}} {min_probs}-{max_probs} por contest
\\end{{itemize}}
\\end{{center}}
\\end{{frame}}"""
    print(performance_latex)
    
    print("\n" + "="*50)
    print("LaTeX: Diapositiva 'Total de Submissions'")
    print("="*50)
    total_frame_latex = f"""\\begin{{frame}}{{Total de Submissions}}
\\begin{{center}}
\\Huge
\\textbf{{¡{total_subs:,} SUBMISSIONS!}}

\\vspace{{0.7cm}}

\\textsf{{\\Large En {num_contests} contests durante 8 días}}

\\vspace{{0.3cm}}

\\normalsize
\\begin{{itemize}}
\\item \\textbf{{{total_unique_users} participantes únicos}}
\\item \\textbf{{{len(data.get("submissions", []))} submissions analizadas}}
\\item \\textbf{{{total_problems_with_dups} problemas disponibles}}
\\item \\textbf{{{unique_problems_count} problemas únicos}}
\\end{{itemize}}

\\vspace{{0.7cm}}

\\textbf{{¡Gracias por hacer del Training Camp 2026 un éxito rotundo!}}
\\end{{center}}
\\end{{frame}}"""
    print(total_frame_latex)

if __name__ == "__main__":
    main()
