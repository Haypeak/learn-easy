import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../utils/api';
import styles from '../styles/Quiz.module.css';

export default function Quiz() {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [quiz, setQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(null);

  useEffect(() => {
    fetchQuiz();
  }, [quizId]);

  useEffect(() => {
    if (quiz?.timeLimit && !quizResult) {
      setTimeRemaining(quiz.timeLimit * 60); // Convert minutes to seconds
      const timer = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev === null || prev <= 1) {
            clearInterval(timer);
            handleSubmitQuiz();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [quiz]);

  const fetchQuiz = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/quizzes/${quizId}`);
      setQuiz(response.data);
    } catch (err) {
      setError('Failed to fetch quiz. Please try again later.');
      console.error('Error fetching quiz:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptionSelect = (questionId, option) => {
    const question = quiz?.questions[currentQuestionIndex];
    if (!question) return;

    setUserAnswers((prev) => {
      if (question.type === 'single') {
        return { ...prev, [questionId]: [option] };
      }

      const currentAnswers = prev[questionId] || [];
      const updatedAnswers = currentAnswers.includes(option)
        ? currentAnswers.filter((a) => a !== option)
        : [...currentAnswers, option];

      return { ...prev, [questionId]: updatedAnswers };
    });
  };

  const handleSubmitQuiz = async () => {
    try {
      const submissions = Object.entries(userAnswers).map(
        ([questionId, selectedOptions]) => ({
          questionId,
          selectedOptions,
        })
      );

      const response = await api.post(`/quizzes/${quizId}/submit`, {
        submissions,
      });

      setQuizResult(response.data);
    } catch (err) {
      setError('Failed to submit quiz. Please try again.');
      console.error('Error submitting quiz:', err);
    }
  };

  const navigateToNextQuestion = () => {
    if (!quiz) return;
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  const navigateToPreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return <div className={styles.loading}>Loading quiz...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!quiz) {
    return <div className={styles.error}>Quiz not found</div>;
  }

  if (quizResult) {
    return (
      <div className={styles.container}>
        <div className={styles.result}>
          <h2>Quiz Results</h2>
          <div className={styles.score}>
            <p>
              Score: {quizResult.score}% ({quizResult.correctAnswers} out of{' '}
              {quizResult.totalQuestions} correct)
            </p>
          </div>

          <div className={styles.feedback}>
            {quizResult.feedback.map((feedback, index) => {
              const question = quiz.questions.find((q) => q.id === feedback.questionId);
              return (
                <div
                  key={feedback.questionId}
                  className={`${styles.feedbackItem} ${
                    feedback.isCorrect ? styles.correct : styles.incorrect
                  }`}
                >
                  <p>
                    <strong>Question {index + 1}:</strong> {question?.question}
                  </p>
                  <p>
                    <strong>{feedback.isCorrect ? 'Correct!' : 'Incorrect'}</strong>
                  </p>
                  {feedback.explanation && (
                    <p className={styles.explanation}>{feedback.explanation}</p>
                  )}
                </div>
              );
            })}
          </div>

          <button
            onClick={() => navigate(-1)}
            className={styles.returnButton}
          >
            Return to Course
          </button>
        </div>
      </div>
    );
  }

  const currentQuestion = quiz.questions[currentQuestionIndex];

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>{quiz.title}</h1>
        {timeRemaining !== null && (
          <div className={styles.timer}>
            Time Remaining: {formatTime(timeRemaining)}
          </div>
        )}
      </div>

      <div className={styles.progress}>
        Question {currentQuestionIndex + 1} of {quiz.questions.length}
      </div>

      <div className={styles.question}>
        <h2>{currentQuestion.question}</h2>
        <div className={styles.options}>
          {currentQuestion.options.map((option, index) => (
            <label
              key={index}
              className={`${styles.option} ${
                userAnswers[currentQuestion.id]?.includes(option)
                  ? styles.selected
                  : ''
              }`}
            >
              <input
                type={currentQuestion.type === 'single' ? 'radio' : 'checkbox'}
                name={`question-${currentQuestion.id}`}
                value={option}
                checked={userAnswers[currentQuestion.id]?.includes(option)}
                onChange={() => handleOptionSelect(currentQuestion.id, option)}
              />
              <span className={styles.optionText}>{option}</span>
            </label>
          ))}
        </div>
      </div>

      <div className={styles.navigation}>
        <button
          onClick={navigateToPreviousQuestion}
          disabled={currentQuestionIndex === 0}
          className={styles.navButton}
        >
          Previous
        </button>

        {currentQuestionIndex === quiz.questions.length - 1 ? (
          <button
            onClick={handleSubmitQuiz}
            className={`${styles.navButton} ${styles.submit}`}
          >
            Submit Quiz
          </button>
        ) : (
          <button
            onClick={navigateToNextQuestion}
            className={styles.navButton}
          >
            Next
          </button>
        )}
      </div>
    </div>
  );
}

Quiz.propTypes = {
  quiz: PropTypes.shape({
    id: PropTypes.string,
    title: PropTypes.string,
    description: PropTypes.string,
    timeLimit: PropTypes.number,
    questions: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.string.isRequired,
        question: PropTypes.string.isRequired,
        options: PropTypes.arrayOf(PropTypes.string).isRequired,
        type: PropTypes.oneOf(['single', 'multiple']).isRequired
      })
    )
  }),
  quizResult: PropTypes.shape({
    score: PropTypes.number.isRequired,
    totalQuestions: PropTypes.number.isRequired,
    correctAnswers: PropTypes.number.isRequired,
    feedback: PropTypes.arrayOf(
      PropTypes.shape({
        questionId: PropTypes.string.isRequired,
        isCorrect: PropTypes.bool.isRequired,
        explanation: PropTypes.string
      })
    ).isRequired
  })
};

