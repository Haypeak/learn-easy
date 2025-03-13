import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Button from '../components/Button';
import { Book, BarChart, Lightbulb, TrendingUp, Users, Award, Clock, MessageCircle, Layout, Zap } from 'lucide-react';
import styles from '../styles/Features.module.css';

function Features() {
  return (
    <div>
      <Header />
      <main className={styles.main}>
        {/* Hero Section */}
        <section className={styles.hero}>
          <div className={styles.heroContent}>
            <h1>Platform Features</h1>
            <p>Explore the powerful tools that make learning personalized and effective.</p>
          </div>
        </section>

        {/* Key Features Section */}
        <section className={styles.keyFeatures}>
          <div className={styles.container}>
            <h2>Key Features</h2>
            <div className={styles.keyFeatureGrid}>
              <div className={styles.keyFeatureCard}>
                <div className={styles.iconWrapper}>
                  <Book color="white" />
                </div>
                <h3>Assessment</h3>
                <p>Evaluate your current skills with comprehensive tests.</p>
                <ul>
                  <li>Adaptive testing technology</li>
                  <li>Instant feedback</li>
                  <li>Detailed skill analysis</li>
                </ul>
              </div>
              <div className={styles.keyFeatureCard}>
                <div className={styles.iconWrapper}>
                  <BarChart color="white" />
                </div>
                <h3>Analysis</h3>
                <p>Get detailed insights into your learning progress.</p>
                <ul>
                  <li>Performance tracking</li>
                  <li>Strengths and weaknesses</li>
                  <li>Customizable reports</li>
                </ul>
              </div>
              <div className={styles.keyFeatureCard}>
                <div className={styles.iconWrapper}>
                  <Lightbulb color="white" />
                </div>
                <h3>Recommendations</h3>
                <p>Receive personalized learning plans tailored to you.</p>
                <ul>
                  <li>Customized resources</li>
                  <li>Adaptive learning paths</li>
                  <li>Goal setting tools</li>
                </ul>
              </div>
              <div className={styles.keyFeatureCard}>
                <div className={styles.iconWrapper}>
                  <TrendingUp color="white" />
                </div>
                <h3>Progress Tracking</h3>
                <p>Monitor your growth with real-time updates.</p>
                <ul>
                  <li>Visual progress charts</li>
                  <li>Milestone alerts</li>
                  <li>Performance history</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* Smart Features Section */}
        <section className={styles.smartFeatures}>
          <div className={styles.container}>
            <h2>Smart Features</h2>
            <div className={styles.smartFeatureGrid}>
              <div className={styles.smartFeatureCard}>
                <Users color={styles.primary} />
                <h3>Peer Learning</h3>
                <p>Connect with peers for collaborative learning.</p>
              </div>
              <div className={styles.smartFeatureCard}>
                <Award color={styles.primary} />
                <h3>Gamification</h3>
                <p>Earn rewards to stay motivated.</p>
              </div>
              <div className={styles.smartFeatureCard}>
                <Clock color={styles.primary} />
                <h3>Flexible Scheduling</h3>
                <p>Learn at your own pace.</p>
              </div>
              <div className={styles.smartFeatureCard}>
                <MessageCircle color={styles.primary} />
                <h3>Expert Support</h3>
                <p>Get help from experienced educators.</p>
              </div>
              <div className={styles.smartFeatureCard}>
                <Layout color={styles.primary} />
                <h3>Interactive Dashboard</h3>
                <p>Track everything in one place.</p>
              </div>
              <div className={styles.smartFeatureCard}>
                <Zap color={styles.primary} />
                <h3>Quick Assessments</h3>
                <p>Fast and accurate skill checks.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Comparison Table */}
        <section className={styles.comparison}>
          <div className={styles.container}>
            <h2>LearnSphere vs Traditional Learning</h2>
            <table className={styles.comparisonTable}>
              <thead>
                <tr>
                  <th>Features</th>
                  <th>LearnSphere</th>
                  <th>Traditional Learning</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Personalized Learning</td>
                  <td>✔</td>
                  <td>Limited</td>
                </tr>
                <tr>
                  <td>Real-Time Feedback</td>
                  <td>✔</td>
                  <td>✘</td>
                </tr>
                <tr>
                  <td>Flexible Scheduling</td>
                  <td>✔</td>
                  <td>✘</td>
                </tr>
                <tr>
                  <td>Interactive Tools</td>
                  <td>✔</td>
                  <td>Limited</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}

export default Features;