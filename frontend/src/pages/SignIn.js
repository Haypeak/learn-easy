// import React from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { Formik, Form, Field } from 'formik';
// import * as Yup from 'yup';
// import { toast } from 'react-toastify';
// import { useAuth } from '../context/AuthContext';

// const validationSchema = Yup.object({
//   email: Yup.string()
//     .email('Invalid email address')
//     .required('Required'),
//   password: Yup.string()
//     .required('Required'),
// });

// const SignIn = () => {
//   const { login } = useAuth();
//   const navigate = useNavigate();

//   const handleSubmit = async (values, { setSubmitting, setFieldError }) => {
//     try {
//       await login(values);
//       toast.success('Successfully signed in!');
//       navigate('/');
//     } catch (error) {
//       toast.error(error.response?.data?.error || 'Failed to sign in');
//       if (error.response?.data?.error === 'Invalid email or password') {
//         setFieldError('email', 'Invalid email or password');
//         setFieldError('password', 'Invalid email or password');
//       }
//     } finally {
//       setSubmitting(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
//       <div className="max-w-md w-full space-y-8">
//         <div>
//           <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
//             Sign in to Learn Easy
//           </h2>
//           <p className="mt-2 text-center text-sm text-gray-600">
//             Or{' '}
//             <Link
//               to="/signup"
//               className="font-medium text-indigo-600 hover:text-indigo-500"
//             >
//               create a new account
//             </Link>
//           </p>
//         </div>
//         <Formik
//           initialValues={{
//             email: '',
//             password: '',
//           }}
//           validationSchema={validationSchema}
//           onSubmit={handleSubmit}
//         >
//           {({ errors, touched, isSubmitting }) => (
//             <Form className="mt-8 space-y-6">
//               <div className="rounded-md shadow-sm -space-y-px">
//                 <div>
//                   <label htmlFor="email" className="sr-only">
//                     Email address
//                   </label>
//                   <Field
//                     id="email"
//                     name="email"
//                     type="email"
//                     autoComplete="email"
//                     className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
//                       errors.email && touched.email
//                         ? 'border-red-300'
//                         : 'border-gray-300'
//                     } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
//                     placeholder="Email address"
//                   />
//                   {errors.email && touched.email && (
//                     <div className="text-red-500 text-xs mt-1">{errors.email}</div>
//                   )}
//                 </div>
//                 <div>
//                   <label htmlFor="password" className="sr-only">
//                     Password
//                   </label>
//                   <Field
//                     id="password"
//                     name="password"
//                     type="password"
//                     autoComplete="current-password"
//                     className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
//                       errors.password && touched.password
//                         ? 'border-red-300'
//                         : 'border-gray-300'
//                     } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
//                     placeholder="Password"
//                   />
//                   {errors.password && touched.password && (
//                     <div className="text-red-500 text-xs mt-1">{errors.password}</div>
//                   )}
//                 </div>
//               </div>

//               <div>
//                 <button
//                   type="submit"
//                   disabled={isSubmitting}
//                   className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
//                     isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
//                   }`}
//                 >
//                   {isSubmitting ? 'Signing in...' : 'Sign in'}
//                 </button>
//               </div>
//             </Form>
//           )}
//         </Formik>
//       </div>
//     </div>
//   );
// };

// export default SignIn;

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