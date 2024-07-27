import yfinance as yf
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

def fetch_stock_data_and_save_to_csv():
    data_list = []
    columns = [
        "Stock Symbol", "Price", "Low52", "High52", "Change", "Day Low", "Day High",
        "Volume", "Average Volume", "Return 52 week", "Market Cap", "PE Ratio", "EPS", "Previous Close"
    ]
    symbols = [
       "AAPL","MSFT", "QCOM", "META", "PANW", "CRM", "GOOG", "ADBE",
    "IBM", "CSCO", "WMT", "BA", "KVUE", "BABA", "TXN", "JPM", "BAC", "MS",
    "V", "PYPL", "SQ", "C", "ADSK", "PARA", "FDX", "UPS", "GM", "EXC", "BMY",
    "PFE", "JNJ", "BP", "MCK", "MGA", "VZ", "GTLB", "PLTR", "TDOC", "ANIX",
    "DOCU", "SNAP", "NIO", "VTI", "QQQ", "DIA", "SPY", "SPYD", "VOO", "RSP",
    "IWV", "IWM", "VTWO", "IWO", "DES", "DVY", "FSKAX", "VTSAX", "IJR", "IJH",
    "IJS", "IWS", "FNDC", "FNDA", "SCHD", "VTV", "VUG", "IGM", "PRF", "XLG",
    "EFA", "EFG", "IEFA", "SCZ", "VSS", "IEMG", "FNDF", "SCHF", "SCHE", "VEU",
    "VSGX", "VGK", "VWO", "VEA", "PXH", "FUTY", "VPU", "XLU", "IBB", "XBI",
    "FREL", "ICF", "VNQ", "VNQI", "JETS", "BETZ", "IYT", "SKYY", "FTEC", "SMH",
    "IGM", "XLK", "HACK", "VOX", "IGV", "IGE", "XLE", "VDE", "XLF", "VFH", "XLY",
    "IHF", "XLV", "FHLC", "PRNT", "ARKF", "ARKG", "ARKW", "ARKK", "ARKX", "ARKQ",
    "ETHE", "GBTC", "GLD", "SLV", "XLB", "BND", "AGG", "TLT", "SHY", "ISTB", "VCPAX",
    "VSGDX", "TIP", "SCHP", "VTIP", "FLTB", "ANGL", "VTAPX", "VCSH", "VCIT", "VCLT",
    "LQD", "VWEHX", "UIINX", "PFF", "PGX", "JPC", "HYG", "JNK", "BNDX", "EMB", "VWOB",
    "VGAVX", "VEGBX", "MUC", "MUB", "NAC", "PCK", "VTEB", "CMF", "EWA", "INDA", "INDY",
    "EWG", "EWW", "SPEM", "FXI", "FHKCX", "EEM", "VIG", "VDIGX", "VWIAX", "VWINX", "VWIGX",
    "FBALX", "OPGIX", "PNOPX", "VHGEX", "PRDMX", "PRGFX", "PRHSX", "TRREX", "VTMGX", "VPADX",
    "FSPHX", "FSMEX", "FSHCX", "VGHCX", "FMCSX", "FCPVX", "FCNTX", "FBGRX", "FOSFX", "FMIJX",
    "FIGRX", "RGAGX", "GSIIX", "VTRIX", "ANAYX", "DODLX", "AIAHX", "VTAPX", "JMSIX", "PRILX",
    "SIGIX", "TGEIX", "PYEMX", "VBIAX", "VTIAX", "VVIAX", "VEIRX", "VEUSX", "VFSAX", "VSIAX",
    "OSMYX", "VMMSX", "VGAVX", "VWEAX", "TIHYX", "VCADX", "VCLAX", "VTEAX", "VTMSX", "VTMFX",
    "VUSXX"

    ]

    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1d")
            if hist.empty:
                hist = stock.history(period="1mo")

            if not hist.empty:
                info = stock.info
                data = {
                    "Stock Symbol": symbol,
                    "Price": float(hist['Close'].iloc[0]),
                    "Low52": float(info.get('fiftyTwoWeekLow', 'N/A')),
                    "High52": float(info.get('fiftyTwoWeekHigh', 'N/A')),
                    "Change": float(hist['Close'].iloc[0] - hist['Open'].iloc[0]),
                    "Day Low": float(hist['Low'].iloc[0]),
                    "Day High": float(hist['High'].iloc[0]),
                    "Volume": float(hist['Volume'].iloc[0]),
                    "Average Volume": float(info.get('averageVolume', 'N/A')),
                    "Return 52 week": float(info.get('52WeekChange', 'N/A')),
                    "Market Cap": float(info.get('marketCap', 'N/A')),
                    "PE Ratio": float(info.get('trailingPE', 'N/A')),
                    "EPS": float(info.get('trailingEps', 'N/A')),
                    "Previous Close": float(info.get('previousClose', 'N/A'))
                }
                data_list.append(data)
        except Exception as e:
            print(f"Could not fetch data for {symbol}: {e}")

    # Converting data to  DataFrame
    df = pd.DataFrame(data_list, columns=columns)

    # Save 
    save_to_csv(df)

    return data_list

def save_to_csv(df):
    # Current date
    today = datetime.today().strftime('%Y-%m-%d')
    file_name = f'stock_data_{today}.csv'

    # If already exists, append the data 
    if os.path.exists(file_name):
        df.to_csv(file_name, mode='a', header=False, index=False)
    else:
        #  save to new file
        df.to_csv(file_name, index=False) 

    print("Data processing completed.")

@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks_data = fetch_stock_data_and_save_to_csv()
    return jsonify(stocks_data)

if __name__ == '__main__':
    app.run(debug=True)
