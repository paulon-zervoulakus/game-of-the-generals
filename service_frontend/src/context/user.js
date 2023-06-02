import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';


export const UserContext = createContext();
export function UserContextProvider({ children }){
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [profileUsername, setProfileUsername] = useState('');
    const [gameAuthToken, setGameAuthToken] = useState(false);

    const ping_session_status = async (default_count = 0, default_sleep = 3) => {
        if(!isLoggedIn){
            let longPoolCount = default_count;
            let sleep_time = default_sleep;
            if(longPoolCount > 10  && longPoolCount < 30){
                sleep_time = 10;
            }else if(longPoolCount >= 30){
                sleep_time = 30;
            }
            
            console.log("long pooling in :", sleep_time, "sec");
            
            axios.get(`/api/ping-session-status/${sleep_time}/`,
                {withCredentials: true}                
            ).then(res => {
                if('session_status' in res.data){
                    if(!res.data.session_status){
                        ping_session_status(longPoolCount + 1, sleep_time);
                    }else{
                        setIsLoggedIn(true);
                    }
                }
            }).catch(err => {
                console.log("ping aborted..");
            }); 
        }
    }
    
    const setProfile = (str_name) => setProfileUsername(str_name);
    const logout = () => {
        axios.get("/api/logout/"
        ).then(res => {
            if ('username' in res.data) {               
                setIsLoggedIn(false);
                setProfileUsername('');
                setGameAuthToken(false);
            }
        }).catch(err => { 
            console.log('logout error: ', err);
        });
    }

    const properties = {
        isLoggedInStatus: isLoggedIn,
        setIsLoggedInFunc: setIsLoggedIn,
        profileUsername: profileUsername,        
        setProfileUsernameFunc: setProfile,
        gameAuthToken: gameAuthToken,
        logoutFunc:logout
    }
    
    useEffect(()=>{
        if(isLoggedIn){
            axios.get("/api/get-user-token/"       
            ).then(res => {
                if ('game_user_token' in res.data ) {
                    setGameAuthToken(res.data.game_user_token);           
                }
            }); 
        }else{
            ping_session_status();
        }
    },[isLoggedIn]);

    return (
        <UserContext.Provider value={properties}>
            {children}
        </UserContext.Provider>
    )
}