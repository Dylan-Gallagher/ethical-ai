import React, { useState } from 'react';
import PDFUpload from './Component/PDFUpload';
import KnowledgeGraph from './Component/KnowledgeGraph';
import logo from './IBM-logo.png'; 
import './App.css';

function App() {
  const [graphData, setGraphData] = useState(null);

  const handlePDFUpload = (file) => {
    console.log('Upload file to backend:', file.name);
    // Upload file to backend, then update graph data
    // setGraphData(responseData);
  };

  return (
    <div className="App">
      <div className="nav-bar">
        <img src={logo} className="nav-logo" alt="IBM Logo"/>
      </div>
      <div className="content">
        <h1>IBM Compliance Tool</h1>
        <PDFUpload onUpload={handlePDFUpload} />
        <KnowledgeGraph data={graphData} />
      </div>
    </div>
  );
}

export default App;
