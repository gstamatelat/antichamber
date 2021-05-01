text_size_cache = {}


def execute(command, success_codes=None):
    if success_codes is None:
        success_codes = [0]
    import subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode not in success_codes:
        print(stdout.decode('UTF-8'), stderr.decode('UTF-8'))
        raise ValueError("Process {} failed with return code {}".format(command[0], process.returncode))
    return process.returncode, stdout.decode('UTF-8'), stderr.decode('UTF-8')


def potrace(image_in_path, image_out_path):
    import settings
    execute([settings.args.potrace, '-b', 'pdf', image_in_path, '-o', image_out_path])


def convert(image_in_path, image_out_path):
    import settings
    execute([settings.args.magick, 'convert', image_in_path, image_out_path])


def negate(image_path):
    import settings
    execute([settings.args.magick, 'mogrify', '-negate', image_path])


def latex(engine, code, output_file):
    import tempfile
    import os
    tmp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    tmp_file.write(code)
    tmp_file.close()
    path, file = os.path.split(output_file)
    execute([engine, '-interaction=nonstopmode', '-output-directory', path, '-jobname', os.path.splitext(file)[0],
             tmp_file.name])
    os.remove(tmp_file.name)


def xelatex(code, output_file):
    import settings
    return latex(settings.args.xelatex, code, output_file)


def pdflatex(code, output_file):
    import settings
    return latex(settings.args.pdflatex, code, output_file)


def quote_pdf(quote, font, output_pdf):
    import os
    with open("data/quote.tex", 'r') as tex_file:
        tex_string = tex_file.read()
    i_tex_string = tex_string.format(quote=quote, font_path=os.getcwd().replace("\\", "/") + "/data/font/", font=font)
    return xelatex(i_tex_string, output_pdf)


def text_size(text, font):
    import os
    import tempfile
    if text in text_size_cache:
        return text_size_cache[text]
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_file.close()
    quote_pdf(text, font, tmp_file.name)
    size = pdf_size(tmp_file.name)
    os.remove(tmp_file.name)
    text_size_cache[text] = size
    return size


def quote_pdf_best(quote, font, output_pdf, ratio):
    best_fit_map = {}
    k = 1
    while True:
        error_map = {}
        for partition in enumerate_text_partitions(quote, k):
            sizes = [text_size(line, font)[0] for line in partition.split("\\\\")]
            error = sum((max(sizes) - size) ** 2 for size in sizes)
            error_map[partition] = error
        min_key = min(error_map.keys(), key=lambda x: error_map[x])
        min_text_size = text_size(min_key, font)
        font_scale = min(ratio / min_text_size[0], 1 / min_text_size[1])
        best_fit_map[min_key] = font_scale
        if min_text_size[0] / min_text_size[1] < ratio:
            break
        else:
            k += 1
    best_fit = max(best_fit_map.keys(), key=lambda x: best_fit_map[x])
    return quote_pdf(best_fit, font, output_pdf)


def pdf_size(pdf_path):
    import settings
    return_code, stdout, stderr = execute([settings.args.pdfinfo, pdf_path])
    pdfsize = list(filter(lambda x: x.startswith("Page size:"), stdout.split('\n')))
    assert len(pdfsize) == 1
    pdfsize = pdfsize[0]
    pdfsize = pdfsize[len("Page size:"):].strip()
    pdfsize = pdfsize[:-len("pts")].strip()
    pdfsize = pdfsize.split("x")
    return float(pdfsize[0].strip()), float(pdfsize[1].strip())


def enumerate_text_partitions(text, k):
    partitions = []
    text = text.split(" ")
    assert len(text) >= k
    groups = []
    for i in range(k - 1):
        groups.append([text[0]])
        text = text[1:]
    groups.append(text)
    partitions.append("\\\\".join([" ".join(g) for g in groups]))
    while True:
        c = 0
        for i in reversed(range(0, k)):
            if len(groups[i]) > 1:
                c = i
                break
        if c == 0:
            return partitions
        groups[c - 1].append(groups[c][0])
        groups[c] = groups[c][1:]
        for i in range(c, k - 1):
            groups[i + 1] = groups[i][1:] + groups[i + 1]
            groups[i] = [groups[i][0]]
        partitions.append("\\\\".join([" ".join(g) for g in groups]))
