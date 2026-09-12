from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import re

URL = "https://deporflix.pe/canales/america-television/"
OUTPUT = "america.m3u"

def es_stream(url):
    u = url.lower()

    return (
        ".m3u8" in u
        or "playlist.php" in u
    )


def main():

    encontrados = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        def capturar(request):

            url = request.url

            if es_stream(url):

                # Evitar duplicados
                if url not in encontrados:
                    encontrados.append(url)

                    print("STREAM ENCONTRADO:")
                    print(url)

        page.on("request", capturar)

        print("Abriendo:")
        print(URL)

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        # Dar tiempo al reproductor para cargar
        page.wait_for_timeout(15000)

        # Intentar hacer clic en la primera opción
        try:
            page.get_by_text(
                "OPCIÓN 1 - América Televisión",
                exact=True
            ).click(timeout=5000)

            print("Opción 1 seleccionada")

            page.wait_for_timeout(10000)

        except Exception as e:
            print("No se pudo seleccionar la opción 1:")
            print(e)

        browser.close()


    # Eliminar posibles duplicados por URL
    encontrados = list(dict.fromkeys(encontrados))

    print()
    print("Total de streams:", len(encontrados))

    # Crear M3U
    with open(OUTPUT, "w", encoding="utf-8") as f:

        f.write("#EXTM3U\n")

        for i, stream in enumerate(encontrados, 1):

            f.write(
                f"#EXTINF:-1,América Televisión {i}\n"
            )

            f.write(stream + "\n")

    print("Archivo generado:", OUTPUT)


if __name__ == "__main__":
    main()
