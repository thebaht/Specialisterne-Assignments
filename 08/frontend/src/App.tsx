import React, { useEffect, useState } from "react";
import './App.css'


const App: React.FC = () => {
  const [itemsByType, setItemsByType] = useState<Record<string, Record<string, any>[]>>({});
  const [editing, setEditing] = useState<{ type: string; rowIndex: number; column: string } | null>(null); // Track which cell is being edited
  const [tempValue, setTempValue] = useState<string>(""); 
  const [errors, setErrors] = useState<{ [key: string]: boolean }>({}); // Track errors for each cell

  const columnOrder = ["id", "name", "type", "description", "price", "discount", "quantity", "manufacturer_id", "genre_id", "num_players_max", "num_players_min", "min_age", "height", "width", "length", "character_id","num_units","num_pieces" ];

  useEffect(() => {
    const fetchData = async () => {
      const requestBody = {  };
      try {
        const response = await fetch("http://127.0.0.1:5000/api/getitems/item",  {
          method: "POST",
          headers: {"Content-Type": "application/json",},
          body: JSON.stringify(requestBody), 
        }); 
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const jsonData: Record<string, any>[] = await response.json();

        const groupedItems = jsonData.reduce((acc, item) => {
          const type = item.type || "Unknown"; 
          if (!acc[type]) {
            acc[type] = [];
          }
          acc[type].push(item);
          return acc;
        }, {} as Record<string, Record<string, any>[]>);

        setItemsByType(groupedItems);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);


  const handleCellDoubleClick = (type: string, rowIndex: number, column: string, value: any) => {
    if (column === "id") {
      return;  // Do nothing if the user clicked the 'id' column
    }
    setEditing({ type, rowIndex, column });
    setTempValue(value); // Initialize temp value with current cell value
  };

  const handleCellChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTempValue(event.target.value);
  };

  const handleSave = async () => {
    if (!editing) return;
  
    const { type, rowIndex, column } = editing;
  
    // Get the item being edited
    const updatedItemsByType = { ...itemsByType };
    const updatedRow = updatedItemsByType[type][rowIndex];

    // Don't allow editing the ID column
    if (column === "id") return;

    // Extract the ID and the updated value for the specific column
    const id = updatedRow.id;
    const updatedValue = tempValue === "null" ? null : tempValue;

    
    // Reset error state for the edited cell
    setErrors((prevErrors) => ({
      ...prevErrors,
      [`${updatedRow.id}-${column}`]: false,
    }));

    // Check if the value has actually changed
    if (updatedRow[column] === updatedValue) {
      // If the value hasn't changed, skip the API call
      setEditing(null); // Exit editing mode
      setTempValue(""); // Reset tempValue
      return;
    }
  
    // Send API call with only the updated value
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/item/item/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [column]: updatedValue }), // Send only the updated value
      });

      if (!response.ok) {
        throw new Error("Update failed");
      }
  
      // Update local state with the new value
      updatedRow[column] = updatedValue;
      setItemsByType(updatedItemsByType);
  

    } catch (error) {
      console.error("Error updating data:", error);

       // Set the error state to true for the cell that failed
       setErrors((prevErrors) => ({
        ...prevErrors,
        [`${updatedRow.id}-${column}`]: true, // Mark this cell as having an error
      }));
    }
  
    // Exit editing mode
    setEditing(null);
    setTempValue("");
  };
  

  const handleCancel = () => {
    setEditing(null);
    setTempValue("");
  };

  return (
    <div>
      {/* <h1>Flask API Data</h1> */}
      {Object.keys(itemsByType).length > 0 ? (
        Object.entries(itemsByType).map(([type, items]) => {
          // Dynamically filter columns that have at least one value in the data
          const filteredColumns = columnOrder.filter((column) =>
            items.some((item) => item[column] !== undefined)
          );

          return (
            <div key={type} style={{ marginBottom: "4rem" }}>
              <h2>{type}</h2>
              <table>
                <thead>
                  <tr>
                    {filteredColumns.map((header) => (
                      <th key={header}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {items.map((item, rowIndex) => (
                    <tr key={rowIndex}>
                      {filteredColumns.map((column) => (
                        <td
                          key={column}
                          onDoubleClick={() =>
                            handleCellDoubleClick(type, rowIndex, column, item[column])
                          }
                          style={{
                            color: errors[`${item.id}-${column}`] ? "red" : "white", // Apply red color if error occurred
                          }}
                        >
                          {editing &&
                          editing.type === type &&
                          editing.rowIndex === rowIndex &&
                          editing.column === column ? (
                            <input
                              type="text"
                              value={tempValue}
                              onChange={handleCellChange}
                              onBlur={handleSave} // Save on blur
                              onKeyDown={(e) => {
                                if (e.key === "Enter") handleSave(); // Save on Enter
                                if (e.key === "Escape") handleCancel(); // Cancel on Escape
                              }}
                              autoFocus
                            />
                          ) : (
                            item[column] || "null"
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        })
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default App;