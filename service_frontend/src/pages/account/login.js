import React, { useState, useEffect, useContext } from "react";
import axios from 'axios';
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "../../context/user";

export default function Login(){
    const [ username, setUsername ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ errorMessage, setErrorMessage] = useState('');
    const [ csrfToken, setCsrfToken ] = useState('');
    const { 
        isLoggedInStatus, 
        setIsLoggedInFunc, 
        setProfileUsernameFunc } = useContext(UserContext);
    const navigate = useNavigate();
    
    const handleSubmit = (event) => {
        if(!isLoggedInStatus){
            event.preventDefault();
            axios.post("/account/login/",
            {username, password}
            ).then( res => {       
                if('username' in res.data){
                    setIsLoggedInFunc(true);
                    setProfileUsernameFunc(res.data.username)
                }            
                navigate('/');        
            }).catch(err => {
                if('code' in err.response.data){
                    switch (err.response.data.code){
                        case 401:
                            setErrorMessage(err.response.data.message)
                            break;

                    }
                }
            });
        }
    };
    useEffect(() => {
        if (isLoggedInStatus) {
            navigate('/');
        }
    }, [isLoggedInStatus, navigate]);
    
    return (
        <div className="__regis">
            <form onSubmit={handleSubmit}>    
                <input type="hidden" value={csrfToken} />            
                <div>
                    <label>Username :</label>
                    <span id="span-username">{errorMessage}</span>
                    <input type='text' onChange={(event)=>setUsername(event.target.value)}/>
                </div>
                <div>
                    <label>Password :</label>
                    <span id="span-username">{errorMessage}</span>
                    <input type='password' onChange={(event)=>setPassword(event.target.value)}/>
                </div>
                <button type="submit">Login</button>
                <Link to={"/account/create-user/"}>Register</Link>
            </form>
        </div>
    )
}