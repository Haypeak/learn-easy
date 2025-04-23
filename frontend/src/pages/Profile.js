import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import styles from '../styles/Profile.module.css';

export default function Profile() {
  // const { user } = useAuth(); // Removed as it is not used
  const navigate = useNavigate();
  
  const [profile, setProfile] = useState(null);
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [editForm, setEditForm] = useState({
    name: '',
    email: '',
    avatar: '',
    bio: '',
  });

  useEffect(() => {
    fetchProfileData();
    fetchEnrolledCourses();
    fetchAchievements();
  }, []);

  const fetchProfileData = async () => {
    try {
      const jwt = localStorage.getItem('jwt');
      const response = await api.get('/auth/profile', {
        headers: {
          Authorization: `Bearer ${jwt}`,
        },
      });
      setProfile(response.data);
      setEditForm(response.data);
    } catch (err) {
      setError('Failed to fetch profile data');
      console.error('Error fetching profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchEnrolledCourses = async () => {
    try {
      const response = await api.get('/auth/enrolled-courses');
      setEnrolledCourses(response.data);
    } catch (err) {
      console.error('Error fetching enrolled courses:', err);
    }
  };

  const fetchAchievements = async () => {
    try {
      const response = await api.get('/auth/achievements');
      setAchievements(response.data);
    } catch (err) {
      console.error('Error fetching achievements:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put('/auth/profile', editForm);
      setProfile(editForm);
      setIsEditing(false);
    } catch (err) {
      setError('Failed to update profile');
      console.error('Error updating profile:', err);
    }
  };

  const navigateToCourse = (courseId) => {
    navigate(`/course/${courseId}`);
  };

  if (loading) {
    return <div className={styles.loading}>Loading profile...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <div className={styles.profileHeader}>
          {profile?.avatar && (
            <img
              src={profile.avatar}
              alt="Profile"
              className={styles.avatar}
            />
          )}
          <div className={styles.profileInfo}>
            <h1>{profile?.name || 'User'}</h1>
            <p>{profile?.email}</p>
          </div>
        </div>
        <button
          onClick={() => setIsEditing(!isEditing)}
          className={styles.editButton}
        >
          {isEditing ? 'Cancel' : 'Edit Profile'}
        </button>
      </div>

      {isEditing ? (
        <form onSubmit={handleSubmit} className={styles.editForm}>
          <div className={styles.formGroup}>
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={editForm.name}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className={styles.formGroup}>
            <label htmlFor="avatar">Avatar URL</label>
            <input
              type="url"
              id="avatar"
              name="avatar"
              value={editForm.avatar || ''}
              onChange={handleInputChange}
            />
          </div>
          
          <div className={styles.formGroup}>
            <label htmlFor="bio">Bio</label>
            <textarea
              id="bio"
              name="bio"
              value={editForm.bio || ''}
              onChange={handleInputChange}
              rows={4}
            />
          </div>

          <button type="submit" className={styles.submitButton}>
            Save Changes
          </button>
        </form>
      ) : (
        <>
          <div className={styles.bio}>
            <h2>About Me</h2>
            <p>{profile?.bio || 'No bio provided'}</p>
          </div>

          <div className={styles.enrolledCourses}>
            <h2>Enrolled Courses</h2>
            {enrolledCourses.length > 0 ? (
              <div className={styles.courseGrid}>
                {enrolledCourses.map((course) => (
                  <div
                    key={course.id}
                    className={styles.courseCard}
                    onClick={() => navigateToCourse(course.id)}
                  >
                    <h3>{course.title}</h3>
                    <div className={styles.progressBar}>
                      <div
                        className={styles.progressFill}
                        style={{ width: `${course.progress}%` }}
                      />
                    </div>
                    <p>{course.progress}% Complete</p>
                    <p className={styles.lastAccessed}>
                      Last accessed: {new Date(course.lastAccessed).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className={styles.noCourses}>
                You haven't enrolled in any courses yet.
              </p>
            )}
          </div>

          <div className={styles.achievements}>
            <h2>Achievements</h2>
            {achievements.length > 0 ? (
              <div className={styles.achievementGrid}>
                {achievements.map((achievement) => (
                  <div key={achievement.id} className={styles.achievementCard}>
                    <h3>{achievement.title}</h3>
                    <p>{achievement.description}</p>
                    <p className={styles.earnedAt}>
                      Earned on: {new Date(achievement.earnedAt).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className={styles.noAchievements}>
                No achievements earned yet. Keep learning to earn badges!
              </p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

Profile.propTypes = {
  profile: PropTypes.shape({
    name: PropTypes.string,
    email: PropTypes.string,
    avatar: PropTypes.string,
    bio: PropTypes.string
  }),
  enrolledCourses: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      progress: PropTypes.number.isRequired,
      lastAccessed: PropTypes.string.isRequired
    })
  ),
  achievements: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
      earnedAt: PropTypes.string.isRequired
    })
  )
};

