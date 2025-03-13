import React from 'react';
import styles from '../styles/Footer.module.css';
import { Facebook, Twitter, Instagram, Linkedin } from 'lucide-react';

function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.column}>
        <h2>LearnSphere<span>.io</span></h2>
        <p>Personalized learning assessment and guidance for students at all levels.</p>
      </div>
      <div className={styles.column}>
        <h3>Quick Links</h3>
        <a href="/">Home</a>
        <a href="/#features">Features</a>
        <a href="/#about">About Us</a>
        <a href="/signin">Sign In</a>
      </div>
      <div className={styles.column}>
        <h3>Support</h3>
        <a href="#">Help Center</a>
        <a href="#">Contact Us</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
      </div>
      <div className={styles.column}>
        <h3>Stay Connected</h3>
        <div className={styles.socialIcons}>
          <a href="#"><Facebook /></a>
          <a href="#"><Twitter /></a>
          <a href="#"><Instagram /></a>
          <a href="#"><Linkedin /></a>
        </div>
        <p>Subscribe to our newsletter</p>
        <div className={styles.newsletter}>
          <input type="email" placeholder="Your email" />
          <button>Subscribe</button>
        </div>
      </div>
    <p className={styles.copyright}>© 2025 LearnSphere.io. All rights reserved.</p>
    </footer>
  );
}

export default Footer;