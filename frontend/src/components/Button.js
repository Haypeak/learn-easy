import React from 'react';
import styles from '../styles/Button.module.css';

function Button({ children, variant = 'primary', onClick, fullWidth }) {
  return (
    <button
      className={`${styles.button} ${variant === 'outline' ? styles.outline : ''} ${fullWidth ? styles.fullWidth : ''}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export default Button;