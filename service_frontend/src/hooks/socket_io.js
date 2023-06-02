import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

export function useSocket(url, isLoggedInStatus, autoToken){
    const [userList, setUserList] = useState([]);
    const [broadcastMessage, setBroadcastMessage] = useState([]);
    const [connectionStatus, setConnectionStatus] = useState(false);

    var socket;

    const onUpdateUserList=(user_list)=>setUserList(user_list);
    const onConnect=(msg)=>setBroadcastMessage(prevBroadcastMessage => [...prevBroadcastMessage, msg]);
    const onDisconnect=(msg)=>setBroadcastMessage(prevBroadcastMessage => [...prevBroadcastMessage, msg]);
    const onBroadcastMessage=(msg)=>setBroadcastMessage(prevBroadcastMessage => [...prevBroadcastMessage, msg]);
    
    
    useEffect(() => {
        
        if(isLoggedInStatus) {
            socket = io(url, {query: {authToken: autoToken} } );
        }else {
            socket = io(url, {query: {authToken: 'visitor-only'} } );
        }

        socket.on('connect', onConnect);
        socket.on('disconnect', onDisconnect);
        socket.on('update_user_list', onUpdateUserList);
        socket.on('broadcast message', onBroadcastMessage);
        socket.on('private_lobby_message', onBroadcastMessage);
        
        return () => {        
              
            socket.off('connect', onConnect);
            socket.off('disconnect', onDisconnect);
            socket.off('update_user_list', onUpdateUserList);
            socket.off('broadcast message', onBroadcastMessage);
            socket.off('private_lobby_message', onBroadcastMessage);
                  
        };
    }, [isLoggedInStatus]);

    return { 
        broadcastMessage, 
        setBroadcastMessage, 
        userList, 
        setUserList, 
        connectionStatus,
        socket }
}
