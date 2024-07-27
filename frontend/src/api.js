export const fetchStockData = async (stockSymbol) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/stocks?symbol=${stockSymbol}`);
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error('Failed to fetch stock data');
    }
  };
  