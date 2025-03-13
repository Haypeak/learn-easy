import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Button from '../components/Button';
import styles from '../styles/ProfileForm.module.css';

function ProfileForm() {
  const [step, setStep] = useState(1);

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  return (
    <div>
      <Header />
      <main className={styles.formContainer}>
        <div className={styles.progress}>
          <span className={step === 1 ? styles.active : ''}>1</span>
          <span className={step === 2 ? styles.active : ''}>2</span>
          <span className={step === 3 ? styles.active : ''}>3</span>
        </div>
        {step === 1 && (
          <div className={styles.step}>
            <h2>Education Information</h2>
            <select>
              <option>Junior High</option>
              <option>Senior High</option>
              <option>University</option>
            </select>
            <input type="text" placeholder="School Name" />
            <Button onClick={nextStep}>Next</Button>
          </div>
        )}
        {step === 2 && (
          <div className={styles.step}>
            <h2>Subjects & Interests</h2>
            <label><input type="checkbox" /> Mathematics</label>
            <label><input type="checkbox" /> Physics</label>
            <label><input type="checkbox" /> Literature</label>
            <div className={styles.navigation}>
              <Button onClick={prevStep}>Previous</Button>
              <Button onClick={nextStep}>Next</Button>
            </div>
          </div>
        )}
        {step === 3 && (
          <div className={styles.step}>
            <h2>Learning Preferences</h2>
            <textarea placeholder="Your Goals"></textarea>
            <textarea placeholder="Your Challenges"></textarea>
            <div className={styles.navigation}>
              <Button onClick={prevStep}>Previous</Button>
              <Button>Submit</Button>
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default ProfileForm;