import React, { useEffect, useState } from "react";
import axios from "axios";
import './App.css'

type Item = {
  id: number;
  name: string;
  description: string;
};

const App: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const requestBody = {  discount: 20.0   };
      try {
        const response = await axios.get("http://localhost:5000/api/items/item", {
          headers: {
            "Content-Type": "application/json",
          },
          data: requestBody, 
        });
        setItems(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Flask API Data</h1>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <h2>{item.name}</h2>
              <p>{item.description}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default App;