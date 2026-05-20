import streamlit as st

st.set_page_config(page_title="Optimizare Plasmă, Bare & Bond", layout="centered")
st.title("⚙️ Optimizare CNC & Confecții Metalice")

# Meniu principal
tip_material = st.radio("Material de optimizat:", ["Foi de tablă (CNC Plasmă)", "Bare (Confecții)", "Panouri Bond"])

# ==========================================
# 1. SECȚIUNEA FOI DE TABLĂ (CNC PLASMĂ)
# ==========================================
if tip_material == "Foi de tablă (CNC Plasmă)":
    piese_input = st.text_area("Introdu piesele (LungimexLățimexCantitate):", value="200x100x80", key="tablar")
    
    if st.button("Calculează Table"):
        try:
            text_curat = piese_input.strip().lower().replace(" ", "")
            X_MAX, Y_MAX = 920, 2000
            
            parti = text_curat.split("x")
            p_lungime, p_latime, cantitate_ceruta = int(parti[0]), int(parti[1]), int(parti[2])
            
            piese_pe_X_1, piese_pe_Y_1 = X_MAX // p_latime, Y_MAX // p_lungime
            total_1 = piese_pe_X_1 * piese_pe_Y_1
            
            piese_pe_X_2, piese_pe_Y_2 = X_MAX // p_lungime, Y_MAX // p_latime
            total_2 = piese_pe_X_2 * piese_pe_Y_2
            
            if total_1 >= total_2:
                x_buc, y_buc, dim_X, dim_Y = piese_pe_X_1, piese_pe_Y_1, p_latime, p_lungime
            else:
                x_buc, y_buc, dim_X, dim_Y = piese_pe_X_2, piese_pe_Y_2, p_lungime, p_latime
            
            total_piese_foaie = x_buc * y_buc
            
            if total_piese_foaie == 0:
                st.error("Piesa este prea mare pentru spațiul util de 2000x920 mm!")
            else:
                foi_necesare = (cantitate_ceruta + total_piese_foaie - 1) // total_piese_foaie
                rest_X = X_MAX - (x_buc * dim_X)
                rest_Y = Y_MAX - (y_buc * dim_Y)
                
                st.success("Plan Foaie Tablă Generat:")
                st.markdown(f"""
                ### 📊 Raport Debitări Foaie (Linie Comună)
                * **Orientare optimă:** {dim_X} mm pe lățime (X) × {dim_Y} mm pe lungime (Y)
                * **Configurație:** **{x_buc} piese** pe lățime (X) și **{y_buc} piese** pe lungime (Y)
                * **Capacitate:** **{total_piese_foaie} bucăți** per foaie
                * **Necesar stoc:** Pentru cele {cantitate_ceruta} piese, ai nevoie de **{foi_necesare} foi**
                
                ### 📐 Resturi recuperabile
                * **Fâșia pe Lățime (X):** **{rest_X} mm** (plus marginea moartă de 80 mm)
                * **Fâșia pe Lungime (Y):** **{rest_Y} mm**
                """)
        except:
            st.error("Format incorect! Folosește modelul: LungimexLățimexCantitate (Ex: 200x100x80)")

# ==========================================
# 2. SECȚIUNEA BARE (CONFECȚII)
# ==========================================
elif tip_material == "Bare (Confecții)":
    st.markdown("""
    * **Lungime bară brută:** **6000 mm**
    * **Grosime pânză:** **3 mm** (scăzută automat)
    """)
    piese_input = st.text_area("Introdu piesele (LungimexCantitate, o piesă pe rând):", value="1500x4\n800x10", key="barer")
    
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
                if piesa > BARA_MAX:
                    st.error(f"Piesa de {piesa} mm depășește lungimea de 6000 mm!")
                    st.stop()
                
                plasat = False
                for bara in bare_folosite:
                    spatiu_ramas = BARA_MAX - (sum(bara) + (len(bara) * PANZA))
                    if piesa <= spatiu_ramas:
                        bara.append(piesa)
                        plasat = True
                        break
                if not plasat:
                    bare_folosite.append([piesa])
            
            st.success("Plan Bare Generat:")
            st.markdown(f"### 📊 Raport Debitări Bare\n* **Total bare de 6m necesare:** **{len(bare_folosite)} bucăți**")
            for i, bara in enumerate(bare_folosite, 1):
                spatiu_utilizat = sum(bara) + ((len(bara) - 1) * PANZA if len(bara) > 0 else 0)
                rest_bara = max(0, BARA_MAX - spatiu_utilizat)
                st.markdown(f"**Bară #{i}:** [{' + '.join([f'{p}mm' for p in bara])}] ➡️ *Rest: {rest_bara} mm*")
        except:
            st.error("Format incorect! Introdu fiecare tip de piesă pe un rând nou (Ex:\n1500x4\n800x10)")

# ==========================================
# 3. SECȚIUNEA OPTIMIZARE BOND (FORMATURI NOI)
# ==========================================
else:
    format_bond = st.radio(
        "Alege formatul panoului Bond:", 
        ["1250 mm x 3200 mm", "1250 mm x 4050 mm", "1500 mm x 3200 mm", "1500 mm x 4050 mm"]
    )
    
    opțiune_disc = st.radio(
        "Grosime Debitare:",
        ["Disc 3 mm (Standard CNC / Frezare)", "Disc 0 mm (Cote lejere / Fără pierderi)"]
    )
    
    DISC = 3 if "3 mm" in opțiune_disc else 0
    
    st.markdown(f"""
    * *Fiecare tip de casetă se introduce pe un rând nou.*
    * **Grosime disc curentă:** **{DISC} mm** (scăzut automat doar între piese)
    """)
    
    # Mapare formate noi
    if "1250 mm x 3200 mm" in format_bond:
        FOAIE_X, FOAIE_Y = 1250, 3200
    elif "1250 mm x 4050 mm" in format_bond:
        FOAIE_X, FOAIE_Y = 1250, 4050
    elif "1500 mm x 3200 mm" in format_bond:
        FOAIE_X, FOAIE_Y = 1500, 3200
    else: # 1500 x 4050
        FOAIE_X, FOAIE_Y = 1500, 4050
        
    piese_input = st.text_area(
        "Introdu casetele Bond (LungimexLățimexCantitate, una pe rând):", 
        value="4000x1000x4", 
        key="bond_nesting_v8"
    )
    
    if st.button("Calculează Optimizare Inteligentă Bond"):
        try:
            text_procesat = piese_input.replace("\r", "")
            linii = text_procesat.strip().lower().split("\n")
            toate_piesele = []
            
            for linie in linii:
                linie_curata = linie.strip().replace(" ", "")
                if not linie_curata or "x" not in linie_curata:
                    continue
                    
                parti = linie_curata.split("x")
                if len(parti) < 3:
                    continue
                
                dim1 = int(parti[0].strip())
                dim2 = int(parti[1].strip())
                cant = int(parti[2].strip())
                
                p_lungime = max(dim1, dim2)
                p_latime = min(dim1, dim2)
                
                if p_latime > FOAIE_X or p_lungime > FOAIE_Y:
                    st.error(f"⚠️ Piesa {dim1}x{dim2} mm depășește fizic formatul foii ({FOAIE_X}x{FOAIE_Y} mm)!")
                    st.stop()
                
                for _ in range(cant):
                    toate_piesele.append({"L": p_lungime, "l": p_latime})
            
            if not toate_piesele:
                st.warning("Nu ai introdus nicio piesă validă.")
                st.stop()
                
            toate_piesele.sort(key=lambda p: (p["l"], p["L"]), reverse=True)
            foi = []
            
            for piesa in toate_piesele:
                plasat = False
                for foaie in foi:
                    for rand in foaie["randuri"]:
                        if piesa["l"] <= rand["inaltime"]:
                            spatiu_necesar_Y = piesa["L"] if rand["lungime_ocupata"] == 0 else piesa["L"] + DISC
                            if rand["lungime_ocupata"] + spatiu_necesar_Y <= FOAIE_Y:
                                rand["piese"].append(piesa)
                                rand["lungime_ocupata"] += spatiu_necesar_Y
                                plasat = True
                                break
                    if plasat: break
                    
                    latime_actuala_X = sum(r["inaltime"] for r in foaie["randuri"]) + (len(foaie["randuri"]) * DISC)
                    if latime_actuala_X + piesa["l"] <= FOAIE_X:
                        un_nou_rand = {"inaltime": piesa["l"], "lungime_ocupata": piesa["L"], "piese": [piesa]}
                        foaie["randuri"].append(un_nou_rand)
                        plasat = True
                        break
                
                if not plasat:
                    foi.append({"randuri": [{"inaltime": piesa["l"], "lungime_ocupata": piesa["L"], "piese": [piesa]}]})
            
            st.success("🔥 Optimizare Nesting Inteligent Finalizată!")
            st.markdown(f"### 📊 Necesar Total Stoc: **{len(foi)} foi de Bond** (Format {FOAIE_X}x{FOAIE_Y} mm)")
            
            for f_idx, foaie in enumerate(foi, 1):
                st.markdown(f"#### 📑 FOAIA # {f_idx}")
                total_latime_foaie_X = 0
                for r_idx, rand in enumerate(foaie["randuri"], 1):
                    total_latime_foaie_X += rand["inaltime"] + (DISC if r_idx > 1 else 0)
                    schita_piese = " + ".join([f"{p['L']}x{p['l']}mm" for p in rand["piese"]])
                    rest_lungime_rand = FOAIE_Y - rand["lungime_ocupata"]
                    st.markdown(f"**Rând {r_idx} [Lățime fâșie {rand['inaltime']}mm]:**\n&nbsp;&nbsp;&nbsp;&nbsp;📐 `[{schita_piese}]` ➡️ *Rest în capăt: {max(0, rest_lungime_rand)} mm*")
                
                rest_foaie_X = max(0, FOAIE_X - total_latime_foaie_X)
                st.info(f"➡️ **Fâșie disponibilă pe Lățimea foii (X): {rest_foaie_X} mm**")
                st.markdown("---")
        except Exception as e:
            st.error(f"Eroare tehnică la optimizare: {str(e)}.")