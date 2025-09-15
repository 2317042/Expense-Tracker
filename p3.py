from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Dummy data for expenses
expenses = [
    {"id": 1, "title": "Groceries", "amount": 1500},
    {"id": 2, "title": "Electricity Bill", "amount": 2500},
    {"id": 3, "title": "Travel", "amount": 1200}
]

# Frontend HTML (React-like simple UI with JS)
frontend_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Expense Tracker</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; background: #f7f7f7; }
    h1 { color: #333; }
    #expenses { margin-top: 20px; }
    .expense { padding: 10px; background: #fff; margin: 5px 0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    input, button { padding: 8px; margin: 5px; }
  </style>
</head>
<body>
  <h1>💰 Expense Tracker</h1>

  <div>
    <input type="text" id="title" placeholder="Expense Title" />
    <input type="number" id="amount" placeholder="Amount" />
    <button onclick="addExpense()">Add Expense</button>
  </div>

  <h2>Expenses:</h2>
  <div id="expenses"></div>

  <script>
    async function loadExpenses() {
      let res = await fetch('/expenses');
      let data = await res.json();
      let container = document.getElementById('expenses');
      container.innerHTML = '';
      data.forEach(exp => {
        container.innerHTML += `<div class="expense">#${exp.id} - ${exp.title} : ₹${exp.amount}</div>`;
      });
    }

    async function addExpense() {
      let title = document.getElementById('title').value;
      let amount = document.getElementById('amount').value;
      if (!title || !amount) return alert("Enter details!");
      let res = await fetch('/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title, amount: parseInt(amount) })
      });
      let msg = await res.json();
      alert(msg.message);
      loadExpenses();
    }

    loadExpenses();
  </script>
</body>
</html>
"""

# Route for frontend
@app.route('/')
def home():
    return render_template_string(frontend_html)

# Get all expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

# Add new expense
@app.route('/expenses', methods=['POST'])
def add_expense():
    new_expense = request.json
    new_expense["id"] = len(expenses) + 1
    expenses.append(new_expense)
    return jsonify({"message": "Expense added successfully", "data": new_expense})

# Run backend + frontend
if __name__ == "__main__":
    app.run(debug=True)
