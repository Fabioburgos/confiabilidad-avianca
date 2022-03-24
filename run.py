from load import Load
from export import Export
from flask import Flask, render_template, request

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    ENV = 'development'
)

@app.route('/', methods=['GET', 'POST'])
def index():

    load = Load()
    export = Export()

    if request.method == 'POST':
        amos = load.read_file_amos(request.files.get('archivoamos'))
        airman = load.read_file_airman(request.files.get('archivoairman'))
        final_csv = export.new_dataframe(amos, airman)
        return final_csv #render_template('index.html', shape_amos = amos.shape, shape_airman = airman.shape, shape_final = final_csv)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()