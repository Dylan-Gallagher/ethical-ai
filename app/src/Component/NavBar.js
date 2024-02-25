import React from 'react';
import './NavBar.css';
import { Link } from 'react-router-dom'; 
import logo from './Images/trinity-ibm-logo.png';
import github from './Images/github-mark.png'; 

function NavBar() {
  return (
    <nav className="navbar">
      <Link to="/">
        <img src={logo} className="nav-logo" alt="IBM Logo"/>
      </Link>
      <h1>Compliance Assistant</h1>
      <div className="navbar-main-links">
        <Link to="/about" className="navbar-item">About</Link>
      </div>
      <div className="navbar-right">
        <a href="https://github.com/AllanNastin/ethical-ai" target="_blank" rel="noopener noreferrer" className="navbar-item">
          <img src={github} className="nav-icon" alt="GitHub"/>
        </a>
      </div>
    </nav>
  );
}

export default NavBar;
