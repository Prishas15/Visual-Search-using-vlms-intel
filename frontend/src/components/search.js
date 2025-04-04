import React, { useState } from "react";
import { searchImage } from "../api";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState("");

  const handleSearch = async () => {
    if (!query) {
      setMessage("Please enter a search query.");
      return;
    }
    try {
      setMessage("Searching...");
      const response = await searchImage(query);
      setResults(response.results);
      setMessage(response.results.length ? "Results found:" : "No results found.");
    } catch (error) {
      setMessage("Search failed. Please try again.");
    }
  };

  return (
    <div>
      <h2>Search Images</h2>
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Enter search query" />
      <button onClick={handleSearch}>Search</button>
      {message && <p>{message}</p>}
      <div>
        {results.map((image, index) => (
          <img key={index} src={`http://localhost:8000/${image}`} alt="Search result" width="100" />
        ))}
      </div>
    </div>
  );
}

export default Search;

