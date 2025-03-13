import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Header from '../components/Header';
import Button from '../components/Button';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styles from '../styles/Auth.module.css';

const SignUpSchema = Yup.object().shape({
  fullName: Yup.string().required('Required'),
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(6, 'Too Short!').required('Required'),
  confirmPassword: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match').required('Required'),
});

function SignUp() {
  const { signUp } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      await signUp(values.email, values.password, values.fullName);
      toast.success('Account created successfully!');
      navigate('/profile-setup');
    } catch (error) {
      toast.error(error.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <Header />
      <main className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Create an Account</h2>
          <p className={styles.subtitle}>Sign up to your LearnSphere account</p>
          <Formik initialValues={{ fullName: '', email: '', password: '', confirmPassword: '' }} validationSchema={SignUpSchema} onSubmit={handleSubmit}>
            {({ isSubmitting }) => (
              <Form>
                <div className={styles.inputGroup}>
                  <Field
                    type="text"
                    name="fullName"
                    placeholder="Full Name"
                    className={styles.input}
                  />
                  <ErrorMessage name="fullName" component="div" className={styles.error} />
                </div>
                <div className={styles.inputGroup}>
                  <Field
                    type="email"
                    name="email"
                    placeholder="Email"
                    className={styles.input}
                  />
                  <ErrorMessage name="email" component="div" className={styles.error} />
                </div>
                <div className={styles.inputGroup}>
                  <Field
                    type="password"
                    name="password"
                    placeholder="Password"
                    className={styles.input}
                  />
                  <ErrorMessage name="password" component="div" className={styles.error} />
                </div>
                <div className={styles.inputGroup}>
                  <Field
                    type="password"
                    name="confirmPassword"
                    placeholder="Confirm Password"
                    className={styles.input}
                  />
                  <ErrorMessage name="confirmPassword" component="div" className={styles.error} />
                </div>
                <label className={styles.checkboxLabel}>
                  <Field type="checkbox" name="terms" required />
                  I agree to the terms and conditions
                </label>
                <Button type="submit" fullWidth className={styles.signInButton} disabled={isSubmitting}>
                  {isSubmitting ? 'Signing Up...' : 'Sign Up'}
                </Button>
                <p className={styles.signupLink}>
                  Already have an account? <Link to="/signin">Sign in</Link>
                </p>
              </Form>
            )}
          </Formik>
        </div>
      </main>
      <ToastContainer />
    </div>
  );
}

export default SignUp;