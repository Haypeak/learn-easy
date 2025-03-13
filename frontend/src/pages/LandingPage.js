import React from 'react';
import { Link } from 'react-router-dom';
import image1 from '../assets/1.avif';
import image2 from '../assets/2.avif';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Card from '../components/Card';
import Button from '../components/Button';
import { Book, BarChart, Lightbulb, TrendingUp } from 'lucide-react';
import styles from '../styles/LandingPage.module.css';

function LandingPage() {
  return (
    <div>
      <Header />
      <main className={styles.main}>
        {/* Hero Section */}
        <section className={styles.hero}>
          <div className={styles.heroContent}>
            <h1>Discover Your Learning Potential</h1>
            <p>
              LearnSphere.io empowers students with personalized learning paths, advanced assessments, and actionable recommendations to unlock their full academic potential. Whether you're in junior high, senior high, or university, our platform adapts to your unique needs to help you succeed.
            </p>
            <div className={styles.heroButtons}>
              <Link to="/signup">
                <Button>Get Started</Button>
              </Link>
              <Link to="/features">
                <Button variant="outline">Learn More</Button>
              </Link>
            </div>
          </div>
          <img src={image1} alt="Students learning together" className={styles.heroImage} />
        </section>

        {/* Features Section */}
        <section className={styles.features} id="features">
          <h2>How LearnSphere Works</h2>
          <div className={styles.featureGrid}>
            <Card icon={<Book />} title="Assessment" description="Complete a comprehensive assessment to identify your academic strengths and areas for improvement." />
            <Card icon={<BarChart />} title="Analysis" description="Receive detailed insights into your learning style and performance across different subject areas." />
            <Card icon={<Lightbulb />} title="Recommendations" description="Get personalized learning resources and strategies tailored to your unique educational needs." />
            <Card icon={<TrendingUp />} title="Progress Tracking" description="Monitor your improvement over time with detailed progress reports and milestone achievements." />
          </div>
        </section>

        {/* Testimonials Section */}
        <section className={styles.testimonials} id="testimonials">
          <h2>What Our Students Say</h2>
          <div className={styles.testimonialGrid}>
            <div className={styles.testimonialCard}>
              <p>"LearnSphere helped me identify my weak areas in mathematics and provided resources that finally made calculus click for me."</p>
              <div className={styles.testimonialInfo}>
                <img src="https://via.placeholder.com/50" alt="Sarah Johnson" className={styles.profileImage} />
                <div>
                  <p className={styles.testimonialName}>Sarah Johnson</p>
                  <p className={styles.testimonialRole}>University Student</p>
                </div>
              </div>
            </div>
            <div className={styles.testimonialCard}>
              <p>"As a high school student preparing for college, LearnSphere's assessment helped me focus my study efforts where they were most needed."</p>
              <div className={styles.testimonialInfo}>
                <img src="https://via.placeholder.com/50" alt="Michael Chen" className={styles.profileImage} />
                <div>
                  <p className={styles.testimonialName}>Michael Chen</p>
                  <p className={styles.testimonialRole}>High School Senior</p>
                </div>
              </div>
            </div>
            <div className={styles.testimonialCard}>
              <p>"The personalized recommendations were game-changing for my daughter's academic confidence and performance."</p>
              <div className={styles.testimonialInfo}>
                <img src="https://via.placeholder.com/50" alt="Lisa Rodriguez" className={styles.profileImage} />
                <div>
                  <p className={styles.testimonialName}>Lisa Rodriguez</p>
                  <p className={styles.testimonialRole}>Parent</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section className={styles.about} id="about">
          <div className={styles.aboutContent}>
            <h2>About LearnSphere.io</h2>
            <p>
              Founded by educators and learning specialists, LearnSphere.io is dedicated to revolutionizing how students approach their education. We believe that every student has unique learning needs and that personalized guidance is key to success.
            </p>
            <p>
              Our platform combines advanced assessment technology with proven educational methodologies to create a powerful learning tool for students at all levels, from junior high through university.
            </p>
            <Link to="/signup">
              <Button>Join LearnSphere Today</Button>
            </Link>
          </div>
          <img src={image2} alt="Students collaborating" className={styles.aboutImage} />
        </section>

        {/* Final CTA Section */}
        <section className={styles.finalCta}>
          <h2>Ready to Unlock Your Learning Potential?</h2>
          <p>
            Join thousands of students who have improved their academic performance with LearnSphere's personalized learning approach.
          </p>
          <Link to="/signup">
            <Button>Get Started for Free</Button>
          </Link>
        </section>
      </main>
      <Footer />
    </div>
  );
}

export default LandingPage;