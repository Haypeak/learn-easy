import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Card from '../components/Card';
import { BarChart, BookOpen, Target, Trophy } from 'lucide-react';
import styles from '../styles/Dashboard.module.css';

function Dashboard() {
  const profileData = JSON.parse(localStorage.getItem('profile')) || {};

  return (
    <div>
      <Header />
      <main className={styles.dashboard}>
      <h1>Welcome, {profileData.educationLevel || 'User'}!</h1>

        <div className={styles.stats}>
          <p>School: {profileData.schoolName}</p>
          <p>Grade/Year: {profileData.gradeYear}</p>
          <p>Learning Goals: {profileData.goals}</p>

          <Card icon={<BarChart />} title="Progress" description="75% Complete" />
          <Card icon={<BookOpen />} title="Active Courses" description="4" />
          <Card icon={<Target />} title="Goals Achieved" description="2" />
          <Card icon={<Trophy />} title="Awards Earned" description="3" />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default Dashboard;
