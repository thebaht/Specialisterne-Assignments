import React, { useEffect, useState } from "react";
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
      const requestBody = {
        key: "value",
        anotherKey: "anotherValue",
      };
      try {
        const response = await fetch("http://127.0.0.1:5000/api/items/item",  {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody), // Include JSON body
        }); 
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const jsonData: Item[] = await response.json();
        setItems(jsonData);
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