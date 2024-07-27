
import React, { useState, useEffect } from 'react';
import './App.css';


function App() {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await fetch('http://localhost:5000/stocks');
        if (!response.ok) {
          throw new Error('Failed to fetch stock data');
        }
        const data = await response.json();
        setStocks(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchStockData();
  }, []);

  const handleSymbolClick = (symbol) => {
    setSelectedSymbol(symbol);
  };

  return (
    <div className="App">
      <h1>Stock Performance</h1>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Price</th>
              <th>Low 52</th>
              <th>High 52</th>
              <th>Change</th>
              <th>Day Low</th>
              <th>Day High</th>
              <th>Volume</th>
              <th>Average Volume</th>
              <th>Return 52 Week</th>
              <th>Market Cap</th>
              <th>PE Ratio</th>
              <th>EPS</th>
              <th>Previous Close</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map(stock => (
              <tr key={stock['Stock Symbol']} onClick={() => handleSymbolClick(stock['Stock Symbol'])}>
                <td>{stock['Stock Symbol']}</td>
                <td>{stock['Price']}</td>
                <td>{stock['Low52']}</td>
                <td>{stock['High52']}</td>
                <td>{stock['Change']}</td>
                <td>{stock['Day Low']}</td>
                <td>{stock['Day High']}</td>
                <td>{stock['Volume']}</td>
                <td>{stock['Average Volume']}</td>
                <td>{stock['Return 52 week']}</td>
                <td>{stock['Market Cap']}</td>
                <td>{stock['PE Ratio']}</td>
                <td>{stock['EPS']}</td>
                <td>{stock['Previous Close']}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    
    </div>
  );
}

export default App;
