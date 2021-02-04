from flask import Flask, render_template, request
import json
import server
import jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def main():
    return render_template('sample.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print("Result: ", result)
        # server.from_server(result.
        input_word = request.form.getlist('input_word')[0]
        input_sorting = request.form.getlist('input_sorting')[0]
        input_price_low = int(request.form.getlist('input_price_low')[0])
        input_price_high = int(request.form.getlist('input_price_high')[0])
        pincode = int(request.form.getlist('pincode')[0])
        product_count = int(request.form.getlist('product_count')[0])
        objs, min_product = server.from_server(input_word, input_sorting, input_price_low, input_price_high, pincode, product_count)
        # return render_template('result.html', result=result, jsonfile=objs)
        return render_template('result.html', data1 = objs, data2 = min_product)

if __name__ == "__main__":
    app.run(debug=True)
