from flask import Flask, render_template, request, redirect, url_for
from blockchain import AcademicBlockchain

app = Flask(__name__)
blockchain = AcademicBlockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if request.method == 'POST':
        student_id = request.form['student_id']
        institution = request.form['institution']
        degree = request.form['degree']
        year = request.form['year']
        
        blockchain.add_credential(student_id, institution, degree, year)
        blockchain.mine_pending_credentials()
        return redirect(url_for('index'))
    return render_template('issue.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    result = None
    if request.method == 'POST':
        student_id = request.form['student_id']
        institution = request.form['institution']
        degree = request.form['degree']
        year = request.form['year']
        
        result = blockchain.verify_credential(student_id, institution, degree, year)
    return render_template('verify.html', result=result)

@app.route('/view_chain')
def view_chain():
    return render_template('view_chain.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(debug=True)
