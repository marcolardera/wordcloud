from flask import Flask, render_template, request
from wordcloud import WordCloud
from io import BytesIO
from colormaps import colormap_list
import base64

max_width=1920
max_height=1080

app=Flask (__name__)

@app.route ("/")
def main ():
    return render_template ("index.html", colormap_list=colormap_list, max_width=max_width, max_height=max_height)

@app.route ("/generate", methods=["GET", "POST"])
def generate ():
    words=request.form.getlist ("word")
    freqs=request.form.getlist ("frequency")
    try:
        freqs=[int (i) for i in freqs]
    except:
        return "Error: one or more frequency value are invalid"
    wf=dict(zip(words, freqs))

    width=int (request.form ["width"])
    height=int (request.form ["height"])
    bgcolor=request.form ["bgcolor"]
    colormap=request.form ["colormap"]
    prefer_horizontal=float (request.form ["prefer_horizontal"])
    relative_scaling=float (request.form ["relative_scaling"])
    monocolor_enabled=request.form.get ("monocolor-enabled")
    monocolor=request.form ["monocolor"]

    #Those checks are implemented for security reasons
    if width > max_width:
        return f"Error: width > {max_width}"
    if height > max_height:
        return f"Error: height > {max_height}"

    if monocolor_enabled == "on":
        wc=WordCloud (
        width=width,
        height=height,
        colormap=colormap,
        background_color=bgcolor,
        prefer_horizontal=prefer_horizontal,
        relative_scaling=relative_scaling,
        color_func = lambda *args, **kwargs: monocolor).generate_from_frequencies (wf)
    else:
        wc=WordCloud (
        width=width,
        height=height,
        colormap=colormap,
        background_color=bgcolor,
        prefer_horizontal=prefer_horizontal,
        relative_scaling=relative_scaling).generate_from_frequencies (wf)

    wc_img=wc.to_image()
    buff=BytesIO ()
    wc_img.save (buff, format="PNG")
    img_b64=base64.b64encode (buff.getvalue()).decode("utf-8")

    return render_template ("generate.html", img_b64=img_b64)

if __name__ == "__main__":
    app.run ()
