from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def show_map():
    return render_template('traffic_hotspot_map.html')

if __name__ == '__main__':
    app.run(debug=True,port=8070, host='0.0.0.0')
