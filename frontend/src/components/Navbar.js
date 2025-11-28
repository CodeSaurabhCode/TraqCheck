import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">📋</span>
          <span className="logo-text">TraqCheck</span>
        </Link>

        <div className="navbar-menu">
          <Link 
            to="/" 
            className={`navbar-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            <span className="nav-icon">🏠</span>
            Dashboard
          </Link>
        </div>

        <div className="navbar-spacer"></div>
      </div>
    </nav>
  );
};

export default Navbar;
