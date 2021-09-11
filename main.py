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

@app.route ("/generate_from_frequencies", methods=["GET", "POST"])
def generate_freq ():
    words=request.form.getlist ("word")
    freqs=request.form.getlist ("frequency")
    try:
        freqs=[int (i) for i in freqs]
    except:
        return "Error: one or more frequency value are invalid", 400
    wf=dict(zip(words, freqs))

    width=int (request.form ["width"])
    height=int (request.form ["height"])
    bgcolor=request.form ["bgcolor"]
    colormap=request.form ["colormap"]
    prefer_horizontal=float (request.form ["prefer_horizontal"])
    relative_scaling=float (request.form ["relative_scaling"])
    monocolor_enabled=request.form.get ("monocolor_enabled")
    monocolor=request.form ["monocolor"]

    #Those checks are implemented for security reasons
    #In case of POST requests made bypassing the frontend
    if width > max_width:
        return f"Error: width > {max_width}", 400
    if height > max_height:
        return f"Error: height > {max_height}", 400

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

@app.route ("/generate_from_text", methods=["GET", "POST"])
def generate_text ():
    input_text=request.form ["input_text"]
    stopwords=request.form ["stopwords"]
    stopwords=set (stopwords.splitlines())

    width=int (request.form ["width"])
    height=int (request.form ["height"])
    max_words=int (request.form ["max_words"])
    bgcolor=request.form ["bgcolor"]
    colormap=request.form ["colormap"]
    prefer_horizontal=float (request.form ["prefer_horizontal"])
    relative_scaling=float (request.form ["relative_scaling"])
    monocolor_enabled=request.form.get ("monocolor_enabled")
    monocolor=request.form ["monocolor"]

    #Those checks are implemented for security reasons
    #In case of POST requests made bypassing the frontend
    if width > max_width:
        return f"Error: width > {max_width}"
    if height > max_height:
        return f"Error: height > {max_height}"

    if monocolor_enabled == "on":
        wc=WordCloud (
        width=width,
        height=height,
        max_words=max_words,
        colormap=colormap,
        background_color=bgcolor,
        prefer_horizontal=prefer_horizontal,
        relative_scaling=relative_scaling,
        color_func = lambda *args, **kwargs: monocolor,
        stopwords=stopwords).generate_from_text (input_text)
    else:
        wc=WordCloud (
        width=width,
        height=height,
        max_words=max_words,
        colormap=colormap,
        background_color=bgcolor,
        prefer_horizontal=prefer_horizontal,
        relative_scaling=relative_scaling,
        stopwords=stopwords).generate_from_text (input_text)

    wc_img=wc.to_image()
    buff=BytesIO ()
    wc_img.save (buff, format="PNG")
    img_b64=base64.b64encode (buff.getvalue()).decode("utf-8")

    return render_template ("generate.html", img_b64=img_b64)

#This endpoint is just for keeping the app always alive using Heroku base plan
#A cron job makes requests at a regular interval
@app.route ("/ping")
def ping ():
    return "OK", 200

if __name__ == "__main__":
    app.run (debug=False)
