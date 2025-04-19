from flask import Flask, jsonify, render_template

app = Flask(__name__)

# 模拟座位状态数据
seat_status = {
    1: "free",
    2: "occupied",
    3: "free",
    4: "occupied"
}

@app.route('/seat-status')
def get_seat_status():
    return jsonify(seat_status)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)