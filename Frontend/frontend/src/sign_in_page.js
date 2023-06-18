import React from 'react';
import { useNavigate } from 'react-router-dom';
import { userRef, useState, useEffect} from 'react';

const SignInPage = () => {
  const navigate = useNavigate();

  const userRef = useRef()
  const errRef = errRef()

  const [user, setUser] = useState('');
  const [pwd, setPwd] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    userRef.current.focus()
  }, [])

  useEffect(() => {
    setErrorMsg('');
  }, [user, pwd])

  const handleSignIn = () => {
    navigate('/destination');
  };

  return (
    <section>
        <h1>AI English Learner</h1>
        <form>
            <label htmlFor='username'>Username: </label>
            <input
                type="text"
                id="username"
                ref={userRef}
            />
        </form>
    </section>
  );
};

export default SignInPage;