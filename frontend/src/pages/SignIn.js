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

const SignInSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(6, 'Too Short!').required('Required'),
});

function SignIn() {
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      await signIn(values.email, values.password);
      toast.success('Signed in successfully!');
      navigate('/dashboard');
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
          <h2>Welcome Back</h2>
          <p className={styles.subtitle}>Sign in to your LearnSphere account</p>
          <Formik initialValues={{ email: '', password: '' }} validationSchema={SignInSchema} onSubmit={handleSubmit}>
            {({ isSubmitting }) => (
              <Form>
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
                <Link to="/forgot-password" className={styles.forgotLink}>Forgot password?</Link>
                <Button type="submit" fullWidth className={styles.signInButton} disabled={isSubmitting}>
                  {isSubmitting ? 'Signing In...' : 'Sign In'}
                </Button>
                <p className={styles.signupLink}>
                  Don’t have an account? <Link to="/signup">Sign up</Link>
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

export default SignIn;