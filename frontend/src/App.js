import React, { useState } from "react";
import Upload from "./components/Upload";
import Search from "./components/Search";
import "./App.css";

function App() {
  return (
    <div className="app">
      <h1>Visual Search with CLIP</h1>
      <Upload />
      <Search />
    </div>
  );
}

export default App;
