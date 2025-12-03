from io import BytesIO
import zipfile
import fitz  # PyMuPDF

async def POST(request):
    form = await request.form()
    files = form.getall("files")

    if not files:
        return Response("No files uploaded", status=400)

    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            pdf_in = await file.read()
            pdf_out = editar_pdf(pdf_in)
            zf.writestr(f"EDITADO_{file.filename}", pdf_out)

    mem_zip.seek(0)

    return Response(
        mem_zip.read(),
        headers={
            "Content-Type": "application/zip",
            "Content-Disposition": "attachment; filename=pdf_editados.zip",
        },
        status=200,
    )


def editar_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    URL_NEW = "https://riverlabs-solutions.com/"
    BORRAR = "Inspired by knowledge"
    DELETE_URLS = ["condalab.com", "www.condalab.com"]

    for page in doc:

        # Borrar textos viejos
        for pattern in [BORRAR] + DELETE_URLS:
            for rect in page.search_for(pattern):
                page.add_redact_annot(rect, fill=(1,1,1))
        page.apply_redactions()

        # Insertar URL nueva
        W, H = page.rect.width, page.rect.height
        page.insert_text((W - 150, H - 20), URL_NEW, fontsize=8)

    output = doc.tobytes()
    doc.close()
    return output
