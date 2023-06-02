import React, { useState, useEffect, useContext, Children, createContext } from "react";
import { io } from "socket.io-client";
import { UserContext } from "./user";

const SocketContext = createContext();
function SocketProvider({url, children}){
    const [socket, setSocket] = useState(null);
    const [broadcastMessage, setBroadcastMessage] = useState([]);
    const [userList, setUserList] = useState([]);

    const { isLoggedInStatus, gameAuthToken, setIsLoggedInFunc } = useContext(UserContext);

    const onConnect = () => setBroadcastMessage(prevBroadcastMessage => [...prevBroadcastMessage, 'Connected..']);
    const onDisconnect = () => {
        console.log('onDisconnect');
    };
    const onBroadcastMessage = (msg) => setBroadcastMessage(prevBroadcastMessage => [...prevBroadcastMessage, msg]);
    const onUpdateUserList = (user_list) => setUserList(user_list);
    const onLogoutMinions = (username) => {
        console.log(username);
        setIsLoggedInFunc(false);
    }

    useEffect(()=>{
        let newSocket;
        if(gameAuthToken && isLoggedInStatus) {
            newSocket = io(url, {query: {authToken: gameAuthToken} } );
        }else {
            newSocket = io(url, {query: {authToken: 'visitor-only'} } );
        }
        setSocket(newSocket);
        return () => newSocket.disconnect();
    },[url, isLoggedInStatus, gameAuthToken]);

    useEffect( ()=> {
        if (socket) {
            socket.on('connect', onConnect);
            socket.on('disconnect', onDisconnect);
            socket.on('broadcast message', onBroadcastMessage); 
            socket.on('private_lobby_message', onBroadcastMessage);             
            socket.on('update_user_list', onUpdateUserList);
            socket.on('logout minions', onLogoutMinions)
        }
    
        return ()=>{
           if (socket) {
               socket.off('connect');
               socket.off('disconect');
               socket.off('broadcast message');
               socket.off('private_lobby_message');
               socket.off('update_user_list');
            }
        }        
    },[socket]);

    const properties = {
        socket,
        broadcastMessage,
        userList
    }
    return (
        <SocketContext.Provider value={properties}>
            {children}
        </SocketContext.Provider>
    )
}

export { SocketContext, SocketProvider }