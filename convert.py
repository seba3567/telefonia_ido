import pandas as pd
import sys
import os
import json

def extraer_sin_titulos(input_file):
    # Limpiamos las comillas extra de la terminal MINGW64
    input_file = input_file.strip("'").strip('"')
    
    if not os.path.exists(input_file):
        print(f"❌ Archivo no encontrado: {input_file}")
        return

    print(f"🚀 Extracción por fuerza bruta en: {input_file}...")
    try:
        # header=None es la magia: lee todo como datos puros, sin títulos
        df = pd.read_excel(input_file, header=None, dtype=str)
        df = df.fillna('')

        fijos = []
        moviles = []
        voip = []

        # Recorremos el Excel fila por fila
        for index, row in df.iterrows():
            texto_fila = " ".join(row.values).upper()

            # Ignoramos la fila si es un encabezado colado o está vacía
            if "BLOQUE DE NUMERACIÓN" in texto_fila or "CABIDE" in texto_fila or not str(row[0]).strip():
                continue

            # Capturamos directo de las posiciones que nos dio tu consola
            bloque = str(row[0]).strip()
            ido_idd = str(row[1]).strip()
            empresa = str(row[4]).strip()

            # Validación de seguridad: si el bloque no empieza con un número, lo saltamos
            if len(bloque) < 5 or not bloque[0].isdigit():
                continue

            # Estructuramos el JSON
            registro = {
                "bloque": bloque,
                "empresa": empresa,
                "ido_idd": ido_idd
            }

            # Clasificamos buscando la palabra en TODA la fila, imposible que falle
            if 'LOCAL' in texto_fila:
                fijos.append(registro)
            elif 'MÓVIL' in texto_fila or 'MOVIL' in texto_fila:
                moviles.append(registro)
            elif 'INTERNET' in texto_fila or 'VOIP' in texto_fila or 'VOIN' in texto_fila:
                voip.append(registro)

        # Guardar los archivos físicos
        def guardar_json(datos, archivo):
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            print(f"✅ {archivo}: {len(datos)} registros extraídos.")

        guardar_json(fijos, 'fijos.json')
        guardar_json(moviles, 'moviles.json')
        guardar_json(voip, 'voip.json')

    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else 'tabla_numeracion_ido_idd_09-03-2026.xlsx'
    extraer_sin_titulos(archivo)