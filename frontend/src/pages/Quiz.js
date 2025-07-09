import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext'; // Import AuthContext
import '../styles/Quiz.module.css';

const Quiz = () => {
  // Preset quiz data
  const presetQuiz = {
    title: 'Technology Quiz',
    timeLimit: 5, // Time limit in minutes
    questions: [
      {
        id: 1,
        question: 'What does HTML stand for?',
        options: [
          'HyperText Markup Language',
          'HighText Machine Language',
          'Hyperlink and Text Markup Language',
        ],
        correctAnswer: 'HyperText Markup Language',
      },
      {
        id: 2,
        question: 'Which programming language is primarily used for web development?',
        options: ['Python', 'JavaScript', 'C++'],
        correctAnswer: 'JavaScript',
      },
      {
        id: 3,
        question: 'What is the name of the version control system created by Linus Torvalds?',
        options: ['Git', 'SVN', 'Mercurial'],
        correctAnswer: 'Git',
      },
      {
        id: 4,
        question: 'Which company developed the React library?',
        options: ['Google', 'Facebook', 'Microsoft'],
        correctAnswer: 'Facebook',
      },
      {
        id: 5,
        question: 'What does CSS stand for?',
        options: [
          'Cascading Style Sheets',
          'Computer Style Sheets',
          'Creative Style Sheets',
        ],
        correctAnswer: 'Cascading Style Sheets',
      },
    ],
  };

  // State variables
  const [quiz, setQuiz] = useState(presetQuiz); // Use preset quiz data
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(null);

  // Timer logic
  useEffect(() => {
    if (quiz?.timeLimit && !quizResult) {
      setTimeRemaining(quiz.timeLimit * 60); // Convert minutes to seconds
      const timer = setInterval(() => {
        setTimeRemaining((prev) => (prev > 0 ? prev - 1 : 0));
      }, 1000);

      return () => clearInterval(timer); // Cleanup timer on unmount
    }
  }, [quiz?.timeLimit, quizResult]);

  // Handle answer selection
  const handleAnswer = (questionId, answer) => {
    setUserAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: answer,
    }));
  };

  // Submit quiz
  const submitQuiz = () => {
    const results = quiz.questions.map((q) => ({
      question: q.question,
      correct: userAnswers[q.id] === q.correctAnswer,
      userAnswer: userAnswers[q.id],
      correctAnswer: q.correctAnswer,
    }));
    setQuizResult(results);
  };

  const resetSelection = (questionId) => {
    setUserAnswers((prevAnswers) => ({
      ...prevAnswers,
      [questionId]: null,
    }));
  };

  // Render quiz result
  const renderResult = () => (
    <div className="quiz-results">
      <h2>Quiz Results</h2>
      {quizResult.map((result, index) => (
        <div key={index} className="result-item">
          <p>Question: {result.question}</p>
          <p>Your Answer: {result.userAnswer || 'No Answer'}</p>
          <p>
            {result.correct
              ? 'Correct!'
              : `Incorrect. Correct Answer: ${result.correctAnswer}`}
          </p>
        </div>
      ))}
    </div>
  );

  return (
    <div className="quiz-container">
      <h1 className="quiz-title">{quiz.title}</h1>
      {timeRemaining !== null && (
        <p className="quiz-timer">
          Time Remaining: {Math.floor(timeRemaining / 60)}:{timeRemaining % 60}
        </p>
      )}
      {quizResult ? (
        renderResult()
      ) : (
        <div className="quiz-question-container">
          <p className="quiz-question">
            {quiz.questions[currentQuestionIndex].question}
          </p>
          <div className="quiz-options">
            {quiz.questions[currentQuestionIndex].options.map((option) => (
              <label key={option} className="quiz-option">
                <input
                  type="checkbox"
                  checked={userAnswers[quiz.questions[currentQuestionIndex].id] === option}
                  onChange={() =>
                    handleAnswer(quiz.questions[currentQuestionIndex].id, option)
                  }
                />
                <span className="circle"></span>
                {option}
              </label>
            ))}
          </div>
          <button
            onClick={() => resetSelection(quiz.questions[currentQuestionIndex].id)}
            className="quiz-reset-button"
          >
            Reset Selection
          </button>
          <div className="quiz-navigation">
            {currentQuestionIndex > 0 && (
              <button
                onClick={() => setCurrentQuestionIndex((prev) => prev - 1)}
                className="quiz-nav-button"
              >
                Previous
              </button>
            )}
            {currentQuestionIndex < quiz.questions.length - 1 ? (
              <button
                onClick={() => setCurrentQuestionIndex((prev) => prev + 1)}
                className="quiz-nav-button"
              >
                Next
              </button>
            ) : (
              <button onClick={submitQuiz} className="quiz-submit-button">
                Submit Quiz
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Quiz;
