import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from '../styles/Header.module.css';

function Header() {
  const { user, logout } = useAuth(); // Ensure user and logout are accessed from context

  return (
    <header className={styles.header}>
      <Link to="/" className={styles.logo}>
        LearnSphere<span>.io</span>
      </Link>
      <div className={styles.navAuth}>

        {user ? (
          <>
          <Link to="/dashboard" className={styles.navLink}>Dashboard</Link>
          <Link to="/features" className={styles.navLink}>Features</Link>
          <div className={styles.dropdown}>
            <Link to="/profile" className={styles.navLink}>Profile</Link>
            <Link to="/courses" className={styles.navLink}>All Courses</Link>
            
          </div>
          <Link to="/about" className={styles.navLink}>About</Link>
          <button onClick={logout} className={styles.signOut}>Sign Out</button>
          </>
        ) : (
          <>
            <Link to="/features" className={styles.navLink}>Features</Link>
            <Link to="/about" className={styles.navLink}>About</Link>
            <Link to="/signin" className={styles.signIn}>Sign In</Link>
            <Link to="/signup" className={styles.signUp}>Sign Up</Link>
          </>
        )}
      </div>
    </header>
  );
}

export default Header;
