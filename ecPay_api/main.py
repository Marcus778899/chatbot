from flask import (
    Flask, 
    request,
    redirect,
    url_for,
    render_template_string
)
from flask_wtf import CSRFProtect
from .item import *
from .params import Params 
from . import module
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
csrf = CSRFProtect(app)


@app.route("/")
def index():
    form_html = """
    <form method='post' action='/login'>
        <input type='text' name='username' />
        <br/>
        <input type='hidden' name='csrf_token' value="{{ csrf_token() }}"/>
        <button type='submit'>Submit</button>
    </form>
    """
    return render_template_string(form_html)

@app.route('/login', methods=['POST']) 
def login():
    hostname = request.url
    logging.info(f'hostname: {hostname}')
    params = Params.get_params()

    ecpay_payment = module.ECPayPaymentSdk(
        MerchantID=params['MerchantID'],
        HashKey=params['HashKey'],
        HashIV=params['HashIV']
    )
    order_params = order_param_init(hostname)
    order_params.update(extend_params_1())
    order_params.update(extend_params_2())
    order_params.update(extend_params_3())
    order_params.update(extend_params_4())

    order_params.update(inv_params())
    try:
        final_order_params = ecpay_payment.create_order(order_params)

        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # Test environnment
        
        html = ecpay_payment.gen_html_post_form(action_url, final_order_params)
        return html
    
    except Exception as error:
        print('An exception happened: ' + str(error))

# ReturnURL: ecPay Server
@csrf.exempt
@app.route('/login/receive_result', methods=["POST"])
def payment_result():
    logging.info(f'Request form: {request.form}')
    get_request_form = request.form
    result = get_request_form['RtnMsg']
    trade_detail = get_request_form['CustomField1']
    trade_detail = "交易項目"
    logging.info(f'交易細項: {trade_detail}\n交易結果: {result}')
    return '1|OK'

#OrderResultURL: ecPay Client
@csrf.exempt
@app.route('/login/trad_result', methods=["Get","POST"])
def end_page():
    if request.method == "GET":
        return redirect(url_for('index'))
    if request.method == "POST":
        try:
            check_mac_value = Params.get_check_mac_value(request.form)
            logging.info(f'trad_result<CheckMacValue>: {check_mac_value}')
            logging.info(f'request.form<CheckMacValue>: {request.form["CheckMacValue"]}')

            if request.form['CheckMacValue'] != check_mac_value:
                trade_status = "交易失敗"
                logging.info(f'CheckMacValue: {request.form["CheckMacValue"]}\n交易結果: {trade_status}')
                return "請聯繫賣場人員"
            
            result = request.form['RtnMsg']
            logging.info(f'交易結果: {result}')
            if result == "Succeeded":
                trade_status = "交易成功"

                return f"<h1>{trade_status}</h1>"
        
            else:
                return f"<h1>{result}</h1>"
            
        except KeyError as e:
            logging.error(f'Missing key in request.form: {str(e)}')
            return "Request form is missing required parameters.", 400

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5000)   