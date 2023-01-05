"""
WordCloud Generator

A web frontend for the WordCloud Python package
Author: Marco Lardera <larderamarco@hotmail.com>
"""

from flask import Flask, render_template, request
from wordcloud import WordCloud
from colormaps import colormap_list
from utils import wc_to_b64, check_size

MAX_WIDTH=1920
MAX_HEIGHT=1080

app=Flask (__name__)

@app.route("/")
def main() -> None:
    return render_template ("index.html", colormap_list=colormap_list, max_width=MAX_WIDTH, max_height=MAX_HEIGHT)

@app.route("/generate/frequencies", methods=["POST"])
def generate_freq() -> None:
    words=request.form.getlist("word")
    freqs=request.form.getlist("frequency")
    try:
        freqs=[int (i) for i in freqs]
    except:
        return "Invalid frequencies values", 400
    wf=dict(zip(words, freqs))

    args={}

    args["width"]=int(request.form ["width"])
    args["height"]=int(request.form ["height"])
    args["background_color"]=request.form["bgcolor"]
    args["colormap"]=request.form["colormap"]
    args["prefer_horizontal"]=float(request.form["prefer_horizontal"])
    args["relative_scaling"]=float(request.form["relative_scaling"])
    if request.form.get("monocolor_enabled") == "on":
        monocolor=request.form["monocolor"]
        args["color_func"]=lambda *args, **kwargs: monocolor
    
    if not check_size(args["width"], args["height"], MAX_WIDTH, MAX_HEIGHT):
        return "Wordcloud size not allowed", 400

    wc=WordCloud(**args).generate_from_frequencies(wf)

    img_b64=wc_to_b64(wc)

    return render_template("generate.html", img_b64=img_b64)

@app.route("/generate/text", methods=["POST"])
def generate_text() -> None:
    input_text=request.form["input_text"]

    stopwords=request.form["stopwords"]
    stopwords=set(stopwords.splitlines())

    args={}

    args["stopwords"]=stopwords
    args["width"]=int(request.form["width"])
    args["height"]=int(request.form["height"])
    args["max_words"]=int(request.form["max_words"])
    args["background_color"]=request.form["bgcolor"]
    args["colormap"]=request.form["colormap"]
    args["prefer_horizontal"]=float(request.form ["prefer_horizontal"])
    args["relative_scaling"]=float(request.form ["relative_scaling"])
    if request.form.get("monocolor_enabled") == "on":
        monocolor=request.form["monocolor"]
        args["color_func"]=lambda *args, **kwargs: monocolor

    if not check_size(args["width"], args["height"], MAX_WIDTH, MAX_HEIGHT):
        return "Wordcloud size not allowed", 400

    wc=WordCloud(**args).generate_from_text(input_text)

    img_b64=wc_to_b64(wc)

    return render_template("generate.html", img_b64=img_b64)

#This endpoint is just for keeping the app always alive using Heroku base plan
#A cron job makes requests at a regular interval
#UPDATE: Since the application isn't hosted on Heroku anymore, it is not necessary - but still nice to have
@app.route("/ping")
def ping() -> None:
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=False)