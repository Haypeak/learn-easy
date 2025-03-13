import React from 'react';
import styles from '../styles/Card.module.css';

function Card({ icon, title, description }) {
  return (
    <div className={styles.card}>
      {icon && <div className={styles.icon}>{icon}</div>}
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default Card;