import React, { useState, useEffect } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


export default function Signup(){
    const navigate = useNavigate();
    const [ username, setUsername ] = useState('');
    const [ email, setEmail ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ password2, setPassword2 ] = useState('');

    const [ errorUsername, setErrorUsername ] = useState('');
    const [ errorEmail, setErrorEmail] = useState('');
    const [ errorPassword, setErrorPassword] = useState('');
    const [ errorPassword2, setErrorPassword2] = useState('');
    
    const handleSubmit = (event) => {
        event.preventDefault();
        setErrorEmail('');
        setErrorPassword('');
        setErrorUsername('');
        setErrorPassword2('');
        axios.post("/account/create-user/",
           {username, password, email, password2}
        ).then( res => {            
            navigate('/account/login/');
        }).catch( err => {
            if(err.response){
                let error = err.response.data.error
                if('username' in error){
                    setErrorUsername(error.username);
                }
                if('email' in error){
                    setErrorEmail(error.email);
                }
                if('password' in error){
                    setErrorPassword(error.password);
                }
                if('password2' in error){
                    setErrorPassword2(error.password2);
                }
            }
        });
    };
   
    return (
        <div className="__regis">
            <form onSubmit={handleSubmit}>               
                <div>
                    <label htmlFor='username'>Username :</label>
                    <span id="span-username">{errorUsername}</span>
                    <input type='text' onChange={(event)=>setUsername(event.target.value)}/>
                </div>
                <div>
                    <label>Email :</label>
                    <span id="span-email">{errorEmail}</span>
                    <input type='text' onChange={(event)=>setEmail(event.target.value)}/>
                </div>
                <div>
                    <label>Password :</label>
                    <span id="span-password">{errorPassword}</span>
                    <input type='password' onChange={(event)=>setPassword(event.target.value)}/>
                </div>
                <div>
                    <label>Confirm Password :</label>
                    <span id="span-password2">{errorPassword2}</span>
                    <input type='password' onChange={(event)=>setPassword2(event.target.value)}/>
                </div>
                <button type="submit">Join me</button>
            </form>
        </div>
    )
}