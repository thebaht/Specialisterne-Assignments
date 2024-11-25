import React, { useEffect, useState } from "react";
import './App.css'

type ApiResponse = {
  id: number;
  name: string;
};

const App: React.FC = () => {
  const [data, setData] = useState<ApiResponse  | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/item/item/1"); // Replace with your Flask API endpoint
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Flask API Data</h1>
      {data ? (
        <div>
          <p><strong>id:</strong> {data.id}</p>
          <p><strong>name:</strong> {data.name}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default App;