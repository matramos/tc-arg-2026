#!/usr/bin/env python3
import requests
import random
import sys

def generar_sets_entrenamiento(handle):
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error al conectar con la API de Codeforces.")
        sys.exit(1)
        
    data = response.json()
    if data['status'] != 'OK':
        print(f"Error de la API: {data.get('comment', 'Desconocido')}")
        sys.exit(1)
        
    submissions = data['result']
    problemas_por_rating = {'muy_faciles': {}, 'faciles': {}, 'comunes': {}, 'dificiles': {}, 'muy_dificiles': {}}
    
    for sub in submissions:
        if sub.get('verdict') == 'OK':
            prob = sub.get('problem', {})
            if 'rating' not in prob or 'contestId' not in prob:
                continue
                
            rating = prob['rating']
            prob_id = f"{prob['contestId']}{prob['index']}"
            tags = prob.get('tags', [])
            tags_str = ", ".join(tags) if tags else "N/A"
            prob_url = f"https://codeforces.com/contest/{prob['contestId']}/problem/{prob['index']}"
            
            prob_info = {
                'id': prob_id,
                'name': prob['name'],
                'rating': rating,
                'url': prob_url,
                'tags': tags_str
            }
            
            if rating == 800:
                if prob_id not in problemas_por_rating['muy_faciles']:
                    problemas_por_rating['muy_faciles'][prob_id] = prob_info
            
            if 800 <= rating <= 1100:
                if prob_id not in problemas_por_rating['faciles']:
                    problemas_por_rating['faciles'][prob_id] = prob_info
            elif 1200 <= rating <= 1600:
                if prob_id not in problemas_por_rating['comunes']:
                    problemas_por_rating['comunes'][prob_id] = prob_info
            elif 1700 <= rating <= 2100:
                if prob_id not in problemas_por_rating['dificiles']:
                    problemas_por_rating['dificiles'][prob_id] = prob_info
                    
            if rating > 2000:
                if prob_id not in problemas_por_rating['muy_dificiles']:
                    problemas_por_rating['muy_dificiles'][prob_id] = prob_info

    req_muy_faciles, req_faciles, req_comunes, req_dificiles, req_muy_dificiles = 2, 4, 8, 4, 1
    
    if len(problemas_por_rating['muy_faciles']) < req_muy_faciles:
        print("No hay suficientes problemas resueltos con rating 800.")
        sys.exit(1)
    if len(problemas_por_rating['muy_dificiles']) < req_muy_dificiles:
        print("No hay suficientes problemas resueltos con rating > 2000.")
        sys.exit(1)
        
    seleccion_muy_faciles = random.sample(list(problemas_por_rating['muy_faciles'].values()), req_muy_faciles)
    seleccion_muy_dificiles = random.sample(list(problemas_por_rating['muy_dificiles'].values()), req_muy_dificiles)
    
    elegidos_faciles_ids = {p['id'] for p in seleccion_muy_faciles}
    faciles_disponibles = [p for p in problemas_por_rating['faciles'].values() if p['id'] not in elegidos_faciles_ids]
    
    elegidos_dificiles_ids = {p['id'] for p in seleccion_muy_dificiles}
    dificiles_disponibles = [p for p in problemas_por_rating['dificiles'].values() if p['id'] not in elegidos_dificiles_ids]
    
    if len(faciles_disponibles) < req_faciles or \
       len(problemas_por_rating['comunes']) < req_comunes or \
       len(dificiles_disponibles) < req_dificiles:
        print(f"No hay suficientes problemas resueltos en uno o más rangos de rating.")
        print(f"Encontrados: Muy Fáciles: {len(problemas_por_rating['muy_faciles'])}/{req_muy_faciles}, "
              f"Fáciles: {len(faciles_disponibles)}/{req_faciles}, "
              f"Comunes: {len(problemas_por_rating['comunes'])}/{req_comunes}, "
              f"Difíciles: {len(dificiles_disponibles)}/{req_dificiles}, "
              f"Muy Difíciles: {len(problemas_por_rating['muy_dificiles'])}/{req_muy_dificiles}")
        sys.exit(1)

    seleccion_faciles = random.sample(faciles_disponibles, req_faciles)
    seleccion_comunes = random.sample(list(problemas_por_rating['comunes'].values()), req_comunes)
    seleccion_dificiles = random.sample(dificiles_disponibles, req_dificiles)

    return seleccion_muy_faciles, seleccion_faciles, seleccion_comunes, seleccion_dificiles, seleccion_muy_dificiles

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_sets.py <handle_codeforces>")
        sys.exit(1)
    
    handle = sys.argv[1]
    muy_faciles, faciles, comunes, dificiles, muy_dificiles = generar_sets_entrenamiento(handle)
    
    print(f"=== SETS DE ENTRENAMIENTO GENERADOS PARA EL HANDLE: {handle} ===\n")
    
    print("--- CONTEST INICIAL ---")
    print("Problemas Exclusivos Muy Fáciles:")
    for p in muy_faciles:
        print(f"- [{p['id']}] {p['name']} (Rating: {p['rating']}) [Tags: {p['tags']}] - {p['url']}")
        
    print("\nProblemas Exclusivos Fáciles:")
    for p in faciles:
        print(f"- [{p['id']}] {p['name']} (Rating: {p['rating']}) [Tags: {p['tags']}] - {p['url']}")
    
    print("\nProblemas de Base Común:")
    for p in comunes:
        print(f"- [{p['id']}] {p['name']} (Rating: {p['rating']}) [Tags: {p['tags']}] - {p['url']}")
        
    print("\n-----------------------\n")
    
    print("--- CONTEST AVANZADO ---")
    print("Problemas de Base Común:")
    for p in comunes:
        print(f"- [{p['id']}] {p['name']} (Rating: {p['rating']}) [Tags: {p['tags']}] - {p['url']}")
        
    print("\nProblemas Exclusivos Difíciles:")
    for p in dificiles:
        print(f"- [{p['id']}] {p['name']} (Rating: {p['rating']}) [Tags: {p['tags']}] - {p['url']}")
        
    print("\nProblemas Exclusivos Muy Difíciles (> 2000):")
    for p in muy_dificiles:
        print(f"- [{p['id']}] {p['name']} (Rating: {p['rating']}) [Tags: {p['tags']}] - {p['url']}")
