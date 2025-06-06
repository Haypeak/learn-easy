import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Import AuthContext
// import Sidebar from '../components/Sidebar';
import { BookOpen, Target, Award } from 'lucide-react'; // For previous dashboard icons
import styles from '../styles/Dashboard.module.css';
import Header from '../components/Header';


export default function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth(); // Access logout from AuthContext
  // const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Retrieve profile data from localStorage (optional, if still needed)
  // const profile = JSON.parse(localStorage.getItem('profile') || '{}');
  // const userName = profile.schoolName ? profile.schoolName.split(' ')[0] : 'John Doe'; // Fallback name

  // Mock data for previous dashboard
  const metrics = [
    { title: 'Progress', value: '75% Complete', icon: <BookOpen /> },
    { title: 'Courses', value: '4 Active', icon: <BookOpen /> },
    { title: 'Goals', value: '2 Achieved', icon: <Target /> },
    { title: 'Awards', value: '3 Earned', icon: <Award /> },
  ];

  const recentActivity = [
    { title: 'Completed Math Assessment', detail: 'Score: 85%', time: '2 hours ago', icon: <BookOpen /> },
    { title: 'Set New Learning Goal', detail: 'Complete Advanced Physics Module', time: 'Yesterday', icon: <Target /> },
    { title: 'Earned Achievement', detail: 'Perfect score in Chemistry Quiz', time: '2 days ago', icon: <Award /> },
  ];

  // Mock data for current dashboard
  const continueLearning = {
    title: 'Introduction to Algebra',
    action: 'Resume',
    progress: 60,
  };

  const upcomingTasks = [
    { title: 'Quiz 1', date: 'Mar 5' },
    { title: 'Assignment 2', date: 'Mar 7' },
    { title: 'Module Review', date: 'Mar 10' },
  ];

  const quickStats = {
    progress: 70,
    modulesCompleted: '7 of 10 modules completed',
  };

  // var handleLogout = () => {
  //   logout(); // Call AuthContext logout function to update state
  //   navigate('/'); // Redirect to the original landing page
  // };


  return (
    <div className={styles.dashboard}>
      <Header />
      <main className={styles.mainContent}>
        <div className={styles.welcome}>
          <h2>Welcome Back!</h2>
        </div>
        <div className={styles.cards}>
          <div className={styles.card}>
            <h3>Continue Learning</h3>
            <p>{continueLearning.title}</p>
            <p>Pick up where you left off</p>
            <button className={styles.resumeButton}>Resume</button>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{ width: `${continueLearning.progress}%` }}
              ></div>
            </div>
          </div>
          <div className={styles.card}>
            <h3>Upcoming Tasks</h3>
            <ul className={styles.taskList}>
              {upcomingTasks.map((task, index) => (
                <li key={index} className={styles.taskItem}>
                  <span className={styles.taskIcon}>📅</span> {task.title} <span>{task.date}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className={styles.card}>
            <h3>Quick Stats</h3>
            <div className={styles.progressCircle}>
              <svg className={styles.circleSvg}>
                <circle cx="50" cy="50" r="40" className={styles.circleBackground} />
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  className={styles.circleProgress}
                  style={{
                    strokeDasharray: `${2 * Math.PI * 40}`,
                    strokeDashoffset: `${2 * Math.PI * 40 * (1 - quickStats.progress / 100)}`,
                  }}
                />
              </svg>
              <div className={styles.progressText}>{quickStats.progress}%</div>
            </div>
            <p>{quickStats.modulesCompleted}</p>
          </div>
          {metrics.map((metric, index) => (
            <div key={index} className={styles.card}>
              <h3>{metric.title}</h3>
              <div className={styles.metricContent}>
                {metric.icon}
                <p>{metric.value}</p>
              </div>
            </div>
          ))}
          <div className={styles.card}>
            <h3>Recent Activity</h3>
            <ul className={styles.activityList}>
              {recentActivity.map((activity, index) => (
                <li key={index} className={styles.activityItem}>
                  {activity.icon}
                  <div>
                    <p className={styles.activityTitle}>{activity.title}</p>
                    <p className={styles.activityDetail}>{activity.detail}</p>
                    <p className={styles.activityTime}>{activity.time}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
