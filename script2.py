# this is another script to create backend
# and return HTML templates using python

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot/')
def plot():
    # tools to visualise data through charts
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, output_file, show
    from bokeh.embed import components
    from bokeh.resources import CDN

    def inc(c,o):
        if c > o:
            value = "increase"
        elif c < o:
            value = "decrease"
        else:
            value = "equal"
        return value


    start = datetime.datetime(2017,12,1)
    end = datetime.datetime(2018,1,5)
    df = data.DataReader(name="AMZN",data_source="yahoo",start=start,end=end)
    df["status"] = [inc(c,o) for c,o in zip(df.Close,df.Open)]
    df["middle"] = (df.Close + df.Open)/2
    df["height"] = abs(df.Close - df.Open)
    df.to_csv("cs.csv")
    p = figure(x_axis_type="datetime",width=1000,height=300,responsive=True)
    p.title.text = "CandleStick"
    p.grid.grid_line_alpha = 0.3
    h12 = 12*60*60*1000
    p.segment(df.index,df.Low,df.index,df.High,color="black")
    p.rect(df.index[df.status=="increase"], df.middle[df.status=="increase"], h12, df.height[df.status=="increase"], fill_color="#ccffff", line_color="black")
    p.rect(df.index[df.status=="decrease"], df.middle[df.status=="decrease"], h12, df.height[df.status=="decrease"], fill_color="#ff3333", line_color="black")
    #output_file("cs.html")
    #show(p)

    script1, div1 = components(p)
    cdn_js = CDN.js_files
    cdn_css = CDN.css_files
    return render_template("plot.html",script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)




@app.route('/about')

def about():
    return render_template("about.html")

@app.route('/home')

def home():
    return render_template("home.html")

@app.route('/')

def layout():
    return render_template("layout.html")
if __name__ == "__main__":
    app.run(debug=True)
