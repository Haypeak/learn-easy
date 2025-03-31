import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Button from '../components/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/Auth.module.css';

function ProfileForm() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    educationLevel: '',
    schoolName: '',
    formYear: '',
    subjects: [],
    goals: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setFormData((prev) => {
        const subjects = checked
          ? [...prev.subjects, value]
          : prev.subjects.filter((subject) => subject !== value);
        return { ...prev, subjects };
      });
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
        ...(name === 'educationLevel' && { formYear: formData.formYear }), // Reset formYear when educationLevel changes
      }));
    }
  };

  const handleNext = () => {
    if (formData.educationLevel && formData.schoolName && formData.formYear) {
      if (step < 3) {
        setStep(step + 1);
      }
    } else {
      toast.error('Please fill in all required fields before proceeding.');
    }
  };

  const handlePrevious = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.educationLevel && formData.schoolName && formData.formYear && formData.goals) {
      try {
        localStorage.setItem('profile', JSON.stringify(formData));
        // fetch(`http://127.0.01:5000/auth/update/${localStorage.getItem('userId')}`, {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //     Authorization: `Bearer ${localStorage.getItem('token')}`,
        //   },
        //   body: JSON.stringify({
        //     formYear: formData.formYear,
        //     subjects: formData.subjects,
        //     schoolName: formData.schoolName,
        //     learning_goals: formData.goals,
        //   }),
        // })
        //   .then((response) => {
        //     if (!response.ok) {
        //       throw new Error('Failed to update profile');
        //     }
        //     return response.json();
        //   })
        //   .then((data) => {
        //     console.log('Profile updated successfully:', data);
        //   })
        //   .catch((error) => {
        //     console.error('Error updating profile:', error);
        //     toast.error('Failed to update profile. Please try again.');
        //   });
        toast.success('Profile saved successfully!');
        navigate('/dashboard');
      } catch (error) {
        toast.error('Failed to save profile. Please try again.');
      }
    } else {
      toast.error('Please fill in all required fields before saving.');
    }
  };

  const getFormYearOptions = () => {
    if (formData.educationLevel === 'Junior High' || formData.educationLevel === 'Senior High') {
      return ['Form 1', 'Form 2', 'Form 3'];
    } else if (formData.educationLevel === 'University') {
      return ['1st Year', '2nd Year', '3rd Year', '4th Year', 'Level 100', 'Level 200', 'Level 300', 'Level 400'];
    }
    return [];
  };

  return (
    <div>
      <Header />
      <main className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Complete Your Profile</h2>
          <p className={styles.subtitle}>Help us personalize your learning experience</p>
          <div className={styles.progress}>
            <div className={`${styles.progressStep} ${step === 1 ? styles.active : ''}`}>1</div>
            <div className={`${styles.progressStep} ${step === 2 ? styles.active : ''}`}>2</div>
            <div className={`${styles.progressStep} ${step === 3 ? styles.active : ''}`}>3</div>
          </div>
          <form onSubmit={handleSubmit}>
            {step === 1 && (
              <div>
                <h3 className={styles.formSectionTitle}>Education Information</h3>
                <div className={styles.inputGroup}>
                  <label htmlFor="educationLevel" className={styles.inputLabel}>Education Level</label>
                  <select
                    id="educationLevel"
                    name="educationLevel"
                    value={formData.educationLevel}
                    onChange={handleChange}
                    className={styles.input}
                    required
                  >
                    <option value="">Select your education level</option>
                    <option value="Junior High">Junior High</option>
                    <option value="Senior High">Senior High</option>
                    <option value="University">University</option>
                  </select>
                </div>
                <div className={styles.inputGroup}>
                  <label htmlFor="schoolName" className={styles.inputLabel}>School Name</label>
                  <input
                    type="text"
                    id="schoolName"
                    name="schoolName"
                    placeholder="Enter your school name"
                    value={formData.schoolName}
                    onChange={handleChange}
                    className={styles.input}
                    required
                  />
                </div>
                <div className={styles.inputGroup}>
                  <label htmlFor="formYear" className={styles.inputLabel}>Form/Year</label>
                  <select
                    id="formYear"
                    name="formYear"
                    value={formData.formYear}
                    onChange={handleChange}
                    className={styles.input}
                    required
                    disabled={!formData.educationLevel}
                  >
                    <option value="">Select your form/year</option>
                    {getFormYearOptions().map((option) => (
                      <option key={option} value={option}>{option}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}
            {step === 2 && (
              <div>
                <h3 className={styles.formSectionTitle}>Subjects of Interest</h3>
                <div className={styles.checkboxGroup}>
                  {['English', 'Mathematics', 'Science'].map((subject) => (
                    <label key={subject} className={styles.checkboxLabel}>
                      <input
                        type="checkbox"
                        name="subjects"
                        value={subject}
                        checked={formData.subjects.includes(subject)}
                        onChange={handleChange}
                        className={styles.checkboxInput}
                      />
                      {subject}
                    </label>
                  ))}
                </div>
              </div>
            )}
            {step === 3 && (
              <div>
                <h3 className={styles.formSectionTitle}>Learning Preferences</h3>
                <div className={styles.inputGroup}>
                  <label htmlFor="goals" className={styles.inputLabel}>Learning Goals</label>
                  <textarea
                    id="goals"
                    name="goals"
                    placeholder="e.g., Improve Math Skills, Prepare for Exams"
                    value={formData.goals}
                    onChange={handleChange}
                    className={styles.textarea}
                    required
                  />
                </div>
              </div>
            )}
            <div className={styles.buttonGroup}>
              {step > 1 && (
                <Button type="button" onClick={handlePrevious} className={styles.previousButton}>
                  Previous
                </Button>
              )}
              {step < 3 ? (
                <Button type="button" onClick={handleNext} className={styles.nextButton}>
                  Next
                </Button>
              ) : (
                <Button type="submit" className={styles.nextButton}>
                  Save Profile
                </Button>
              )}
            </div>
          </form>
        </div>
      </main>
      <ToastContainer />
    </div>
  );
}

export default ProfileForm;