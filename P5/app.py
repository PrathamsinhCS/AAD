from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_coins(amount, denominations):
    dp_table = [float('inf')] * (amount + 1)
    coins_chosen = [-1] * (amount + 1)
    dp_table[0] = 0

    for coin in denominations:
        for current_amount in range(coin, amount + 1):
            if dp_table[current_amount - coin] + 1 < dp_table[current_amount]:
                dp_table[current_amount] = dp_table[current_amount - coin] + 1
                coins_chosen[current_amount] = coin

    if dp_table[amount] == float('inf'):
        return -1, []

    result_set = []
    while amount > 0:
        result_set.append(coins_chosen[amount])
        amount -= coins_chosen[amount]

    return dp_table[-1], result_set

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compute', methods=['POST'])
def compute():
    amount = int(request.form['amount'])  
    denominations = [1, 4, 6]  
    coin_count, selected_coins = calculate_coins(amount, denominations)  
    return render_template('index.html', output=coin_count, coins_used=selected_coins, amount=amount)

if __name__ == '__main__':
    app.run(threaded=False)
