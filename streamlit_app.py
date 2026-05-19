import streamlit as st

st.set_page_config(page_title="Optimizare CNC & Confecții", layout="centered")
st.title("⚙️ Optimizare CNC & Confecții Metalice")

tip_material = st.radio("Material de optimizat:", ["Foi de tablă (CNC Plasmă)", "Bare (Confecții)", "Panouri Bond"])

# ==========================================
# 1. FOI DE TABLĂ
# ==========================================
if tip_material == "Foi de tablă (CNC Plasmă)":
    piese_input = st.text_area("Introdu piesele (LungimexLățimexCantitate):", value="200x100x80")
    if st.button("Calculează Table"):
        try:
            parti = piese_input.strip().lower().replace(" ", "").split("x")
            p_lungime, p_latime, cantitate_ceruta = int(parti[0]), int(parti[1]), int(parti[2])
            X_MAX, Y_MAX = 920, 2000
            
            piese_pe_X_1, piese_pe_Y_1 = X_MAX // p_latime, Y_MAX // p_lungime
            total_1 = piese_pe_X_1 * piese_pe_Y_1
            piese_pe_X_2, piese_pe_Y_2 = X_MAX // p_lungime, Y_MAX // p_latime
            total_2 = piese_pe_X_2 * piese_pe_Y_2
            
            if total_1 >= total_2:
                x_buc, y_buc, dim_X, dim_Y = piese_pe_X_1, piese_pe_Y_1, p_latime, p_lungime
            else:
                x_buc, y_buc, dim_X, dim_Y = piese_pe_X_2, piese_pe_Y_2, p_lungime, p_latime
            
            total_piese_foaie = x_buc * y_buc
            foi_necesare = (cantitate_ceruta + total_piese_foaie - 1) // total_piese_foaie
            
            st.success(f"Necesar: {foi_necesare} foi. Capacitate: {total_piese_foaie} buc/foaie.")
        except:
            st.error("Format incorect! Exemplu: 200x100x80")

# ==========================================
# 2. BARE (CONFECȚII)
# ==========================================
elif tip_material == "Bare (Confecții)":
    piese_input = st.text_area("Introdu piesele (LungimexCantitate, una pe rând):", value="1500x4\n800x10")
    if st.button("Calculează Bare"):
        try:
            linii = piese_input.strip().lower().split("\n")
            lista_piese = []
            for linie in linii:
                if "x" in linie:
                    parti = linie.replace(" ", "").split("x")
                    lista_piese.extend([int(parti[0])] * int(parti[1]))
            
            lista_piese.sort(reverse=True)
            BARA_MAX, PANZA = 6000, 3
            bare_folosite = []
            
            for piesa in lista_piese:
                plasat = False
                for bara in bare_folosite:
                    if piesa <= BARA_MAX - (sum(bara) + len(bara) * PANZA):
                        bara.append(piesa)
                        plasat = True
                        break
                if not plasat:
                    bare_folosite.append([piesa])
            
            st.write(f"Total bare de 6m necesare: {len(bare_folosite)}")
            for i, bara in enumerate(bare_folosite, 1):
                st.write(f"Bară {i}: {' + '.join([str(p)+'mm' for p in bara])}")
        except:
            st.error("Format incorect! Exemplu: 1500x4")

# ==========================================
# 3. PANOURI BOND
# ==========================================
else:
    format_bond = st.radio("Format:", ["1500x3200", "1500x4050", "2000x4050"])
    DISC = st.number_input("Grosime disc (mm):", value=3)
    piese_input = st.text_area("Introdu casete (LungimexLățimexCantitate):", value="4000x1000x4")
    
    if st.button("Calculează Bond"):
        try:
            FOAIE_X, FOAIE_Y = map(int, format_bond.split("x"))
            linii = piese_input.strip().lower().split("\n")
            toate_piesele = []
            for linie in linii:
                parti = linie.replace(" ", "").split("x")
                p_l, p_L = min(int(parti[0]), int(parti[1])), max(int(parti[0]), int(parti[1]))
                toate_piesele.extend([{"L": p_L, "l": p_l}] * int(parti[2]))
            
            toate_piesele.sort(key=lambda p: (p["l"], p["L"]), reverse=True)
            foi = []
            
            for piesa in toate_piesele:
                plasat = False
                for foaie in foi:
                    for rand in foaie:
                        if piesa["l"] <= rand["h"] and piesa["L"] <= FOAIE_Y - rand["l_ocupata"]:
                            rand["piese"].append(piesa)
                            rand["l_ocupata"] += piesa["L"] + DISC
                            plasat = True; break
                    if plasat: break
                    if sum(r["h"] for r in foaie) + piesa["l"] + DISC <= FOAIE_X:
                        foaie.append({"h": piesa["l"], "l_ocupata": piesa["L"] + DISC, "piese": [piesa]})
                        plasat = True; break
                if not plasat:
                    foi.append([{"h": piesa["l"], "l_ocupata": piesa["L"] + DISC, "piese": [piesa]}])
            
            st.success(f"Necesar: {len(foi)} foi de Bond.")
        except Exception as e:
            st.error(f"Eroare: {e}")