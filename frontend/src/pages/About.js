import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Button from '../components/Button';
import styles from '../styles/About.module.css';

function About() {
  return (
    <div>
      <Header />
      <main className={styles.main}>
        {/* Hero Section */}
        <section className={styles.hero}>
          <div className={styles.heroContent}>
            <h1>About LearnSphere</h1>
            <p>Revolutionizing education with personalized learning solutions.</p>
          </div>
        </section>

        {/* Mission Section */}
        <section className={styles.mission}>
          <div className={styles.container}>
            <div className={styles.missionContent}>
              <h2>Our Mission</h2>
              <p>
                At LearnSphere, we are committed to transforming education by delivering personalized learning experiences that empower every student to succeed.
              </p>
              <div className={styles.stats}>
                <div>
                  <h3>50,000+</h3>
                  <p>Active Students</p>
                </div>
                <div>
                  <h3>95%</h3>
                  <p>Success Rate</p>
                </div>
                <div>
                  <h3>1,000+</h3>
                  <p>Educational Partners</p>
                </div>
              </div>
            </div>
            <img src="https://via.placeholder.com/500x300" alt="Students collaborating" className={styles.missionImage} />
          </div>
        </section>

        {/* Core Values Section */}
        <section className={styles.coreValues}>
          <div className={styles.container}>
            <h2>Our Core Values</h2>
            <div className={styles.coreValuesGrid}>
              <div className={styles.coreValueCard}>
                <h3 style={{ color: 'var(--primary)' }}>Student-Centric</h3>
                <p>Putting students' needs at the heart of everything we do.</p>
              </div>
              <div className={styles.coreValueCard}>
                <h3 style={{ color: 'var(--primary)' }}>Innovation</h3>
                <p>Embracing cutting-edge technology for better learning.</p>
              </div>
              <div className={styles.coreValueCard}>
                <h3 style={{ color: 'var(--primary)' }}>Accessibility</h3>
                <p>Making education available to all.</p>
              </div>
              <div className={styles.coreValueCard}>
                <h3 style={{ color: 'var(--primary)' }}>Excellence</h3>
                <p>Striving for the highest standards in education.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Approach Section */}
        <section className={styles.approach}>
          <div className={styles.container}>
            <h2>Our Approach</h2>
            <div className={styles.approachGrid}>
              <div className={styles.approachStep}>
                <h3 style={{ color: 'var(--primary)' }}>1. Assessment</h3>
                <p>Evaluate your skills with advanced tools.</p>
              </div>
              <div className={styles.approachStep}>
                <h3 style={{ color: 'var(--primary)' }}>2. Analysis</h3>
                <p>Analyze your learning needs in depth.</p>
              </div>
              <div className={styles.approachStep}>
                <h3 style={{ color: 'var(--primary)' }}>3. Personalization</h3>
                <p>Create tailored learning paths.</p>
              </div>
              <div className={styles.approachStep}>
                <h3 style={{ color: 'var(--primary)' }}>4. Support</h3>
                <p>Provide ongoing guidance and resources.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Leadership Team Section */}
        <section className={styles.leadership}>
          <div className={styles.container}>
            <h2>Leadership Team</h2>
            <div className={styles.leadershipGrid}>
              <div className={styles.leadershipCard}>
                <img src="https://via.placeholder.com/200" alt="CEO" className={styles.leadershipImage} />
                <h3>Jane Doe</h3>
                <p style={{ color: 'var(--primary)' }}>CEO & Co-founder</p>
                <p>Leads the vision for personalized education.</p>
              </div>
              <div className={styles.leadershipCard}>
                <img src="https://via.placeholder.com/200" alt="CTO" className={styles.leadershipImage} />
                <h3>John Smith</h3>
                <p style={{ color: 'var(--primary)' }}>CTO</p>
                <p>Drives technological innovation.</p>
              </div>
              <div className={styles.leadershipCard}>
                <img src="https://via.placeholder.com/200" alt="Head of Education" className={styles.leadershipImage} />
                <h3>Emily Johnson</h3>
                <p style={{ color: 'var(--primary)' }}>Head of Education</p>
                <p>Oversees educational content and support.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}

export default About;