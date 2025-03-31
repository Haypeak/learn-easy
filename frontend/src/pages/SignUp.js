// import React from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { Formik, Form, Field } from 'formik';
// import * as Yup from 'yup';
// import { toast } from 'react-toastify';
// import { useAuth } from '../context/AuthContext';

// const validationSchema = Yup.object({
//   name: Yup.string()
//     .required('Required')
//     .min(2, 'Name must be at least 2 characters'),
//   email: Yup.string()
//     .email('Invalid email address')
//     .required('Required'),
//   password: Yup.string()
//     .required('Required')
//     .min(6, 'Password must be at least 6 characters'),
//   confirmPassword: Yup.string()
//     .oneOf([Yup.ref('password'), null], 'Passwords must match')
//     .required('Required'),
// });

// const SignUp = () => {
//   const { register } = useAuth();
//   const navigate = useNavigate();

//   const handleSubmit = async (values, { setSubmitting, setFieldError }) => {
//     try {
//       await register({
//         name: values.name,
//         email: values.email,
//         password: values.password,
//       });
//       toast.success('Successfully registered! Welcome to Learn Easy.');
//       navigate('/');
//     } catch (error) {
//       toast.error(error.response?.data?.error || 'Failed to register');
//       if (error.response?.data?.error === 'Email already registered') {
//         setFieldError('email', 'Email already registered');
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
//             Create your account
//           </h2>
//           <p className="mt-2 text-center text-sm text-gray-600">
//             Or{' '}
//             <Link
//               to="/signin"
//               className="font-medium text-indigo-600 hover:text-indigo-500"
//             >
//               sign in to your account
//             </Link>
//           </p>
//         </div>
//         <Formik
//           initialValues={{
//             name: '',
//             email: '',
//             password: '',
//             confirmPassword: '',
//           }}
//           validationSchema={validationSchema}
//           onSubmit={handleSubmit}
//         >
//           {({ errors, touched, isSubmitting }) => (
//             <Form className="mt-8 space-y-6">
//               <div className="rounded-md shadow-sm -space-y-px">
//                 <div>
//                   <label htmlFor="name" className="sr-only">
//                     Full Name
//                   </label>
//                   <Field
//                     id="name"
//                     name="name"
//                     type="text"
//                     autoComplete="name"
//                     className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
//                       errors.name && touched.name
//                         ? 'border-red-300'
//                         : 'border-gray-300'
//                     } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
//                     placeholder="Full Name"
//                   />
//                   {errors.name && touched.name && (
//                     <div className="text-red-500 text-xs mt-1">{errors.name}</div>
//                   )}
//                 </div>
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
//                     } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
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
//                     autoComplete="new-password"
//                     className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
//                       errors.password && touched.password
//                         ? 'border-red-300'
//                         : 'border-gray-300'
//                     } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
//                     placeholder="Password"
//                   />
//                   {errors.password && touched.password && (
//                     <div className="text-red-500 text-xs mt-1">{errors.password}</div>
//                   )}
//                 </div>
//                 <div>
//                   <label htmlFor="confirmPassword" className="sr-only">
//                     Confirm Password
//                   </label>
//                   <Field
//                     id="confirmPassword"
//                     name="confirmPassword"
//                     type="password"
//                     autoComplete="new-password"
//                     className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
//                       errors.confirmPassword && touched.confirmPassword
//                         ? 'border-red-300'
//                         : 'border-gray-300'
//                     } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
//                     placeholder="Confirm Password"
//                   />
//                   {errors.confirmPassword && touched.confirmPassword && (
//                     <div className="text-red-500 text-xs mt-1">{errors.confirmPassword}</div>
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
//                   {isSubmitting ? 'Creating account...' : 'Create account'}
//                 </button>
//               </div>
//             </Form>
//           )}
//         </Formik>
//       </div>
//     </div>
//   );
// };

// export default SignUp;

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