import React, { useState, useEffect, useContext } from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { UserContext } from "../../context/user";

export default function Login(){
    const [ username, setUsername ] = useState('');
    const [ password, setPassword ] = useState('');
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
                    <input type='text' onChange={(event)=>setUsername(event.target.value)}/>
                </div>
                <div>
                    <label>Password :</label>
                    <input type='password' onChange={(event)=>setPassword(event.target.value)}/>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    )
}