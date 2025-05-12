import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import styles from '../styles/CourseDetail.module.css';

export default function CourseDetail() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  // const { user } = useAuth();
  
  const [course, setCourse] = useState(null);
  const [enrollmentStatus, setEnrollmentStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCourseDetails();
    fetchEnrollmentStatus();
  }, [courseId]);

  const fetchCourseDetails = async () => {
    try {
      const response = await api.get(`/learning/course/${courseId}`);
      setCourse(response.data);
    } catch (err) {
      setError('Failed to fetch course details. Please try again later.');
      console.error('Error fetching course details:', err);
    } finally {
      setLoading(false);
    }
  };


  const generateQuiz = async (topic, num_questions) => {
    try {
      const response = await api.post(`/learning/course/${courseId}/generate`, {
        topic,
        num_questions,
      });
      const updatedCourse = await api.get(`/learning/course/${courseId}`);
      setCourse(updatedCourse.data);
    } catch (err) {
      setError('Failed to request quiz. Please try again later.');
      console.error('Error requesting quiz:', err);
    }
  };

  const fetchEnrollmentStatus = async () => {
    try {
      const response = await api.get(`/learning/course/${courseId}/enrollment`);
      setEnrollmentStatus(response.data);
    } catch (err) {
      console.error('Error fetching enrollment status:', err);
    }
  };

  const handleEnrollment = async () => {
    try {
      if (enrollmentStatus?.isEnrolled) {
        await api.delete(`/learning/course/${courseId}/enrollment`);
      } else {
        await api.post(`/learning/course/${courseId}/enrollment`);
      }
      await fetchEnrollmentStatus();
    } catch (err) {
      setError('Failed to update enrollment. Please try again later.');
      console.error('Error updating enrollment:', err);
    }
  };

  const navigateToQuiz = (quizId) => {
    navigate(`/learning/quiz/${quizId}`);
  };

  if (loading) {
    return <div className={styles.loading}>Loading course details...</div>;
  }

  if (error || !course) {
    return <div className={styles.error}>{error || 'Course not found'}</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>{course.title}</h1>
        <button
          onClick={handleEnrollment}
          className={`${styles.enrollButton} ${
            enrollmentStatus?.isEnrolled ? styles.enrolled : ''
          }`}
        >
          {enrollmentStatus?.isEnrolled ? 'Unenroll' : 'Enroll Now'}
        </button>
      </div>

      <div className={styles.courseInfo}>
        <div className={styles.author}>
          <strong>Author:</strong> {course.author}
        </div>
        
        {enrollmentStatus?.isEnrolled && (
          <div className={styles.progress}>
            <strong>Progress:</strong> {enrollmentStatus.progress}%
          </div>
        )}
      </div>

      <div className={styles.description}>
        <h2>Course Description</h2>
        <p>{course.description}</p>
      </div>

      <div className={styles.content}>
        <h2>Course Content</h2>
      {course.contentItems.map((item, index) => (
        <div key={index} className={styles.contentItem}>
          {item.type === 'video' && (
            <div className={styles.video}>
              <h3>{item.title}</h3>
              <video controls>
                <source src={item.url} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          )}
          {item.type === 'article' && (
            <div className={styles.article}>
              <h3>{item.title}</h3>
              <div dangerouslySetInnerHTML={{'__html': item.content}} />
            </div>
          )}
          {item.type === 'image' && (
            <div className={styles.image}>
              <h3>{item.title}</h3>
              <img src={item.url} alt={item.title} />
            </div>
          )}
        </div>
      ))}
      </div>

      <div className={styles.structure}>
        <h2>Course Structure</h2>
        {/* {console.log(course.structure)} */}
            
             <div className={styles.noQuizzes}>
                <p>No quizzes available for this section.</p>
                <button
                  onClick={() => generateQuiz(course.title, 20)}
                  className={styles.generateQuizButton}
                >
                  Generate a Quiz
                </button>
              </div>
        {course.structure.sections.map((section, index) => (
          <div key={index} className={styles.section}>
            <h3>{section.title}</h3>
            <p>{section.description}</p>
            {section.quizzes.length > 0 && (
              <div className={styles.quizzes}>
                <h4>Quizzes</h4>
                {section.quizzes.map((quiz) => (
                  <button
                    key={quiz.id}
                    onClick={() => navigateToQuiz(quiz.id)}
                    className={styles.quizButton}
                    disabled={!enrollmentStatus?.isEnrolled}
                  >
                    {quiz.title}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

CourseDetail.propTypes = {
  course: PropTypes.shape({
    id: PropTypes.string,
    title: PropTypes.string,
    description: PropTypes.string,
    author: PropTypes.string,
    content: PropTypes.string,
    structure: PropTypes.shape({
      sections: PropTypes.arrayOf(PropTypes.shape({
        title: PropTypes.string,
        description: PropTypes.string,
        quizzes: PropTypes.arrayOf(PropTypes.shape({
          id: PropTypes.string,
          title: PropTypes.string
        }))
      }))
    })
  }),
  enrollmentStatus: PropTypes.shape({
    isEnrolled: PropTypes.bool,
    progress: PropTypes.number
  })
};

