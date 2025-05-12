import React from 'react';
import { FaUser, FaTachometerAlt, FaCog, FaQuestionCircle, FaSignOutAlt, FaBars, FaTimes } from 'react-icons/fa';
import styles from '../styles/Sidebar.module.css';
import { Link } from 'react-router-dom';

function Sidebar({ userName, isOpen, toggleSidebar, onLogout, activeLink }) {
  const navItems = [
    { name: 'Dashboard', icon: <FaTachometerAlt />, href: '/dashboard' },
    { name: 'Settings', icon: <FaCog />, href: '#settings' },
    { name: 'Help', icon: <FaQuestionCircle />, href: '#help' },
    { name: 'Logout', icon: <FaSignOutAlt />, href: '#', onClick: onLogout }, // Logout as a nav item
  ];

  return (
    <aside className={`${styles.sidebar} ${isOpen ? styles.open : styles.closed}`}>
      <div className={styles.sidebarHeader}>
        <button className={styles.toggleButton} onClick={toggleSidebar}>
          {isOpen ? <FaTimes /> : <FaBars />}
        </button>
        <Link to="/profile" className={styles.logo}>
        <div className={styles.userProfile}>
          <FaUser className={styles.userIcon} />
          <div>
            <p className={styles.userName}>{userName}</p>
          </div>
        </div>
        </Link>
      </div>
      <nav className={styles.nav}>
        {navItems.map((item) => (
          <a
            key={item.name}
            href={item.href}
            className={`${styles.navItem} ${activeLink === item.name.toLowerCase() ? styles.active : ''}`}
            onClick={item.onClick} // Handle logout click
          >
            {item.icon} {isOpen && item.name}
          </a>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;